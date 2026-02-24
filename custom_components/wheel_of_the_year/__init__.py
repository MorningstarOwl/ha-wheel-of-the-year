"""The Wheel of the Year integration."""

from __future__ import annotations

import uuid
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

CARD_URL = f"/{DOMAIN}/wheel-of-the-year-card.js"
CARD_PATH = Path(__file__).parent / "www" / "wheel-of-the-year-card.js"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register the Lovelace card static path and auto-add it as a resource."""
    hass.http.register_static_path(CARD_URL, str(CARD_PATH), cache_headers=False)

    async def _add_resource(_event=None) -> None:
        await _async_register_lovelace_resource(hass, CARD_URL)

    if hass.is_running:
        await _add_resource()
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _add_resource)

    return True


async def _async_register_lovelace_resource(hass: HomeAssistant, url: str) -> None:
    """Add the card to the live Lovelace resource collection if not already present."""
    try:
        resources = hass.data.get("lovelace", {}).get("resources")
        if resources is None:
            return

        # Ensure the collection is loaded from storage
        await resources.async_get_info()

        if any(item["url"] == url for item in resources.async_items()):
            return

        await resources.async_create_item({"res_type": "module", "url": url})
    except Exception:  # noqa: BLE001
        pass


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wheel of the Year from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
