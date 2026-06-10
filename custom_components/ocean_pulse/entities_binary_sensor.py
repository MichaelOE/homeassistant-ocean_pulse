"""All binary_sensor entities."""

from homeassistant.components.sensor import SensorEntityDescription

from . import OceanPulseSensorEntityDescription as SensorEntityDesc

BINARY_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDesc(
        key="DOOR_FL_OPEN",
        name="Door front left",
        icon="mdi:car-door",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="DOOR_FR_OPEN",
        name="Door front right",
        icon="mdi:car-door",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="DOOR_RL_OPEN",
        name="Door rear left",
        icon="mdi:car-door",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="DOOR_RR_OPEN",
        name="Door rear right",
        icon="mdi:car-door",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="TRUNK_OPEN",
        name="Trunk",
        icon="mdi:car-back",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="LOCK_STATUS",
        name="Lock status",
        icon="mdi:car-door-lock",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="STEERING_WHEEL_HEAT",
        name="Steering wheel heat",
        icon="mdi:steering",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="CLIMATE_ON",
        name="Climate",
        icon="mdi:fan",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="FRONT_DEFROST",
        name="Front defrost",
        icon="mdi:car-defrost-front",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="REAR_DEFROST",
        name="Rear defrost",
        icon="mdi:car-defrost-rear",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="SCU_CONNECTED",
        name="SCU connected",
        icon="mdi:car-connected",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
    SensorEntityDesc(
        key="SYNC_ON",
        name="Sync",
        icon="mdi:sync",
        device_class=None,
        native_unit_of_measurement=None,
        value=lambda data, key: data[key],
    ),
)
