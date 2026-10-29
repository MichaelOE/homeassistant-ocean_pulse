"""All binary_sensor entities."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory

from . import OceanPulseBinarySensorEntityDescription as BinarySensorEntityDesc

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    # Doors
    BinarySensorEntityDesc(
        key="DOOR_FL_OPEN",
        name="Front left door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDesc(
        key="DOOR_FR_OPEN",
        name="Front right door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDesc(
        key="DOOR_RL_OPEN",
        name="Rear left door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDesc(
        key="DOOR_RR_OPEN",
        name="Rear right door",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDesc(
        key="TRUNK_OPEN",
        name="Trunk",
        icon="mdi:car-back",
        device_class=BinarySensorDeviceClass.OPENING,
    ),
    # Locks
    BinarySensorEntityDesc(
        key="LOCK_STATUS",
        name="Lock status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value_fn=lambda value: str(value).lower() == "unlocked",
    ),
    # Climate
    BinarySensorEntityDesc(
        key="CLIMATE_ON",
        name="Climate",
        icon="mdi:fan",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
    BinarySensorEntityDesc(
        key="AC_AUTO",
        name="AC auto",
        icon="mdi:air-conditioner",
        device_class=None,
    ),
    BinarySensorEntityDesc(
        key="RECIRCULATION",
        name="Recirculation",
        icon="mdi:air-filter",
        device_class=None,
    ),
    BinarySensorEntityDesc(
        key="FRONT_DEFROST",
        name="Front defrost",
        icon="mdi:car-defrost-front",
        device_class=BinarySensorDeviceClass.HEAT,
    ),
    BinarySensorEntityDesc(
        key="REAR_DEFROST",
        name="Rear defrost",
        icon="mdi:car-defrost-rear",
        device_class=BinarySensorDeviceClass.HEAT,
    ),
    BinarySensorEntityDesc(
        key="STEERING_WHEEL_HEAT",
        name="Steering wheel heat",
        icon="mdi:steering",
        device_class=BinarySensorDeviceClass.HEAT,
    ),
    # Connectivity
    BinarySensorEntityDesc(
        key="CAR_ASLEEP",
        name="Car asleep",
        icon="mdi:car-connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    BinarySensorEntityDesc(
        key="SCU_CONNECTED",
        name="SCU connected",
        icon="mdi:car-connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BinarySensorEntityDesc(
        key="SYNC_ON",
        name="Sync",
        icon="mdi:sync",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)
