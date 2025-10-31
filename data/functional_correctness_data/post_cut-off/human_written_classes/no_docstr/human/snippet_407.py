from dataclasses import dataclass, field
from typing import ClassVar
from custom_components.solis_cloud_control.utils.safe_converters import safe_convert_power_to_watts, safe_get_float_value

@dataclass(frozen=True)
class InverterInfo:
    ENERGY_STORAGE_CONTROL_DISABLED: ClassVar[str] = '0'
    TOU_V2_MODE: ClassVar[str] = '43605'
    MAX_EXPORT_POWER_DEFAULT: ClassVar[float] = 1000000
    MAX_EXPORT_POWER_STEP_DEFAULT: ClassVar[float] = 100
    MAX_EXPORT_POWER_SCALE_DEFAULT: ClassVar[float] = 1.0
    POWER_LIMIT_DEFAULT: ClassVar[float] = 110.0
    PARALLEL_INVERTER_COUNT_DEFAULT: ClassVar[int] = 1
    PARALLEL_BATTERY_COUNT_DEFAULT: ClassVar[int] = 1
    serial_number: str
    model: str | None
    version: str | None
    machine: str | None
    energy_storage_control: str | None
    smart_support: str | None
    generator_support: str | None
    collector_model: str | None
    power: str | None
    power_unit: str | None
    parallel_number: str | None
    parallel_battery: str | None
    tou_v2_mode: str | None = None

    @property
    def is_string_inverter(self) -> bool:
        return self.energy_storage_control is not None and self.energy_storage_control == self.ENERGY_STORAGE_CONTROL_DISABLED

    @property
    def is_tou_v2_enabled(self) -> bool:
        return self.tou_v2_mode is not None and self.tou_v2_mode == self.TOU_V2_MODE

    @property
    def max_export_power(self) -> float:
        power = safe_convert_power_to_watts(self.power, self.power_unit)
        if power is not None:
            return power * self.parallel_inverter_count
        else:
            return self.MAX_EXPORT_POWER_DEFAULT

    @property
    def max_export_power_scale(self) -> float:
        if self.model and self.model.lower() in ['3315', '3331', '5305']:
            return 0.01
        else:
            return self.MAX_EXPORT_POWER_SCALE_DEFAULT

    @property
    def parallel_inverter_count(self) -> int:
        parallel_inverter_count = safe_get_float_value(self.parallel_number)
        if parallel_inverter_count is None or not parallel_inverter_count.is_integer() or parallel_inverter_count < 1:
            return self.PARALLEL_INVERTER_COUNT_DEFAULT
        else:
            return int(parallel_inverter_count)

    @property
    def parallel_battery_count(self) -> int:
        parallel_battery_count = safe_get_float_value(self.parallel_battery)
        if parallel_battery_count is None or not parallel_battery_count.is_integer() or parallel_battery_count < 0:
            return self.PARALLEL_BATTERY_COUNT_DEFAULT
        else:
            return int(parallel_battery_count) + 1