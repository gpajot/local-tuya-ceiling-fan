import asyncio
import sys

import pytest
from local_tuya import Device, DeviceConfig

from local_tuya_ceiling_fan.device import (
    FanDataPoint,
    FanDevice,
    FanDirection,
    FanMode,
    FanSpeed,
    FanState,
)


def test_load_state():
    assert FanState.load(
        {
            FanDataPoint.POWER: True,
            FanDataPoint.SPEED: "2",
            FanDataPoint.DIRECTION: "forward",
            FanDataPoint.LIGHT: False,
            FanDataPoint.MODE: "sleep",
        }
    ) == FanState(
        power=True,
        speed=FanSpeed.L2,
        direction=FanDirection.FORWARD,
        light=False,
        mode=FanMode.SLEEP,
    )


@pytest.mark.skipif(
    sys.version_info < (3, 8),
    reason="requires python3.8 or higher for AsyncMock",
)
async def test_direction_change_lock(mocker):
    base_device = mocker.Mock(spec=Device)
    mocker.patch(
        "local_tuya_ceiling_fan.device.Device.__init__",
    )
    mocker.patch("local_tuya_ceiling_fan.device.Device", return_value=base_device)
    config = mocker.Mock(spec=DeviceConfig)
    config.confirm_timeout = 1
    device = FanDevice(config, change_direction_wait_safety=0.01)
    state = FanState(
        power=True,
        speed=FanSpeed.L1,
        direction=FanDirection.FORWARD,
        light=False,
        mode=FanMode.NORMAL,
    )
    mocker.patch.object(device, "_state", return_value=state)
    update = mocker.patch.object(device, "_update")

    change_direction = asyncio.create_task(device.set_direction(FanDirection.REVERSE))
    turn_off = asyncio.create_task(device.switch(False))
    await asyncio.gather(change_direction, turn_off)

    assert update.call_count == 3
    update.assert_has_calls(
        (
            (({FanDataPoint.POWER: False},), {}),
            (({FanDataPoint.POWER: True, FanDataPoint.DIRECTION: "reverse"},), {}),
            (({FanDataPoint.POWER: False},), {}),
        ),
    )
