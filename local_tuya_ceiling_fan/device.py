import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional

from local_tuya import DataPoint, Device, DeviceConfig, State, Values


class FanDataPoint(DataPoint):
    POWER = "1"
    SPEED = "3"
    DIRECTION = "4"
    LIGHT = "9"
    MODE = "102"


class FanSpeed(str, Enum):
    L1 = "1"
    L2 = "2"
    L3 = "3"
    L4 = "4"
    L5 = "5"
    L6 = "6"


class FanDirection(str, Enum):
    FORWARD = "forward"
    REVERSE = "reverse"


class FanMode(str, Enum):
    NORMAL = "normal"
    SLEEP = "sleep"
    NATURE = "nature"
    TEMP = "temprature"  # Typo on device.


@dataclass
class FanState(State):
    power: bool
    speed: FanSpeed
    direction: FanDirection
    light: bool
    mode: FanMode

    @classmethod
    def load(cls, values: Values) -> "FanState":
        return cls(
            power=bool(values[FanDataPoint.POWER]),
            speed=FanSpeed(values[FanDataPoint.SPEED]),
            direction=FanDirection(values[FanDataPoint.DIRECTION]),
            light=bool(values[FanDataPoint.LIGHT]),
            mode=FanMode(values[FanDataPoint.MODE]),
        )


class FanDevice(Device[FanState]):
    def __init__(
        self,
        config: DeviceConfig,
        state_updated_callback: Optional[Callable[[FanState], Any]] = None,
        # Seconds to wait until the fan stops before changing direction.
        change_direction_wait_safety: float = 30,
    ):
        super().__init__(config, FanState.load, state_updated_callback)
        # Since the direction needs to be changed while fan is fully stopped,
        # add this protection to be sure.
        self._change_direction_wait_safety = change_direction_wait_safety
        self._can_change_direction = config.confirm_timeout > 0
        self._direction_lock = asyncio.Lock()

    async def switch(self, status: bool) -> None:
        async with self._direction_lock:
            await self._update({FanDataPoint.POWER: status})

    async def set_speed(self, speed: FanSpeed) -> None:
        """Set speed."""
        await self._update({FanDataPoint.SPEED: speed.value})

    async def set_direction(self, direction: FanDirection) -> None:
        """Set flow direction."""
        if self._can_change_direction:
            async with self._direction_lock:
                initial_power = (await self._state()).power
                if initial_power:
                    await self._update({FanDataPoint.POWER: False})
                # Let the fan stop.
                await asyncio.sleep(self._change_direction_wait_safety)
                await self._update(
                    {
                        FanDataPoint.DIRECTION: direction.value,
                        FanDataPoint.POWER: initial_power,
                    }
                )

    async def switch_light(self, status: bool) -> None:
        """Set operating mode."""
        await self._update({FanDataPoint.LIGHT: status})

    async def set_mode(self, mode: FanMode) -> None:
        """Set operating mode."""
        await self._update({FanDataPoint.MODE: mode.value})
