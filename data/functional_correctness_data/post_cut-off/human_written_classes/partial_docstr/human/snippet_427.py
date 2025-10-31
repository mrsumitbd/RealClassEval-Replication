from PySide6.QtGui import QAction
from AgentCrew.modules.llm.model_registry import ModelRegistry
from AgentCrew.modules.agents import AgentManager
from PySide6.QtWidgets import QMenuBar

class MenuBuilder:
    """Builds and manages menus for the chat window."""

    def __init__(self, chat_window):
        from AgentCrew.modules.gui import ChatWindow
        if isinstance(chat_window, ChatWindow):
            self.chat_window = chat_window

    def create_menu_bar(self):
        """Create the application menu bar with Agents, Models, and Settings menus"""
        menu_bar = QMenuBar(self.chat_window)
        menu_bar.setStyleSheet(self.chat_window.style_provider.get_menu_style())
        self.chat_window.setMenuBar(menu_bar)
        self._create_agents_menu(menu_bar)
        self._create_models_menu(menu_bar)
        self._create_settings_menu(menu_bar)

    def update_menu_style(self):
        """Update menu styling when theme changes."""
        menu_bar = self.chat_window.menuBar()
        if menu_bar:
            menu_bar.setStyleSheet(self.chat_window.style_provider.get_menu_style())

    def refresh_agent_menu(self):
        """Refresh the agents menu after configuration changes."""
        menu_bar = self.chat_window.menuBar()
        agents_menu = None
        for action in menu_bar.actions():
            if action.text() == 'Agents':
                agents_menu = action.menu()
                break
        if agents_menu:
            agents_menu.clear()
            agent_manager = AgentManager.get_instance()
            available_agents = agent_manager.agents
            for agent_name in available_agents:
                agent_action = QAction(agent_name, self.chat_window)
                agent_action.triggered.connect(lambda checked, name=agent_name: self.chat_window.command_handler.change_agent(name))
                agents_menu.addAction(agent_action)
            current_agent = agent_manager.get_current_agent()
            if current_agent.name != self.chat_window.message_handler.agent.name:
                self.chat_window.command_handler.change_agent(current_agent.name)

    def _create_agents_menu(self, menu_bar):
        """Create the Agents menu."""
        agents_menu = menu_bar.addMenu('Agents')
        agent_manager = AgentManager.get_instance()
        available_agents = agent_manager.agents
        for agent_name in available_agents:
            agent_action = QAction(agent_name, self.chat_window)
            agent_action.triggered.connect(lambda checked, name=agent_name: self.chat_window.command_handler.change_agent(name))
            agents_menu.addAction(agent_action)

    def _create_models_menu(self, menu_bar):
        """Create the Models menu."""
        models_menu = menu_bar.addMenu('Models')
        model_registry = ModelRegistry.get_instance()
        for provider in model_registry.get_providers():
            provider_menu = models_menu.addMenu(provider.capitalize())
            models = model_registry.get_models_by_provider(provider)
            for model in models:
                model_action = QAction(f'{model.name} ({model.id})', self.chat_window)
                model_action.triggered.connect(lambda checked, model_id=f'{model.provider}/{model.id}': self.chat_window.command_handler.change_model(model_id))
                provider_menu.addAction(model_action)

    def _create_settings_menu(self, menu_bar):
        """Create the Settings menu."""
        settings_menu = menu_bar.addMenu('Settings')
        agents_config_action = QAction('Agents Configuration', self.chat_window)
        agents_config_action.triggered.connect(self.chat_window.command_handler.open_agents_config)
        settings_menu.addAction(agents_config_action)
        mcps_config_action = QAction('MCP Servers Configuration', self.chat_window)
        mcps_config_action.triggered.connect(self.chat_window.command_handler.open_mcps_config)
        settings_menu.addAction(mcps_config_action)
        settings_menu.addSeparator()
        global_settings_config_action = QAction('Global Settings', self.chat_window)
        global_settings_config_action.triggered.connect(self.chat_window.command_handler.open_global_settings_config)
        settings_menu.addAction(global_settings_config_action)