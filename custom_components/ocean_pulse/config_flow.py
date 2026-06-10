"""Config flow for Ocean Pulse integration."""

from __future__ import annotations

import logging
from typing import Any
from unittest import result

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ALIAS
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import (
    OceanPulseAPI,
    RequestConnectionError,
    RequestError,
    RequestTimeoutError,
)
from .const import CONF_BASE_URL, CONF_PAIRING_CODE, DOMAIN, URL_BASE

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_PAIRING_CODE): str})
STEP_ALIAS_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ALIAS): str,
    }
)


async def validate_pairing(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the pairing code and return device link data."""
    api = OceanPulseAPI()
    try:
        result = await api.redeem_pairing_code(data[CONF_PAIRING_CODE])
    except RequestError as ex:
        ### FOR TEST only - remove when actual API is available
        return {
            "vin": "OC1234567890ABCDE",
            "device_id": "d7f3a1b2-4e5c-4d6e-8f9a-0b1c2d3e4f5a",
            "car_device_id": "c9e2b3a4-5f6d-4e7f-9a0b-1c2d3e4f5a6b",
            "api_base_url": "https://www.oceanlinkpulse.com",
            "profile_id": 42,
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkN2YzYTFiMiIsImV4cCI6OTk5OTk5OTk5OX0.placeholder",
            "refresh_token": "rt_9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c",
        }

        if ex.error_code in (404, 410):
            raise InvalidPairingCode from ex
        raise CannotConnect from ex
    except (RequestConnectionError, RequestTimeoutError) as ex:
        raise CannotConnect from ex2

    if not isinstance(result, dict) or "vin" not in result:
        raise InvalidPairingCode

    return result


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ocean Pulse."""

    VERSION = 1

    def __init__(self) -> None:
        super().__init__()
        self._device_data: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                device_data = await validate_pairing(self.hass, user_input)
                self._device_data = device_data
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidPairingCode:
                errors["base"] = "invalid_pairing_code"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(self._device_data["vin"])
                self._abort_if_unique_id_configured()
                return await self.async_step_alias()

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_alias(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the alias step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                self._device_data[CONF_ALIAS] = user_input[CONF_ALIAS]
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"{user_input[CONF_ALIAS]} ({self._device_data['vin']})",
                    data=self._device_data,
                )

        return self.async_show_form(
            step_id="alias", data_schema=STEP_ALIAS_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidPairingCode(HomeAssistantError):
    """Error to indicate an invalid or expired pairing code."""
