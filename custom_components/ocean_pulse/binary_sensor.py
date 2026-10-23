"""Ocean Pulse component binary sensors."""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import (
    OceanPulseBaseEntity,
    OceanPulseBinarySensorEntityDescription,
    OceanPulseCoordinator,
)
from .const import DOMAIN
from .entities_binary_sensor import BINARY_SENSORS

_LOGGER = logging.getLogger(__name__)


class OceanPulseBinarySensor(
    OceanPulseBaseEntity, CoordinatorEntity, BinarySensorEntity
):
    """Sensor used by all Fisker entities, inherits from CoordinatorEntity."""

    def __init__(
        self,
        coordinator: OceanPulseCoordinator,
        sensor: OceanPulseBinarySensorEntityDescription,
    ) -> None:
        """Initialize Ocean Pulse vehicle sensor."""
        super().__init__(coordinator, sensor.key)

        self.vin = coordinator.vin
        self.entity_description: OceanPulseBinarySensorEntityDescription = sensor
        self._attr_unique_id = f"{coordinator.vin}_{sensor.key}"
        self._attr_name = f"{coordinator.alias} {sensor.name}"

        _LOGGER.info(self._attr_unique_id)

    @property
    def icon(self):
        return self.entity_description.icon

    @property
    def available(self) -> bool:
        """Return True if the coordinator succeeded and the value exists."""
        return (
            super().available
            and self.coordinator.data.get(self.entity_description.key) is not None
        )

    @property
    def is_on(self) -> bool:
        """Return the binary sensor state."""
        return self.entity_description.value_fn(
            self.coordinator.data[self.entity_description.key]
        )

    @property
    def should_poll(self):
        return False


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.debug("Setup sensors")

    coordinator: OceanPulseCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OceanPulseBinarySensor(coordinator, description)  # New sensor entity
        for description in BINARY_SENSORS  # Loops the list
        if description.key in coordinator.data  # IF there's data for the sensor
    )
