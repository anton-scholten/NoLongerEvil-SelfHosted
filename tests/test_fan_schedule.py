"""The fan schedule can be set and is reported in the device status."""

from datetime import datetime

from nolongerevil.lib.types import DeviceObject
from nolongerevil.routes.control.command import execute_command
from nolongerevil.routes.control.status import format_device_status

SERIAL = "02AA01AB501203EQ"


async def test_fan_schedule_round_trip(state_service, subscription_manager, device_availability):
    for key in (f"device.{SERIAL}", f"shared.{SERIAL}"):
        await state_service.upsert_object(
            DeviceObject(SERIAL, key, 1, 1000, {"has_fan": True}, datetime.now())
        )
    schedule = {
        "fan_mode": "duty-cycle",
        "fan_duty_cycle": 900,
        "fan_duty_start_time": 8 * 3600,
        "fan_duty_end_time": 22 * 3600,
    }
    await execute_command(
        state_service, subscription_manager, SERIAL, "set_device_setting", schedule
    )
    status = format_device_status(SERIAL, state_service, device_availability)
    assert status["fan_schedule"] == {
        "mode": "duty-cycle",
        "duty_cycle": 900,
        "start": 28800,
        "end": 79200,
    }
