from jinja2 import Template
from config.logger import setup_logging
import cnlunar
import os
from typing import Dict, Any

class PromptManager:
    """系统提示词管理器，负责管理和更新系统提示词"""

    def __init__(self, config: Dict[str, Any], logger=None):
        self.config = config
        self.logger = logger or setup_logging()
        self.base_prompt_template = None
        self.last_update_time = 0
        from core.utils.cache.manager import cache_manager, CacheType
        self.cache_manager = cache_manager
        self.CacheType = CacheType
        self._load_base_template()

    def _load_base_template(self):
        """加载基础提示词模板"""
        try:
            template_path = 'agent-base-prompt.txt'
            cache_key = f'prompt_template:{template_path}'
            cached_template = self.cache_manager.get(self.CacheType.CONFIG, cache_key)
            if cached_template is not None:
                self.base_prompt_template = cached_template
                self.logger.bind(tag=TAG).debug('从缓存加载基础提示词模板')
                return
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                self.cache_manager.set(self.CacheType.CONFIG, cache_key, template_content)
                self.base_prompt_template = template_content
                self.logger.bind(tag=TAG).debug('成功加载基础提示词模板并缓存')
            else:
                self.logger.bind(tag=TAG).warning('未找到agent-base-prompt.txt文件')
        except Exception as e:
            self.logger.bind(tag=TAG).error(f'加载提示词模板失败: {e}')

    def get_quick_prompt(self, user_prompt: str, device_id: str=None) -> str:
        """快速获取系统提示词（使用用户配置）"""
        device_cache_key = f'device_prompt:{device_id}'
        cached_device_prompt = self.cache_manager.get(self.CacheType.DEVICE_PROMPT, device_cache_key)
        if cached_device_prompt is not None:
            self.logger.bind(tag=TAG).debug(f'使用设备 {device_id} 的缓存提示词')
            return cached_device_prompt
        else:
            self.logger.bind(tag=TAG).debug(f'设备 {device_id} 无缓存提示词，使用传入的提示词')
        if device_id:
            device_cache_key = f'device_prompt:{device_id}'
            self.cache_manager.set(self.CacheType.CONFIG, device_cache_key, user_prompt)
            self.logger.bind(tag=TAG).debug(f'设备 {device_id} 的提示词已缓存')
        self.logger.bind(tag=TAG).info(f'使用快速提示词: {user_prompt[:50]}...')
        return user_prompt

    def _get_current_time_info(self) -> tuple:
        """获取当前时间信息"""
        from datetime import datetime
        now = datetime.now()
        today_date = now.strftime('%Y-%m-%d')
        today_weekday = WEEKDAY_MAP[now.strftime('%A')]
        today_lunar = cnlunar.Lunar(now, godType='8char')
        lunar_date = '%s年%s%s\n' % (today_lunar.lunarYearCn, today_lunar.lunarMonthCn[:-1], today_lunar.lunarDayCn)
        return (today_date, today_weekday, lunar_date)

    def _get_location_info(self, client_ip: str) -> str:
        """获取位置信息"""
        try:
            cached_location = self.cache_manager.get(self.CacheType.LOCATION, client_ip)
            if cached_location is not None:
                return cached_location
            from core.utils.util import get_ip_info
            ip_info = get_ip_info(client_ip, self.logger)
            city = ip_info.get('city', '未知位置')
            location = f'{city}'
            self.cache_manager.set(self.CacheType.LOCATION, client_ip, location)
            return location
        except Exception as e:
            self.logger.bind(tag=TAG).error(f'获取位置信息失败: {e}')
            return '未知位置'

    def _get_weather_info(self, conn, location: str) -> str:
        """获取天气信息"""
        try:
            cached_weather = self.cache_manager.get(self.CacheType.WEATHER, location)
            if cached_weather is not None:
                return cached_weather
            from plugins_func.functions.get_weather import get_weather
            from plugins_func.register import ActionResponse
            result = get_weather(conn, location=location, lang='zh_CN')
            if isinstance(result, ActionResponse):
                weather_report = result.result
                self.cache_manager.set(self.CacheType.WEATHER, location, weather_report)
                return weather_report
            return '天气信息获取失败'
        except Exception as e:
            self.logger.bind(tag=TAG).error(f'获取天气信息失败: {e}')
            return '天气信息获取失败'

    def update_context_info(self, conn, client_ip: str):
        """同步更新上下文信息"""
        try:
            local_address = self._get_location_info(client_ip)
            self._get_weather_info(conn, local_address)
            self.logger.bind(tag=TAG).info(f'上下文信息更新完成')
        except Exception as e:
            self.logger.bind(tag=TAG).error(f'更新上下文信息失败: {e}')

    def build_enhanced_prompt(self, user_prompt: str, device_id: str, client_ip: str=None) -> str:
        """构建增强的系统提示词"""
        if not self.base_prompt_template:
            return user_prompt
        try:
            today_date, today_weekday, lunar_date = self._get_current_time_info()
            local_address = ''
            weather_info = ''
            if client_ip:
                local_address = self.cache_manager.get(self.CacheType.LOCATION, client_ip) or ''
                if local_address:
                    weather_info = self.cache_manager.get(self.CacheType.WEATHER, local_address) or ''
            template = Template(self.base_prompt_template)
            enhanced_prompt = template.render(base_prompt=user_prompt, current_time='{{current_time}}', today_date=today_date, today_weekday=today_weekday, lunar_date=lunar_date, local_address=local_address, weather_info=weather_info, emojiList=EMOJI_List)
            device_cache_key = f'device_prompt:{device_id}'
            self.cache_manager.set(self.CacheType.DEVICE_PROMPT, device_cache_key, enhanced_prompt)
            self.logger.bind(tag=TAG).info(f'构建增强提示词成功，长度: {len(enhanced_prompt)}')
            return enhanced_prompt
        except Exception as e:
            self.logger.bind(tag=TAG).error(f'构建增强提示词失败: {e}')
            return user_prompt