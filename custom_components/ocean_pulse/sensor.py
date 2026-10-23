"""Ocean Pulse component sensors."""

from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import (
    OceanPulseBaseEntity,
    OceanPulseCoordinator,
    OceanPulseSensorEntityDescription,
)
from .const import DOMAIN
from .entities_sensor import SENSORS_DIGITAL_TWIN

_LOGGER = logging.getLogger(__name__)


class OceanPulseSensor(OceanPulseBaseEntity, CoordinatorEntity, SensorEntity):
    """Sensor entity for Ocean Pulse."""

    entity_description: OceanPulseSensorEntityDescription

    def __init__(
        self,
        coordinator: OceanPulseCoordinator,
        sensor: OceanPulseSensorEntityDescription,
    ) -> None:
        """Initialize Ocean Pulse sensor."""
        super().__init__(coordinator, sensor.key)

        self._coordinator = coordinator
        self.vin = coordinator.vin
        self.entity_description = sensor
        self._attr_unique_id = f"{coordinator.vin}_{sensor.key}"
        self._attr_name = f"{coordinator.alias} {sensor.name}"

    @property
    def available(self) -> bool:
        """Return True if the coordinator succeeded and the value exists."""
        return (
            super().available
            and self.coordinator.data.get(self.entity_description.key) is not None
        )

    @property
    def native_value(self) -> StateType | datetime:
        """Return the sensor value."""
        return self.entity_description.value_fn(
            self.coordinator.data[self.entity_description.key]
        )

    @property
    def extra_state_attributes(self):
        return None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    _LOGGER.debug("Setup sensors")

    coordinator: OceanPulseCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OceanPulseSensor(coordinator, description)  # New sensor entity
        for description in SENSORS_DIGITAL_TWIN  # Loops the list
        if description.key in coordinator.data  # IF there's data for the sensor
    )

    ent_reg = entity_registry.async_get(hass)
    for key in ("lat", "lon"):
        if entity_id := ent_reg.async_get_entity_id(
            "sensor", DOMAIN, f"{coordinator.vin}_{key}"
        ):
            ent_reg.async_remove(entity_id)
