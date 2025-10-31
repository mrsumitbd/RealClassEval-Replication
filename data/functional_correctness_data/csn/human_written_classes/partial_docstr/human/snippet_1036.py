from workbench.utils.workbench_cache import WorkbenchCache
import logging
import os
import re
from openai import OpenAI
import datetime

class AISynth:

    def __init__(self, llm_provider='deepseek', llm_model='deepseek-reasoner'):
        """
        Initialize the AISynth class by setting up the OpenAI client.
        """
        self.log = logging.getLogger('workbench')
        if llm_provider == 'openai':
            self.api_key = os.getenv('OPENAI_API')
            self.base_url = 'https://api.openai.com/v1'
            self.model = 'o3-mini'
            self.model = 'gpt-4o'
        else:
            current_time = datetime.datetime.utcnow().time()
            off_peak_start = datetime.time(16, 30)
            off_peak_end = datetime.time(0, 30)
            is_off_peak = off_peak_start <= current_time <= off_peak_end
            print(f'Is off-peak: {is_off_peak}')
            self.api_key = os.getenv('DEEPSEEK_API')
            self.base_url = 'https://api.deepseek.com/v1'
            self.model = 'deepseek-chat'
            self.model = 'deepseek-reasoner'
        if not self.api_key:
            raise ValueError('AI API key is not set')
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.ai_cache = WorkbenchCache(prefix='ai_synth')

    def smiles_query(self, smiles_string: str, force_pull=False) -> str:
        """
        Query the LLM API for information about a compound using its SMILES string.

        Args:
            smiles_string (str): The SMILES string of the compound.
            force_pull (bool, optional): Force the API to pull the data again. Defaults to False.

        Returns:
            str: A markdown-formatted response containing a synthetic accessibility score (1-10)
                 and a description of how to synthesize the compound.
        """
        cached_summary = self.ai_cache.get(smiles_string)
        if cached_summary and (not force_pull):
            self.log.info(f'Using cached summary for SMILES: {smiles_string}')
            return cached_summary
        self.log.info(f'Querying the API for SMILES: {smiles_string}')
        task = '\n            Provide the following information for the compound with the given SMILES string:\n            1. A synthetic accessibility score (1-10), where 1 is very easy to synthesize and 10 is very difficult.\n            2. A concise description of how to synthesize the compound, including common precursors and reaction steps.\n            DO NOT INCLUDE INTRODUCTORY SENTENCES, CONCLUSIONS, OR CONVERSATIONAL PHRASES.\n        '
        lookup_context = {'action': 'lookup', 'resources': ['PubMed', 'PubChem', 'ChEMBL', 'DrugBank', 'ChemSpider', 'open source'], 'query': f'Provide synthetic accessibility information for compound {smiles_string}. {task}'}
        try:
            response = self.client.chat.completions.create(model=self.model, messages=[{'role': 'user', 'content': str(lookup_context)}])
            summary = response.choices[0].message.content
            self.ai_cache.set(smiles_string, summary)
            return summary
        except Exception as e:
            return f'### Error\n\nAn error occurred while querying the API: {str(e)}'

    @staticmethod
    def clean_summary(response: str) -> str:
        response = re.sub('^\\d+\\.\\s', '', response, flags=re.MULTILINE)
        cleaned_lines = [line.strip() for line in response.split('\n')]
        cleaned_response = '\n'.join(cleaned_lines)
        return cleaned_response