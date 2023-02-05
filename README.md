# local-tuya-ceiling-fan
Control a Tuya Ceiling fan over LAN.

## Usage
See [local tuya requirements](https://github.com/gpajot/local-tuya#requirements) first to find device information.

Example usage:
```python
from local_tuya import DeviceConfig, ProtocolConfig
from local_tuya_ceiling_fan import FanDevice, FanSpeed


async with FanDevice(DeviceConfig(ProtocolConfig("{id}", "{address}", b"{key}"))) as device:
    await device.switch(True)
    await device.set_speec(FanSpeed.L2)
    await device.switch(False)
```

> 💡 There is a safety mechanism that turns off the fan and waits 30s before changing the direction.

## Domoticz plugin
The plugin requires having fetched device information using instructions above.
Make sure to read [plugin instructions](https://www.domoticz.com/wiki/Using_Python_plugins) first.
> 💡 The Domoticz version should be `2022.1` or higher.

```shell
python -m pip install local-tuya-ceiling-fan
python -m local_tuya_ceiling_fan.domoticz.install
```
Domoticz path defaults to `~/domoticz` but you can pass a `-p` option to the second command to change that:
```shell
python -m local_tuya_ceiling_fan.domoticz.install -p /some/other/path
```

Restart Domoticz and create a new Hardware using `Tuya Ceiling Fan`. Fill in device information and add.
The hardware will create up to 5 devices to control the fan (all prefixed with hardware name):
- `power`: turn the fan on or off
- `speed`: set the speed
- `direction`: set direction
- `light`: turn the light on or off
- `mode`: set the operating mode

- You can customize the devices you want added in the hardware page.
All device names and levels van be changed once added as only IDs are used internally.
