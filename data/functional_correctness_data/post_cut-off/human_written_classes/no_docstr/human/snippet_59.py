import flet as ft

class NavigationSidebar:

    def __init__(self, app):
        self.app = app
        self.control_groups = []
        self.selected_control_group = None
        self.app.language_manager.add_observer(self)
        self._ = {}
        self.load()

    def load(self):
        self._ = self.app.language_manager.language.get('sidebar')
        self.control_groups = [ControlGroup(icon=ft.Icons.HOME, label=self._['home'], index=0, name='home', selected_icon=ft.Icons.HOME), ControlGroup(icon=ft.Icons.DASHBOARD, label=self._['recordings'], index=1, name='recordings', selected_icon=ft.Icons.DASHBOARD_ROUNDED), ControlGroup(icon=ft.Icons.SETTINGS, label=self._['settings'], index=2, name='settings', selected_icon=ft.Icons.SETTINGS), ControlGroup(icon=ft.Icons.DRIVE_FILE_MOVE, label=self._['storage'], index=3, name='storage', selected_icon=ft.Icons.DRIVE_FILE_MOVE_OUTLINE), ControlGroup(icon=ft.Icons.INFO, label=self._['about'], index=4, name='about', selected_icon=ft.Icons.INFO)]
        self.selected_control_group = self.control_groups[0]