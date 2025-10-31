from src.common.data_models.database_data_model import DatabaseMessages
from typing import Dict, Optional, Type
from src.chat.message_receive.chat_stream import ChatStream
from src.plugin_system.base.component_types import ComponentType, ActionInfo
from src.plugin_system.core.component_registry import component_registry
from src.plugin_system.base.base_action import BaseAction

class ActionManager:
    """
    动作管理器，用于管理各种类型的动作

    现在统一使用新插件系统，简化了原有的新旧兼容逻辑。
    """

    def __init__(self):
        """初始化动作管理器"""
        self._using_actions: Dict[str, ActionInfo] = {}
        self._using_actions = component_registry.get_default_actions()

    def create_action(self, action_name: str, action_data: dict, reasoning: str, cycle_timers: dict, thinking_id: str, chat_stream: ChatStream, log_prefix: str, shutting_down: bool=False, action_message: Optional[DatabaseMessages]=None) -> Optional[BaseAction]:
        """
        创建动作处理器实例

        Args:
            action_name: 动作名称
            action_data: 动作数据
            reasoning: 执行理由
            cycle_timers: 计时器字典
            thinking_id: 思考ID
            chat_stream: 聊天流
            log_prefix: 日志前缀
            shutting_down: 是否正在关闭

        Returns:
            Optional[BaseAction]: 创建的动作处理器实例，如果动作名称未注册则返回None
        """
        try:
            component_class: Type[BaseAction] = component_registry.get_component_class(action_name, ComponentType.ACTION)
            if not component_class:
                logger.warning(f'{log_prefix} 未找到Action组件: {action_name}')
                return None
            component_info = component_registry.get_component_info(action_name, ComponentType.ACTION)
            if not component_info:
                logger.warning(f'{log_prefix} 未找到Action组件信息: {action_name}')
                return None
            plugin_config = component_registry.get_plugin_config(component_info.plugin_name)
            instance = component_class(action_data=action_data, reasoning=reasoning, cycle_timers=cycle_timers, thinking_id=thinking_id, chat_stream=chat_stream, log_prefix=log_prefix, shutting_down=shutting_down, plugin_config=plugin_config, action_message=action_message)
            logger.debug(f'创建Action实例成功: {action_name}')
            return instance
        except Exception as e:
            logger.error(f'创建Action实例失败 {action_name}: {e}')
            import traceback
            logger.error(traceback.format_exc())
            return None

    def get_using_actions(self) -> Dict[str, ActionInfo]:
        """获取当前正在使用的动作集合"""
        return self._using_actions.copy()

    def remove_action_from_using(self, action_name: str) -> bool:
        """
        从当前使用的动作集中移除指定动作

        Args:
            action_name: 动作名称

        Returns:
            bool: 移除是否成功
        """
        if action_name not in self._using_actions:
            logger.warning(f'移除失败: 动作 {action_name} 不在当前使用的动作集中')
            return False
        del self._using_actions[action_name]
        logger.debug(f'已从使用集中移除动作 {action_name}')
        return True

    def restore_actions(self) -> None:
        """恢复到默认动作集"""
        actions_to_restore = list(self._using_actions.keys())
        self._using_actions = component_registry.get_default_actions()
        logger.debug(f'恢复动作集: 从 {actions_to_restore} 恢复到默认动作集 {list(self._using_actions.keys())}')