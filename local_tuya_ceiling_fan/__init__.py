import logging

from local_tuya_ceiling_fan.device import (
    FanDevice,
    FanDirection,
    FanMode,
    FanSpeed,
    FanState,
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
