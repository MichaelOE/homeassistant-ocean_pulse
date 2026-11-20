"""All sensor entities."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfEnergyDistance,
    UnitOfLength,
    UnitOfPower,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)

from . import OceanPulseSensorEntityDescription as SensorEntityDesc
from .const import CHARGING_LAMP_STATES, CHARGING_STATES, CLIMATE_CONTROL_SEAT_HEAT


def _trip_value(field: str) -> Callable[[Any], float | None]:
    """Return a function that reads a numeric field from a trip payload."""

    def _value(trip: Any) -> float | None:
        # The trip payload is undocumented, so anything unexpected is unknown
        if not isinstance(trip, dict) or not isinstance(
            value := trip.get(field), int | float
        ):
            return None
        return value

    return _value


def _trip_started_at(trip: Any) -> datetime | None:
    """Return when the trip started."""
    if (started_ms := _trip_value("startedAtMs")(trip)) is None:
        return None
    return datetime.fromtimestamp(started_ms / 1000, UTC)


_TRIP_TIMESTAMP_FIELDS = {"startedAtMs": "started_at", "pausedAtMs": "paused_at"}
_TRIP_DURATION_FIELDS = {"drivingMs": "driving_time", "parkedMs": "parked_time"}


def _trip_attributes(trip: Any) -> dict[str, Any]:
    """Expose the current_trip payload with readable times while it is experimental."""
    if not isinstance(trip, dict):
        return {"raw": trip}
    attrs = {}
    for field, value in trip.items():
        if not isinstance(value, int | float):
            attrs[field] = value
        elif name := _TRIP_TIMESTAMP_FIELDS.get(field):
            attrs[name] = datetime.fromtimestamp(value / 1000, UTC)
        elif name := _TRIP_DURATION_FIELDS.get(field):
            attrs[name] = str(timedelta(seconds=round(value / 1000)))
        else:
            attrs[field] = value
    return attrs


SENSORS_DIGITAL_TWIN: tuple[SensorEntityDescription, ...] = (
    # Battery / Range
    SensorEntityDesc(
        key="SOC",
        name="HV battery",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDesc(
        key="SOH",
        name="HV battery health",
        icon="mdi:battery-heart",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDesc(
        key="HV_CAP",
        name="HV battery capacity",
        icon="mdi:car-electric",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    SensorEntityDesc(
        key="INSTANT_POWER_KW",
        name="HV battery power",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    SensorEntityDesc(
        key="INSTANT_POWER_KW_CHARGE",
        source_key="INSTANT_POWER_KW",
        value_fn=lambda v: None if v is None else max(v, 0),
        name="HV battery charge power",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    SensorEntityDesc(
        key="INSTANT_POWER_KW_DISCHARGE",
        source_key="INSTANT_POWER_KW",
        value_fn=lambda v: None if v is None else max(-v, 0),
        name="HV battery discharge power",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    SensorEntityDesc(
        key="RANGE",
        name="Range",
        icon="mdi:map-marker-distance",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    SensorEntityDesc(
        key="MILEAGE",
        name="Odometer",
        icon="mdi:counter",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        suggested_display_precision=1,
    ),
    SensorEntityDesc(
        key="current_trip",
        name="Current trip",
        icon="mdi:map-marker-path",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=_trip_value("distanceKm"),
        attrs_fn=_trip_attributes,
    ),
    # Previous trip: finished trip values, suited for long-term statistics
    SensorEntityDesc(
        key="previous_trip_distance",
        source_key="previous_trip",
        name="Previous trip distance",
        icon="mdi:map-marker-path",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=_trip_value("distanceKm"),
    ),
    SensorEntityDesc(
        key="previous_trip_energy",
        source_key="previous_trip",
        name="Previous trip energy",
        icon="mdi:lightning-bolt",
        # The energy device class does not allow the measurement state class
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=_trip_value("energyKwh"),
    ),
    SensorEntityDesc(
        key="previous_trip_regen",
        source_key="previous_trip",
        name="Previous trip regeneration",
        icon="mdi:battery-charging",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=_trip_value("regenKwh"),
    ),
    SensorEntityDesc(
        key="previous_trip_efficiency",
        source_key="previous_trip",
        name="Previous trip efficiency",
        icon="mdi:leaf",
        device_class=SensorDeviceClass.ENERGY_DISTANCE,
        native_unit_of_measurement=UnitOfEnergyDistance.KM_PER_KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=_trip_value("efficiencyKmPerKwh"),
    ),
    SensorEntityDesc(
        key="previous_trip_avg_speed",
        source_key="previous_trip",
        name="Previous trip average speed",
        icon="mdi:speedometer-medium",
        device_class=SensorDeviceClass.SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=_trip_value("avgSpeedKph"),
    ),
    SensorEntityDesc(
        key="previous_trip_max_speed",
        source_key="previous_trip",
        name="Previous trip max speed",
        icon="mdi:speedometer",
        device_class=SensorDeviceClass.SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=_trip_value("maxSpeedKph"),
    ),
    SensorEntityDesc(
        key="previous_trip_driving_time",
        source_key="previous_trip",
        name="Previous trip driving time",
        icon="mdi:timer-outline",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        suggested_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=_trip_value("drivingMs"),
    ),
    SensorEntityDesc(
        key="previous_trip_parked_time",
        source_key="previous_trip",
        name="Previous trip parked time",
        icon="mdi:timer-pause-outline",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        suggested_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=_trip_value("parkedMs"),
    ),
    SensorEntityDesc(
        key="previous_trip_start",
        source_key="previous_trip",
        name="Previous trip start",
        icon="mdi:clock-start",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=_trip_started_at,
    ),
    SensorEntityDesc(
        key="BATTERY_12V",
        name="12V battery voltage",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        suggested_display_precision=2,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Temperature
    SensorEntityDesc(
        key="AMBIENT_TEMP",
        name="Ambient temperature",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDesc(
        key="OUTDOOR_TEMP",
        name="Outdoor temperature",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDesc(
        key="CABIN_TEMP",
        name="Cabin temperature",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDesc(
        key="DRIVER_TEMP",
        name="Driver temp setpoint",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDesc(
        key="PASS_TEMP",
        name="Passenger temp setpoint",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Seat heat (int 0-4: 0=Unknown, 1=High, 2=Medium, 3=Low, 4=Off)
    SensorEntityDesc(
        key="SEAT_HEAT_DRIVER",
        name="Seat heat driver",
        icon="mdi:car-seat-heater",
        device_class=SensorDeviceClass.ENUM,
        options=[name for name, _icon in CLIMATE_CONTROL_SEAT_HEAT.values()],
        value_fn=lambda value: CLIMATE_CONTROL_SEAT_HEAT[value][0],
    ),
    SensorEntityDesc(
        key="SEAT_HEAT_PASSENGER",
        name="Seat heat passenger",
        icon="mdi:car-seat-heater",
        device_class=SensorDeviceClass.ENUM,
        options=[name for name, _icon in CLIMATE_CONTROL_SEAT_HEAT.values()],
        value_fn=lambda value: CLIMATE_CONTROL_SEAT_HEAT[value][0],
    ),
    SensorEntityDesc(
        key="SEAT_HEAT_REAR_LEFT",
        name="Seat heat rear left",
        icon="mdi:car-seat-heater",
        device_class=SensorDeviceClass.ENUM,
        options=[name for name, _icon in CLIMATE_CONTROL_SEAT_HEAT.values()],
        value_fn=lambda value: CLIMATE_CONTROL_SEAT_HEAT[value][0],
    ),
    SensorEntityDesc(
        key="SEAT_HEAT_REAR_RIGHT",
        name="Seat heat rear right",
        icon="mdi:car-seat-heater",
        device_class=SensorDeviceClass.ENUM,
        options=[name for name, _icon in CLIMATE_CONTROL_SEAT_HEAT.values()],
        value_fn=lambda value: CLIMATE_CONTROL_SEAT_HEAT[value][0],
    ),
    # Climate
    SensorEntityDesc(
        key="CLIMATE_STATE",
        name="Climate state",
        icon="mdi:fan",
    ),
    SensorEntityDesc(
        key="AC_STATE",
        name="Air conditioning state",
        icon="mdi:air-conditioner",
    ),
    SensorEntityDesc(
        key="FAN_SPEED",
        name="Fan speed",
        icon="mdi:fan",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDesc(
        key="RECIRCULATION",
        name="Recirculation",
        icon="mdi:air-filter",
        device_class=None,
    ),
    # Energy/Charging
    SensorEntityDesc(
        key="CHARGING",
        name="Charging",
        icon="mdi:ev-plug-type2",
        options=list(CHARGING_STATES.values()),
        device_class=SensorDeviceClass.ENUM,
        value_fn=lambda v: CHARGING_STATES.get(v) if v is not None else None,
    ),
    SensorEntityDesc(
        key="AC_CHARGE_LAMP",
        name="AC charge lamp",
        icon="mdi:ev-plug-type2",
        options=list(CHARGING_LAMP_STATES.values()),
        device_class=SensorDeviceClass.ENUM,
        value_fn=lambda v: CHARGING_LAMP_STATES.get(v) if v is not None else None,
    ),
    SensorEntityDesc(
        key="DC_CHARGE_LAMP",
        name="DC charge lamp",
        icon="mdi:ev-plug-ccs2",
        options=list(CHARGING_LAMP_STATES.values()),
        device_class=SensorDeviceClass.ENUM,
        value_fn=lambda v: CHARGING_LAMP_STATES.get(v) if v is not None else None,
    ),
    SensorEntityDesc(
        key="AC_CHARGE_LAMP_COLOR",
        name="AC charge lamp color",
        icon="mdi:ev-plug-type2",
    ),
    SensorEntityDesc(
        key="DC_CHARGE_LAMP_COLOR",
        name="DC charge lamp color",
        icon="mdi:ev-plug-ccs2",
    ),
    # General / System
    SensorEntityDesc(
        key="NETWORK_STATE",
        name="Network state",
        icon="mdi:network-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDesc(
        key="CAR_ASLEEP",
        name="Car sleep state",
        icon="mdi:sleep",
        device_class=SensorDeviceClass.ENUM,
        options=["asleep", "awake"],
        value_fn=lambda v: (
            "asleep" if str(v).lower() in ("true", "1", "asleep") else "awake"
        ),
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDesc(
        key="POWER_MODE",
        name="Power mode",
        icon="mdi:power",
    ),
    SensorEntityDesc(
        key="installed_version",
        name="Firmware version",
        icon="mdi:car-info",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDesc(
        key="installed_build",
        name="Firmware build",
        icon="mdi:car-info",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDesc(
        key="last_update",
        name="Last updated",
        icon="mdi:clock-outline",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=datetime.fromisoformat,
    ),
    SensorEntityDesc(
        key="LAST_PARKED_POLL_AT",
        name="Last parked poll",
        icon="mdi:clock-outline",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=datetime.fromisoformat,
    ),
    SensorEntityDesc(
        key="PARKED_POLL_INTERVAL_S",
        name="Parked poll interval",
        icon="mdi:timer-check-outline",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
        suggested_display_precision=0,
    ),
    SensorEntityDesc(
        key="device_name",
        name="Device name",
        icon="mdi:car-info",
        device_class=None,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)
