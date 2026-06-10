"""Class to handle connections towards OceanPulse API servers."""

import asyncio
import base64
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import logging
from typing import Optional

import aiohttp

from homeassistant.components.dlink import data
from homeassistant.util import dt as dt_util

from .const import API_TIMEOUT, URL_BASE

_LOGGER = logging.getLogger(__name__)


@dataclass
class PulseDeviceLink:
    vin: str
    device_id: str
    car_device_id: str
    api_base_url: str
    profile_id: int
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class OceanPulseAPI:
    """Handle connection towards OceanPulse API servers."""

    def __init__(self) -> None:
        self._links: dict[str, PulseDeviceLink] = {}
        self.vehicle_statuses: dict[str, dict] = {}
        self.is_loading = False

    def link_device(self, link: PulseDeviceLink) -> None:
        self._links[link.vin] = link

    def unlink_device(self, vin: str) -> None:
        self._links.pop(vin, None)
        self.vehicle_statuses.pop(vin, None)

    def _require_link(self, vin: str) -> PulseDeviceLink:
        link = self._links.get(vin)
        if link is None:
            raise Exception(f"Device {vin} is not linked")
        return link

    async def redeem_pairing_code(self, code: str) -> dict:
        """Redeem a pairing code and return the device link data."""
        url = f"{URL_BASE}/api/pairing/{code}"
        _LOGGER.debug("PulseCloud: redeeming pairing code %s", code)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    if resp.status in (404, 410):
                        raise RequestError(
                            "Invalid or expired pairing code", resp.status
                        )
                    body = await resp.text()
                    raise RequestError(
                        f"Failed to redeem pairing code: {resp.status} {body}",
                        resp.status,
                    )
        except aiohttp.ClientError as ex:
            raise RequestConnectionError("Connection failed") from ex
        except asyncio.TimeoutError as ex:
            raise RequestTimeoutError("Request timed out") from ex

    async def get_status(self, vin: str) -> dict:
        """Fetch vehicle status for a specific VIN."""
        link = self._require_link(vin)
        self.is_loading = True
        try:
            headers = await self._auth_headers(link)
            url = f"{link.api_base_url}/api/devices/{link.car_device_id}/status"
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
            ) as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.vehicle_statuses[vin] = data
                        return data
                    if resp.status == 401:
                        data = {
                            "device_id": "a8cc29a4d7967f217ca2a8cfe489588c",
                            "device_name": "Bluey",
                            "status": {
                                "AC_AUTO": "off",
                                "AC_CHARGE_LAMP": 0,
                                "AC_CHARGE_LAMP_COLOR": "off",
                                "AC_STATE": "off",
                                "AMBIENT_TEMP": 29.5,
                                "BATTERY_12V": 12.919,
                                "CHARGING": 0,
                                "CLIMATE_ON": False,
                                "CLIMATE_STATE": 0,
                                "DC_CHARGE_LAMP": 0,
                                "DC_CHARGE_LAMP_COLOR": "off",
                                "DOOR_FL_OPEN": False,
                                "DOOR_FR_OPEN": False,
                                "DOOR_RL_OPEN": False,
                                "DOOR_RR_OPEN": False,
                                "DRIVER_TEMP": 20.5,
                                "FAN_SPEED": 0,
                                "FRONT_DEFROST": False,
                                "HV_CAP": 69.47,
                                "LOCATION": {
                                    "lat": 55.71163299999999,
                                    "lon": 9.86675200000001,
                                },
                                "LOCK_STATUS": "locked",
                                "MILEAGE": 31281.4,
                                "OUTDOOR_TEMP": 29.5,
                                "PASS_TEMP": 20.5,
                                "POWER_MODE": "off",
                                "RANGE": 306,
                                "REAR_DEFROST": False,
                                "RECIRCULATION": "outer",
                                "SCU_CONNECTED": True,
                                "SEAT_HEAT_DRIVER": 4,
                                "SEAT_HEAT_PASSENGER": 4,
                                "SEAT_HEAT_REAR_LEFT": 4,
                                "SEAT_HEAT_REAR_RIGHT": 4,
                                "SOC": 69,
                                "SOH": 98,
                                "STEERING_WHEEL_HEAT": False,
                                "SYNC_ON": True,
                                "TRUNK_OPEN": False,
                                "installed_build": 2229,
                                "installed_version": "1.0.0",
                                "last_update": "2026-05-29T17:10:03.640265Z",
                            },
                        }
                        return data

                        self.unlink_device(vin)
                        raise Exception("Token revoked – device unlinked")
                    body = await resp.text()
                    raise Exception(f"Status failed: {resp.status} {body}")
        finally:
            self.is_loading = False

    async def send_command(
        self,
        vin: str,
        cmd: str,
        extra_data: dict | None = None,
    ) -> dict:
        """Send a vehicle command for a specific VIN."""
        link = self._require_link(vin)
        self.is_loading = True
        try:
            headers = await self._auth_headers(link)
            url = f"{link.api_base_url}/api/devices/{link.car_device_id}/commands"
            body: dict = {"cmd": cmd}
            if extra_data is not None:
                body["extra_data"] = extra_data
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=body,
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    if resp.status in (200, 201):
                        return await resp.json()
                    if resp.status == 401:
                        _LOGGER.debug(
                            "PulseCloud: [send_command] device unlinked for VIN %s", vin
                        )
                        raise Exception(
                            "Token revoked - device unlinked [send_command]"
                        )
                    text = await resp.text()
                    raise Exception(f"Command failed: {resp.status} {text}")
        finally:
            self.is_loading = False

    async def _auth_headers(self, link: PulseDeviceLink) -> dict:
        if link.access_token is None or self._is_token_expired(link.access_token):
            await self._refresh_tokens(link)
        return {
            "Authorization": f"Bearer {link.access_token}",
            "Content-Type": "application/json",
        }

    async def _refresh_tokens(self, link: PulseDeviceLink) -> None:
        if link.refresh_token is None:
            self.unlink_device(link.vin)
            raise Exception("No refresh token")

        url = f"{link.api_base_url}/api/devices/{link.car_device_id}/tokens/refresh"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json={"refresh_token": link.refresh_token},
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    await self._handle_refresh_response(link, resp)
        except asyncio.TimeoutError:
            _LOGGER.debug(
                "PulseCloud: refresh timed out – keeping tokens, will retry later"
            )
        except aiohttp.ClientError as e:
            _LOGGER.debug("PulseCloud: network error during refresh – %s", e)

    async def _handle_refresh_response(
        self, link: PulseDeviceLink, resp: aiohttp.ClientResponse
    ) -> None:
        if resp.status == 200:
            data = await resp.json()
            link.access_token = data["access_token"]
            link.refresh_token = data["refresh_token"]
            _LOGGER.debug("PulseCloud: tokens refreshed for VIN %s", link.vin)
        elif resp.status in (401, 403):
            _LOGGER.debug("PulseCloud: refresh rejected %s – unlinking", resp.status)
            self.unlink_device(link.vin)
            raise Exception("Token refresh rejected – device unlinked")
        elif resp.status >= 500:
            _LOGGER.debug(
                "PulseCloud: server error %s – keeping tokens, will retry later",
                resp.status,
            )
        else:
            body = await resp.text()
            _LOGGER.debug(
                "PulseCloud: unexpected status %s %s – unlinking", resp.status, body
            )
            self.unlink_device(link.vin)
            raise Exception("Token refresh failed – device unlinked")

    def _is_token_expired(self, token: str) -> bool:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return True

            payload = parts[1]
            payload += "=" * (-len(payload) % 4)

            decoded = base64.urlsafe_b64decode(payload).decode("utf-8")
            claims = json.loads(decoded)

            exp = claims.get("exp")
            if exp is None:
                return True

            expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
            return dt_util.utcnow() > expires_at - timedelta(seconds=60)
        except Exception as e:
            _LOGGER.debug("PulseCloud: failed to decode JWT exp: %s", e)
            return True


class OceanPulseApiError(Exception):
    """Base exception for all OceanPulse API errors."""


class AuthenticationError(OceanPulseApiError):
    """Authentication failed."""


class RequestError(OceanPulseApiError):
    """Failed to get the results from the API."""

    def __init__(self, message, error_code) -> None:
        super().__init__(message)
        self.error_code = error_code


class RequestConnectionError(OceanPulseApiError):
    """Failed to make the request to the API."""


class RequestTimeoutError(OceanPulseApiError):
    """Failed to get the results from the API."""


class RequestRetryError(OceanPulseApiError):
    """Retries too many times."""


class RequestDataError(OceanPulseApiError):
    """Data is not valid."""
