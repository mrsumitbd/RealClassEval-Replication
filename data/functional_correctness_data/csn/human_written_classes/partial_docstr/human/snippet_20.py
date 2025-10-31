from typing import Any, Dict, List, Optional
import dataclasses

@dataclasses.dataclass
class BuildConfiguration:
    """Configurations use when building libxgboost"""
    hide_cxx_symbols: bool = True
    use_openmp: bool = True
    use_cuda: bool = False
    use_nccl: bool = False
    use_dlopen_nccl: bool = False
    plugin_federated: bool = False
    plugin_rmm: bool = False
    use_system_libxgboost: bool = False

    def _set_config_setting(self, config_settings: Dict[str, Any]) -> None:
        for field_name in config_settings:
            setattr(self, field_name, config_settings[field_name].lower() in ['true', '1', 'on'])

    def update(self, config_settings: Optional[Dict[str, Any]]) -> None:
        """Parse config_settings from Pip (or other PEP 517 frontend)"""
        if config_settings is not None:
            self._set_config_setting(config_settings)

    def get_cmake_args(self) -> List[str]:
        """Convert build configuration to CMake args"""
        cmake_args = []
        for field_name in [x.name for x in dataclasses.fields(self)]:
            if field_name in ['use_system_libxgboost']:
                continue
            cmake_option = field_name.upper()
            cmake_value = 'ON' if getattr(self, field_name) is True else 'OFF'
            cmake_args.append(f'-D{cmake_option}={cmake_value}')
        return cmake_args