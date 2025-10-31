from services.config_service import config_service
from typing import List, Dict, Any, Optional
import os

class OptionService:
    """选项生成服务类"""

    def __init__(self):
        """初始化选项生成服务"""
        self.config_service = config_service
        if not self.config_service.initialized:
            self.config_service.initialize()
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv('OPTION_API_KEY'), base_url=os.getenv('OPTION_API_BASE_URL'))
        except ImportError:
            print('未找到openai模块，请安装openai模块')
            self.client = None

    def generate_options(self, conversation_history: List[Dict[str, str]], character_config: Dict[str, Any], user_query: str) -> List[str]:
        """
        生成对话选项

        Args:
            conversation_history: 对话历史记录
            character_config: 角色配置
            user_query: 用户最后的查询

        Returns:
            生成的选项列表（最多3个）

        Raises:
            APIError: 当API调用失败时
        """
        option_config = self.config_service.get_option_config()
        if not option_config.get('enable_option_generation', True):
            return []
        if not self.client:
            print('OpenAI客户端未初始化，跳过选项生成')
            return []
        system_prompt = self.config_service.get_option_system_prompt()
        user_prompt = self._build_user_prompt(conversation_history, character_config, user_query)
        try:
            extra_body_list = ['temperature', 'max_tokens', 'enable_reasoning']
            extra_body_dict = {k: option_config[k] for k in extra_body_list if k in option_config}
            request_params = {'model': os.getenv('OPTION_MODEL'), 'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}], 'extra_body': extra_body_dict}
            response = self.client.chat.completions.create(**request_params)
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content.strip()
                options = [opt.strip() for opt in content.split('\n') if opt.strip()]
                return options[:3]
            return []
        except Exception as e:
            print(f'选项生成失败: {str(e)}')
            return []

    def _build_user_prompt(self, conversation_history: List[Dict[str, str]], character_config: Dict[str, Any], user_query: str) -> str:
        """
        构建用户提示词

        Args:
            conversation_history: 对话历史记录
            character_config: 角色配置
            user_query: 用户最后的查询

        Returns:
            构建的用户提示词
        """
        history_text = ''
        for msg in conversation_history[-6:]:
            role = msg['role']
            content = msg['content']
            if role == 'user':
                history_text += f'用户: {content}\n'
            elif role == 'assistant':
                history_text += f"{character_config['name']}: {content}\n"
        character_setting = f"角色名称: {character_config['name']}\n"
        character_setting += f"角色描述: {character_config['description']}\n"
        character_setting += f"角色设定: {character_config['prompt']}\n"
        user_prompt = f'对话历史:\n{history_text}\n\n{character_setting}\n\n用户最后输入: {user_query}\n\n请基于以上对话历史、角色设定和用户最后的问题，生成3个**用户**可能想要说的选项。'
        return user_prompt