from typing import Dict

from local_tuya import DeviceConfig, ProtocolConfig
from local_tuya.domoticz import (
    PluginMetadata,
    UnitId,
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
                            "power - Turn the fan on or off",
                            "speed - Set the speed",
                            "direction - Set direction (fan is properly stopped before)",
                            "light - Turn the light on or off",
                            "mode - Set the operating mode",
                        ]
                    },
                },
            ]
        },
    )


class FanUnitId(UnitId):
    POWER = 1
    SPEED = 2
    DIRECTION = 3
    LIGHT = 4
    MODE = 5


def on_start(
    protocol_config: ProtocolConfig,
    _: Dict[str, str],
    manager: UnitManager[FanState],
) -> FanDevice:
    device = FanDevice(
        config=DeviceConfig(
            protocol=protocol_config,
        ),
    )
    manager.register(
        switch_unit(
            id_=FanUnitId.POWER,
            name="power",
            image=9,
            command_func=device.switch,
        ),
        lambda s: s.power,
    )
    manager.register(
        selector_switch_unit(
            id_=FanUnitId.SPEED,
            name="speed",
            image=7,
            enum=FanSpeed,
            command_func=device.set_speed,
        ),
        lambda s: s.speed,
    )
    manager.register(
        selector_switch_unit(
            id_=FanUnitId.DIRECTION,
            name="direction",
            image=7,
            enum=FanDirection,
            command_func=device.set_direction,
        ),
        lambda s: s.direction,
    )
    manager.register(
        switch_unit(
            id_=FanUnitId.LIGHT,
            name="light",
            image=0,
            command_func=device.switch_light,
        ),
        lambda s: s.light,
    )
    manager.register(
        selector_switch_unit(
            id_=FanUnitId.MODE,
            name="mode",
            image=19,
            enum=FanMode,
            command_func=device.set_mode,
        ),
        lambda s: s.mode,
    )
    return device


if __name__ == "__main__":
    install_plugin(
        _get_metadata(),
        on_start,
        "local_tuya_ceiling_fan.domoticz.install",
        FanUnitId,
    )
