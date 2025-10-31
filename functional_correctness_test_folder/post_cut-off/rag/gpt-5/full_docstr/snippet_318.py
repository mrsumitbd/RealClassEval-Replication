
# In a plugin method:
settings = self.api.app_context.settings
server_manager = self.api.app_context.manager
all_servers = server_manager.get_all_servers()
