"""Ocean Pulse component buttons."""

from homeassistant.helpers.entity import EntityDescription

from . import OceanPulseButtonEntityDescription

BUTTON_ENTITIES: list[EntityDescription] = [
    OceanPulseButtonEntityDescription(
        key="doors_unlock",
        name="Unlock Doors",
        translation_key="doors_unlock",
        icon="mdi:car-door-lock-open",
        command="PKC_UNLOCK",
    ),
    OceanPulseButtonEntityDescription(
        key="doors_lock",
        name="Lock Doors",
        translation_key="doors_lock",
        icon="mdi:car-door-lock",
        command="PKC_LOCK",
    ),
    OceanPulseButtonEntityDescription(
        key="trunk_activate",
        name="Activate Trunk",
        translation_key="trunk_activate",
        icon="mdi:car-back",
        command="PKC_TRUNK_ACTIVATE",
    ),
    OceanPulseButtonEntityDescription(
        key="cabin_temperature_15",
        name="Cabin climate (15 min)",
        translation_key="cabin_temperature_15",
        icon="mdi:air-conditioner",
        command="PKC_CLIMATE_ON",
        command_data={"durationMinutes": 15},
    ),
    OceanPulseButtonEntityDescription(
        key="cabin_climate_off",
        name="Cabin climate off",
        translation_key="cabin_climate_off",
        icon="mdi:air-conditioner",
        command="PKC_CLIMATE_OFF",
    ),
]
