import os
from workbench.utils.workbench_cache import WorkbenchCache
import re
from openai import OpenAI
import logging

class AISummary:

    def __init__(self):
        """
        Initialize the AISummary class by setting up the OpenAI client.
        """
        self.log = logging.getLogger('workbench')
        self.deepseek_api = os.getenv('DEEPSEEK_API')
        if not self.deepseek_api:
            raise ValueError('DEEPSEEK API key is not set')
        self.client = OpenAI(api_key=self.deepseek_api, base_url='https://api.deepseek.com/v1')
        self.ai_cache = WorkbenchCache(prefix='ai_summary')

    def smiles_query(self, smiles_string: str, force_pull=False) -> str:
        """
        Query the DeepSeek API for information about a compound using its SMILES string.

        Args:
            smiles_string (str): The SMILES string of the compound.
            force_pull (bool, optional): Force the API to pull the data again. Defaults to False.

        Returns:
            str: A markdown-formatted bulleted list of the compound's properties.
        """
        cached_summary = self.ai_cache.get(smiles_string)
        if cached_summary and (not force_pull):
            self.log.info(f'Using cached summary for SMILES: {smiles_string}')
            return cached_summary
        self.log.info(f'Querying the API for SMILES: {smiles_string}')
        task = '\n            Search open sources and use internal chemistry knowledge to provide a concise\n            summary of its properties relevant to targeted therapeutics and toxicity.\n            DO NOT INCLUDE INTRODUCTORY SENTENCES, CONCLUSIONS, OR CONVERSATIONAL PHRASES\n        '
        lookup_context = {'action': 'lookup', 'resources': ['PubMed', 'PubChem', 'ChEMBL', 'DrugBank', 'ChemSpider', 'open source'], 'query': f'Find information about the compound with SMILES {smiles_string}. {task}'}
        try:
            response = self.client.chat.completions.create(model='deepseek-chat', messages=[{'role': 'user', 'content': str(lookup_context)}])
            summary = response.choices[0].message.content
            summary = '\n'.join([line for line in summary.split('\n') if 'SMILES' not in line])
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