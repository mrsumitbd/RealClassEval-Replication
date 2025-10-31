from typing import Dict, List, Any, Optional
from lpm_kernel.api.services.user_llm_config_service import UserLLMConfigService
import re
import json
from openai import OpenAI
import numpy as np
from lpm_kernel.L1.bio import Cluster, Note, ShadeInfo, ShadeTimeline, ShadeMergeInfo, ShadeMergeResponse
from lpm_kernel.L1.prompt import PREFER_LANGUAGE_SYSTEM_PROMPT, SHADE_INITIAL_PROMPT, PERSON_PERSPECTIVE_SHIFT_V2_PROMPT, SHADE_MERGE_PROMPT, SHADE_IMPROVE_PROMPT, SHADE_MERGE_DEFAULT_SYSTEM_PROMPT
import traceback

class ShadeMerger:

    def __init__(self):
        self.user_llm_config_service = UserLLMConfigService()
        self.user_llm_config = self.user_llm_config_service.get_available_llm()
        if self.user_llm_config is None:
            self.client = None
            self.model_name = None
        else:
            self.client = OpenAI(api_key=self.user_llm_config.chat_api_key, base_url=self.user_llm_config.chat_endpoint)
            self.model_name = self.user_llm_config.chat_model_name
        self.model_params = {'temperature': 0, 'max_tokens': 3000, 'top_p': 0, 'frequency_penalty': 0, 'seed': 42, 'presence_penalty': 0, 'timeout': 45}
        self.preferred_language = 'en'
        self._top_p_adjusted = False

    def _fix_top_p_param(self, error_message: str) -> bool:
        """Fixes the top_p parameter if an API error indicates it's invalid.

        Some LLM providers don't accept top_p=0 and require values in specific ranges.
        This function checks if the error is related to top_p and adjusts it to 0.001,
        which is close enough to 0 to maintain deterministic behavior while satisfying
        API requirements.

        Args:
            error_message: Error message from the API response.

        Returns:
            bool: True if top_p was adjusted, False otherwise.
        """
        if not self._top_p_adjusted and 'top_p' in error_message.lower():
            logger.warning('Fixing top_p parameter from 0 to 0.001 to comply with model API requirements')
            self.model_params['top_p'] = 0.001
            self._top_p_adjusted = True
            return True
        return False

    def _call_llm_with_retry(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """Calls the LLM API with automatic retry for parameter adjustments.

        This function handles making API calls to the language model while
        implementing automatic parameter fixes when errors occur. If the API
        rejects the call due to invalid top_p parameter, it will adjust the
        parameter value and retry the call once.

        Args:
            messages: List of messages for the API call.
            **kwargs: Additional parameters to pass to the API call.

        Returns:
            API response object from the language model.

        Raises:
            Exception: If the API call fails after all retries or for unrelated errors.
        """
        try:
            return self.client.chat.completions.create(model=self.model_name, messages=messages, **self.model_params, **kwargs)
        except Exception as e:
            error_msg = str(e)
            logger.error(f'API Error: {error_msg}')
            if hasattr(e, 'response') and hasattr(e.response, 'status_code') and (e.response.status_code == 400):
                if self._fix_top_p_param(error_msg):
                    logger.info('Retrying LLM API call with adjusted top_p parameter')
                    return self.client.chat.completions.create(model=self.model_name, messages=messages, **self.model_params, **kwargs)
            raise

    def _build_user_prompt(self, shade_info_list: List[ShadeMergeInfo]) -> str:
        """Builds a user prompt from shade information list.

        Args:
            shade_info_list: List of shade merge information.

        Returns:
            Formatted string containing shade information.
        """
        shades_str = '\n\n'.join([f'Shade ID: {shade.id}\nName: {shade.name}\nAspect: {shade.aspect}\nDescription Third View: {shade.desc_third_view}\nContent Third View: {shade.content_third_view}\n' for shade in shade_info_list])
        return f'Shades List:\n{shades_str}\n'

    def _calculate_merged_shades_center_embed(self, shades: List[ShadeMergeInfo]) -> List[float]:
        """Calculates the center embedding for merged shades.

        Args:
            shades: List of shades to merge.

        Returns:
            A list of floats representing the new center embedding.

        Raises:
            ValueError: If no valid shades found or total cluster size is zero.
        """
        if not shades:
            raise ValueError('No valid shades found for the given merge list.')
        total_embedding = np.zeros(len(shades[0].cluster_info['centerEmbedding']))
        total_cluster_size = 0
        for shade in shades:
            cluster_size = shade.cluster_info['clusterSize']
            center_embedding = np.array(shade.cluster_info['centerEmbedding'])
            total_embedding += cluster_size * center_embedding
            total_cluster_size += cluster_size
        if total_cluster_size == 0:
            raise ValueError('Total cluster size is zero, cannot compute the new center embedding.')
        new_center_embedding = total_embedding / total_cluster_size
        return new_center_embedding.tolist()

    def _build_message(self, system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
        """Builds the message structure for the LLM API.

        Args:
            system_prompt: The system prompt to guide the LLM behavior.
            user_prompt: The user prompt containing the actual query.

        Returns:
            A list of message dictionaries formatted for the LLM API.
        """
        raw_message = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}]
        if self.preferred_language:
            raw_message.append({'role': 'system', 'content': PREFER_LANGUAGE_SYSTEM_PROMPT.format(language=self.preferred_language)})
        return raw_message

    def __parse_json_response(self, content: str, pattern: str, default_res: dict=None) -> Any:
        """Parses JSON response from LLM output.

        Args:
            content: The raw text response from the LLM.
            pattern: Regex pattern to extract the JSON string.
            default_res: Default result to return if parsing fails.

        Returns:
            Parsed JSON object or default_res if parsing fails.
        """
        matches = re.findall(pattern, content, re.DOTALL)
        if not matches:
            logger.error(f'No Json Found: {content}')
            return default_res
        try:
            json_res = json.loads(matches[0])
        except Exception as e:
            logger.error(f'Json Parse Error: {traceback.format_exc()}-{content}')
            return default_res
        return json_res

    def merge_shades(self, shade_info_list: List[ShadeMergeInfo]) -> ShadeMergeResponse:
        """Merges multiple shades based on their similarity.

        Args:
            shade_info_list: List of shade information to be evaluated for merging.

        Returns:
            ShadeMergeResponse object with merge results or error information.
        """
        try:
            for shade in shade_info_list:
                logger.info(f'shade: {shade}')
            user_prompt = self._build_user_prompt(shade_info_list)
            merge_decision_message = self._build_message(SHADE_MERGE_DEFAULT_SYSTEM_PROMPT, user_prompt)
            logger.info(f'Built merge_decision_message: {merge_decision_message}')
            response = self._call_llm_with_retry(merge_decision_message)
            content = response.choices[0].message.content
            logger.info(f'Shade Merge Decision Result: {content}')
            try:
                merge_shade_list = self.__parse_json_response(content, '\\[.*\\]')
                logger.info(f'Parsed merge_shade_list: {merge_shade_list}')
            except Exception as e:
                raise Exception(f'Failed to parse the shade merge list: {content}') from e
            if not merge_shade_list:
                final_merge_shade_list = []
            else:
                final_merge_shade_list = []
                for group in merge_shade_list:
                    shade_ids = group
                    logger.info(f'Processing group with shadeIds: {shade_ids}')
                    if not shade_ids:
                        continue
                    shades = [shade for shade in shade_info_list if str(shade.id) in shade_ids]
                    if not shades:
                        logger.info(f'No valid shades found for shadeIds: {shade_ids}. Skipping this group.')
                        continue
                    new_cluster_embedd = self._calculate_merged_shades_center_embed(shades)
                    logger.info(f'Calculated new cluster embedding: {new_cluster_embedd}')
                    final_merge_shade_list.append({'shadeIds': shade_ids, 'centerEmbedding': new_cluster_embedd})
            result = {'mergeShadeList': final_merge_shade_list}
            response = ShadeMergeResponse(result=result, success=True)
        except Exception as e:
            logger.error(traceback.format_exc())
            response = ShadeMergeResponse(result=str(e), success=False)
        return response