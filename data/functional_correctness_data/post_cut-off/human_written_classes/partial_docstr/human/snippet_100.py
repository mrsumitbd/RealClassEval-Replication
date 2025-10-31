import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import contextlib

class ToolRetriever:
    """Retrieve tools from the tool registry."""

    def __init__(self):
        pass

    def prompt_based_retrieval(self, query: str, resources: dict, llm=None) -> dict:
        """Use a prompt-based approach to retrieve the most relevant resources for a query.

        Args:
            query: The user's query
            resources: A dictionary with keys 'tools', 'data_lake', and 'libraries',
                      each containing a list of available resources
            llm: Optional LLM instance to use for retrieval (if None, will create a new one)

        Returns:
            A dictionary with the same keys, but containing only the most relevant resources

        """
        prompt = f"\nYou are an expert biomedical research assistant. Your task is to select the relevant resources to help answer a user's query.\n\nUSER QUERY: {query}\n\nBelow are the available resources. For each category, select items that are directly or indirectly relevant to answering the query.\nBe generous in your selection - include resources that might be useful for the task, even if they're not explicitly mentioned in the query.\nIt's better to include slightly more resources than to miss potentially useful ones.\n\nAVAILABLE TOOLS:\n{self._format_resources_for_prompt(resources.get('tools', []))}\n\nAVAILABLE DATA LAKE ITEMS:\n{self._format_resources_for_prompt(resources.get('data_lake', []))}\n\nAVAILABLE SOFTWARE LIBRARIES:\n{self._format_resources_for_prompt(resources.get('libraries', []))}\n\nFor each category, respond with ONLY the indices of the relevant items in the following format:\nTOOLS: [list of indices]\nDATA_LAKE: [list of indices]\nLIBRARIES: [list of indices]\n\nFor example:\nTOOLS: [0, 3, 5, 7, 9]\nDATA_LAKE: [1, 2, 4]\nLIBRARIES: [0, 2, 4, 5, 8]\n\nIf a category has no relevant items, use an empty list, e.g., DATA_LAKE: []\n\nIMPORTANT GUIDELINES:\n1. Be generous but not excessive - aim to include all potentially relevant resources\n2. ALWAYS prioritize database tools for general queries - include as many database tools as possible\n3. Include all literature search tools\n4. For wet lab sequence type of queries, ALWAYS include molecular biology tools\n5. For data lake items, include datasets that could provide useful information\n6. For libraries, include those that provide functions needed for analysis\n7. Don't exclude resources just because they're not explicitly mentioned in the query\n8. When in doubt about a database tool or molecular biology tool, include it rather than exclude it\n"
        if llm is None:
            llm = ChatOpenAI(model='gpt-4o')
        if hasattr(llm, 'invoke'):
            response = llm.invoke([HumanMessage(content=prompt)])
            response_content = response.content
        else:
            response_content = str(llm(prompt))
        selected_indices = self._parse_llm_response(response_content)
        selected_resources = {'tools': [resources['tools'][i] for i in selected_indices.get('tools', []) if i < len(resources.get('tools', []))], 'data_lake': [resources['data_lake'][i] for i in selected_indices.get('data_lake', []) if i < len(resources.get('data_lake', []))], 'libraries': [resources['libraries'][i] for i in selected_indices.get('libraries', []) if i < len(resources.get('libraries', []))]}
        return selected_resources

    def _format_resources_for_prompt(self, resources: list) -> str:
        """Format resources for inclusion in the prompt."""
        formatted = []
        for i, resource in enumerate(resources):
            if isinstance(resource, dict):
                name = resource.get('name', f'Resource {i}')
                description = resource.get('description', '')
                formatted.append(f'{i}. {name}: {description}')
            elif isinstance(resource, str):
                formatted.append(f'{i}. {resource}')
            else:
                name = getattr(resource, 'name', str(resource))
                desc = getattr(resource, 'description', '')
                formatted.append(f'{i}. {name}: {desc}')
        return '\n'.join(formatted) if formatted else 'None available'

    def _parse_llm_response(self, response: str) -> dict:
        """Parse the LLM response to extract the selected indices."""
        selected_indices = {'tools': [], 'data_lake': [], 'libraries': []}
        tools_match = re.search('TOOLS:\\s*\\[(.*?)\\]', response, re.IGNORECASE)
        if tools_match and tools_match.group(1).strip():
            with contextlib.suppress(ValueError):
                selected_indices['tools'] = [int(idx.strip()) for idx in tools_match.group(1).split(',') if idx.strip()]
        data_lake_match = re.search('DATA_LAKE:\\s*\\[(.*?)\\]', response, re.IGNORECASE)
        if data_lake_match and data_lake_match.group(1).strip():
            with contextlib.suppress(ValueError):
                selected_indices['data_lake'] = [int(idx.strip()) for idx in data_lake_match.group(1).split(',') if idx.strip()]
        libraries_match = re.search('LIBRARIES:\\s*\\[(.*?)\\]', response, re.IGNORECASE)
        if libraries_match and libraries_match.group(1).strip():
            with contextlib.suppress(ValueError):
                selected_indices['libraries'] = [int(idx.strip()) for idx in libraries_match.group(1).split(',') if idx.strip()]
        return selected_indices