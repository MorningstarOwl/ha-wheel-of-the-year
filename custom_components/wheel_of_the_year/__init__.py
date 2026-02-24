"""The Wheel of the Year integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import async_register_extra_js_url
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

CARD_URL = f"/{DOMAIN}/wheel-of-the-year-card.js"
CARD_PATH = Path(__file__).parent / "www" / "wheel-of-the-year-card.js"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register the Lovelace card static path and load it via the frontend."""
    hass.http.register_static_path(CARD_URL, str(CARD_PATH), cache_headers=False)
    async_register_extra_js_url(hass, CARD_URL)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wheel of the Year from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
