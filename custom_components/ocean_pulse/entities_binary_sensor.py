"""All binary_sensor entities."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)

from . import OceanPulseBinarySensorEntityDescription as BinarySensorEntityDesc

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    # Doors
    BinarySensorEntityDesc(
        key="DOOR_FL_OPEN",
        name="Door front left",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="DOOR_FR_OPEN",
        name="Door front right",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="DOOR_RL_OPEN",
        name="Door rear left",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="DOOR_RR_OPEN",
        name="Door rear right",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="TRUNK_OPEN",
        name="Trunk",
        icon="mdi:car-back",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data, key: data[key],
    ),
    # Locks
    BinarySensorEntityDesc(
        key="LOCK_STATUS",
        name="Lock status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data, key: data[key],
    ),
    # Climate
    BinarySensorEntityDesc(
        key="CLIMATE_ON",
        name="Climate",
        icon="mdi:fan",
        device_class=BinarySensorDeviceClass.RUNNING,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="AC_AUTO",
        name="AC auto",
        icon="mdi:air-conditioner",
        device_class=None,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="RECIRCULATION",
        name="Recirculation",
        icon="mdi:air-filter",
        device_class=None,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="FRONT_DEFROST",
        name="Front defrost",
        icon="mdi:car-defrost-front",
        device_class=BinarySensorDeviceClass.HEAT,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="REAR_DEFROST",
        name="Rear defrost",
        icon="mdi:car-defrost-rear",
        device_class=BinarySensorDeviceClass.HEAT,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="STEERING_WHEEL_HEAT",
        name="Steering wheel heat",
        icon="mdi:steering",
        device_class=BinarySensorDeviceClass.HEAT,
        value=lambda data, key: data[key],
    ),
    # Charging
    BinarySensorEntityDesc(
        key="CHARGING",
        name="Charging",
        icon="mdi:ev-plug-type2",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="AC_CHARGE_LAMP",
        name="AC charge lamp",
        icon="mdi:ev-plug-type2",
        device_class=BinarySensorDeviceClass.PLUG,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="DC_CHARGE_LAMP",
        name="DC charge lamp",
        icon="mdi:ev-plug-ccs2",
        device_class=BinarySensorDeviceClass.PLUG,
        value=lambda data, key: data[key],
    ),
    # Connectivity
    BinarySensorEntityDesc(
        key="SCU_CONNECTED",
        name="SCU connected",
        icon="mdi:car-connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value=lambda data, key: data[key],
    ),
    BinarySensorEntityDesc(
        key="SYNC_ON",
        name="Sync",
        icon="mdi:sync",
        device_class=BinarySensorDeviceClass.RUNNING,
        value=lambda data, key: data[key],
    ),
)
