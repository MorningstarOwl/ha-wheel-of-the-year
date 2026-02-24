"""The Wheel of the Year integration."""

from __future__ import annotations

import uuid
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN, PLATFORMS

CARD_URL = f"/{DOMAIN}/wheel-of-the-year-card.js"
CARD_PATH = Path(__file__).parent / "www" / "wheel-of-the-year-card.js"

_LOVELACE_STORAGE_KEY = "lovelace_resources"
_LOVELACE_STORAGE_VERSION = 1


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register the Lovelace card as a static resource and auto-add to Lovelace."""
    hass.http.register_static_path(CARD_URL, str(CARD_PATH), cache_headers=False)
    await _async_register_lovelace_resource(hass, CARD_URL)
    return True


async def _async_register_lovelace_resource(hass: HomeAssistant, url: str) -> None:
    """Add the card to Lovelace resources storage if not already present."""
    store = Store(hass, _LOVELACE_STORAGE_VERSION, _LOVELACE_STORAGE_KEY)
    data = await store.async_load() or {"items": []}

    if any(item.get("url") == url for item in data.get("items", [])):
        return

    data.setdefault("items", []).append({
        "id": uuid.uuid4().hex,
        "type": "module",
        "url": url,
    })
    await store.async_save(data)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wheel of the Year from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
