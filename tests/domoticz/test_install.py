import subprocess
from pathlib import Path

from local_tuya_ceiling_fan.domoticz.install import UnitId, _get_metadata


def test_unit_id():
    assert UnitId.names() == "power,speed,direction,light,mode"

    assert UnitId.included(UnitId.names()) == set(UnitId)

    assert UnitId.included("power,speed") == {UnitId.POWER, UnitId.SPEED}


def test_metadata():
    test_file = Path(__file__).parent / "test_metadata.xml"
    version = subprocess.check_output(
        ["poetry", "version", "--short"], encoding="utf-8"
    ).strip()
    assert _get_metadata().definition() == test_file.read_text().format(version=version)
