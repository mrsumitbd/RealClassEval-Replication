from langgraph.prebuilt import create_react_agent
from agents.tools.external_deps import ExternalDepsTool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from pathlib import Path
import time
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv
from agents.tools import CodeReferenceReader, CodeStructureTool, PackageRelationsTool, FileStructureTool, GetCFGTool, MethodInvocationsTool, ReadFileTool
import logging
from google.api_core.exceptions import ResourceExhausted
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.tools.read_docs import ReadDocsTool
from trustcall import create_extractor
from agents.agent_responses import AnalysisInsights
from static_analyzer.analysis_result import StaticAnalysisResults
from langchain_aws import ChatBedrockConverse

class CodeBoardingAgent:

    def __init__(self, repo_dir: Path, static_analysis: StaticAnalysisResults, system_message: str):
        self._setup_env_vars()
        self.llm = self._initialize_llm()
        self.repo_dir = repo_dir
        self.read_source_reference = CodeReferenceReader(static_analysis=static_analysis)
        self.read_packages_tool = PackageRelationsTool(static_analysis=static_analysis)
        self.read_structure_tool = CodeStructureTool(static_analysis=static_analysis)
        self.read_file_structure = FileStructureTool(repo_dir=repo_dir)
        self.read_cfg_tool = GetCFGTool(static_analysis=static_analysis)
        self.read_method_invocations_tool = MethodInvocationsTool(static_analysis=static_analysis)
        self.read_file_tool = ReadFileTool(repo_dir=repo_dir)
        self.read_docs = ReadDocsTool(repo_dir=repo_dir)
        self.external_deps_tool = ExternalDepsTool(repo_dir=repo_dir)
        self.agent = create_react_agent(model=self.llm, tools=[self.read_source_reference, self.read_file_tool, self.read_file_structure, self.read_structure_tool, self.read_packages_tool])
        self.static_analysis = static_analysis
        self.system_message = SystemMessage(content=system_message)

    def _setup_env_vars(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_base_url = os.getenv('OPENAI_BASE_URL')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.aws_bearer_token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        self.aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL')

    def _initialize_llm(self):
        """Initialize LLM based on available API keys with priority order."""
        if self.openai_api_key:
            logger.info('Using OpenAI LLM')
            return ChatOpenAI(model='gpt-4o', temperature=0, max_tokens=None, timeout=None, max_retries=2, api_key=self.openai_api_key, base_url=self.openai_base_url)
        elif self.anthropic_api_key:
            logger.info('Using Anthropic LLM')
            return ChatAnthropic(model='claude-3-5-sonnet-20241022', temperature=0, max_tokens=None, timeout=None, max_retries=2, api_key=self.anthropic_api_key)
        elif self.google_api_key:
            logger.info('Using Google Gemini LLM')
            return ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0, max_tokens=None, timeout=None, max_retries=2, api_key=self.google_api_key)
        elif self.aws_bearer_token:
            logger.info('Using AWS Bedrock Converse LLM')
            return ChatBedrockConverse(model='us.anthropic.claude-3-7-sonnet-20250219-v1:0', temperature=0, max_tokens=4096, region_name=self.aws_region, credentials_profile_name=None)
        elif self.ollama_base_url:
            logging.info('Using Ollama LLM')
            return ChatOllama(model='qwen3:32b', base_url=self.ollama_base_url, temperature=0, max_tokens=None, timeout=None, max_retries=2)
        else:
            raise ValueError('No valid API key found. Please set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, or AWS_BEARER_TOKEN_BEDROCK')

    def _invoke(self, prompt) -> str:
        """Unified agent invocation method."""
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.agent.invoke({'messages': [self.system_message, HumanMessage(content=prompt)]})
                agent_response = response['messages'][-1]
                assert isinstance(agent_response, AIMessage), f'Expected AIMessage, but got {type(agent_response)}'
                if type(agent_response.content) == str:
                    return agent_response.content
                if type(agent_response.content) == list:
                    return ''.join([message for message in agent_response.content])
            except (ResourceExhausted, Exception) as e:
                logger.error(f'Resource exhausted, retrying... in 60 seconds: Type({type(e)}) {e}')
                time.sleep(60)
        logger.error('Max retries reached. Failed to get response from the agent.')
        return 'Could not get response from the agent.'

    def _parse_invoke(self, prompt, type):
        response = self._invoke(prompt)
        return self._parse_response(prompt, response, type)

    def _parse_response(self, prompt, response, return_type, max_retries=5):
        if max_retries == 0:
            logger.error(f'Max retries reached for parsing response: {response}')
            raise Exception(f'Max retries reached for parsing response: {response}')
        extractor = create_extractor(self.llm, tools=[return_type], tool_choice=return_type.__name__)
        if response is None or response.strip() == '':
            logger.error(f'Empty response for prompt: {prompt}')
        try:
            result = extractor.invoke(response)['responses'][0]
            return return_type.model_validate(result)
        except (ResourceExhausted, Exception) as e:
            logger.error(f'Resource exhausted or parsing error, retrying... in 60 seconds: Type({type(e)}) {e}')
            time.sleep(60)
            return self._parse_response(prompt, response, return_type, max_retries - 1)

    def fix_source_code_reference_lines(self, analysis: AnalysisInsights):
        for component in analysis.components:
            for reference in component.referenced_source_code:
                for lang in self.static_analysis.get_languages():
                    try:
                        qname = reference.qualified_name.replace('/', '.')
                        node = self.static_analysis.get_reference(lang, qname)
                        reference.reference_file = node.file_path
                        reference.reference_start_line = node.line_start + 1
                        reference.reference_end_line = node.line_end + 1
                        reference.qualified_name = qname
                    except (ValueError, FileExistsError) as e:
                        qname = reference.qualified_name.replace('/', '.')
                        _, node = self.static_analysis.get_loose_reference(lang, qname)
                        if node is not None:
                            reference.reference_file = node.file_path
                            reference.reference_start_line = node.line_start + 1
                            reference.reference_end_line = node.line_end + 1
                            reference.qualified_name = qname
                            break
                        logger.warning(f'[Reference Resolution] Reference {reference.qualified_name} not found in {lang}: {e}')
                        if reference.reference_file is not None and (not reference.reference_file.startswith('/')):
                            joined_path = os.path.join(self.repo_dir, reference.reference_file)
                            if os.path.exists(joined_path):
                                reference.reference_file = joined_path
                                break
                            else:
                                logger.warning(f'[Reference Resolution] Reference file {reference.reference_file} does not exist for {lang}.')
                                reference.reference_file = None
                        file_path = reference.qualified_name.replace('.', '/')
                        full_path = os.path.join(self.repo_dir, file_path)
                        file_ref = '.'.join(full_path.rsplit('/', 1))
                        paths = [full_path, f'{file_path}.py', f'{file_path}.ts', f'{file_path}.tsx', file_ref]
                        found_ref = False
                        for path in paths:
                            if os.path.exists(path):
                                reference.reference_file = str(path)
                                found_ref = True
                                break
                        if found_ref:
                            break
                        if reference.reference_file is None:
                            logger.error(f'[Reference Resolution] Reference file {reference.qualified_name} not found!')
        return analysis