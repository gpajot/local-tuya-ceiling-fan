from enum import IntEnum
from typing import Dict, Optional, Set

from local_tuya import DeviceConfig, ProtocolConfig
from local_tuya.domoticz import (
    Parameter,
    PluginMetadata,
    UnitManager,
    install_plugin,
    selector_switch_unit,
    switch_unit,
)

from local_tuya_ceiling_fan.device import (
    FanDevice,
    FanDirection,
    FanMode,
    FanSpeed,
    FanState,
)


def _get_metadata() -> PluginMetadata:
    return PluginMetadata(
        name="Tuya Ceiling Fan",
        package="local_tuya_ceiling_fan",
        description={
            "p": [
                {"h2": "Tuya Ceiling Fan"},
                {
                    "h3": "Features",
                    "ul": {
                        "li": [
                            "Control a Tuya ceiling fan over LAN",
                            "Automatically receive new device state (compatible with remote usage)",
                        ]
                    },
                },
                {
                    "h3": "Devices",
                    "ul": {
                        "li": [
                            "Power - Turn the fan on or off",
                            "Speed - Set the speed",
                            "Direction - Set direction (fan is properly stopped before)",
                            "Light - Turn the light on or off",
                            "Mode - Set the operating mode",
                        ]
                    },
                },
            ]
        },
        parameters=(
            Parameter(field="Mode1", label="Included units", default=UnitId.names()),
        ),
    )


class UnitId(IntEnum):
    POWER = 1
    SPEED = 2
    DIRECTION = 3
    LIGHT = 4
    MODE = 5

    @classmethod
    def names(cls) -> str:
        return ",".join(e.name.lower() for e in cls)

    @classmethod
    def included(cls, names: Optional[str]) -> Set["UnitId"]:
        if not names:
            return set(cls)
        included_names = names.split(",")
        return {e for e in cls if e.name.lower() in included_names}


def on_start(
    protocol_config: ProtocolConfig,
    parameters: Dict[str, str],
    manager: UnitManager[FanState],
) -> FanDevice:
    included_units = UnitId.included(parameters.get("Mode1"))
    device = FanDevice(
        config=DeviceConfig(
            protocol=protocol_config,
            debounce_updates=1,
        ),
    )
    if UnitId.POWER in included_units:
        manager.register(
            switch_unit(
                id_=UnitId.POWER,
                name="power",
                image=9,
                command_func=device.switch,
            ),
            lambda s: s.power,
        )
    else:
        manager.remove(UnitId.POWER)
    if UnitId.SPEED in included_units:
        manager.register(
            selector_switch_unit(
                id_=UnitId.SPEED,
                name="speed",
                image=7,
                enum=FanSpeed,
                command_func=device.set_speed,
            ),
            lambda s: s.speed,
        )
    else:
        manager.remove(UnitId.SPEED)
    if UnitId.DIRECTION in included_units:
        manager.register(
            selector_switch_unit(
                id_=UnitId.DIRECTION,
                name="direction",
                image=7,
                enum=FanDirection,
                command_func=device.set_direction,
            ),
            lambda s: s.direction,
        )
    else:
        manager.remove(UnitId.DIRECTION)
    if UnitId.LIGHT in included_units:
        manager.register(
            switch_unit(
                id_=UnitId.LIGHT,
                name="light",
                image=0,
                command_func=device.switch_light,
            ),
            lambda s: s.light,
        )
    else:
        manager.remove(UnitId.LIGHT)
    if UnitId.MODE in included_units:
        manager.register(
            selector_switch_unit(
                id_=UnitId.MODE,
                name="mode",
                image=19,
                enum=FanMode,
                command_func=device.set_mode,
            ),
            lambda s: s.mode,
        )
    else:
        manager.remove(UnitId.MODE)
    return device


if __name__ == "__main__":
    install_plugin(
        _get_metadata(),
        on_start,
        "local_tuya_ceiling_fan.domoticz.install",
    )
