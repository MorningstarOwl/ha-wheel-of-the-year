"""The Wheel of the Year integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace.resources import ResourceStorageCollection
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

CARD_URL = f"/{DOMAIN}/wheel-of-the-year-card.js"
CARD_VERSION = "1.1.2"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Register the Lovelace card static path and resource."""
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            f"/{DOMAIN}",
            Path(__file__).parent / "www",
            cache_headers=False,
        )
    ])

    versioned_url = f"{CARD_URL}?v={CARD_VERSION}"
    resources = hass.data["lovelace"].resources

    if isinstance(resources, ResourceStorageCollection):
        await resources.async_get_info()
        existing = [r for r in resources.async_items() if DOMAIN in r.get("url", "")]
        if existing:
            if not existing[0]["url"].endswith(CARD_VERSION):
                await resources.async_update_item(
                    existing[0]["id"], {"res_type": "module", "url": versioned_url}
                )
        else:
            await resources.async_create_item({"res_type": "module", "url": versioned_url})
    else:
        # YAML lovelace mode — fall back to global extra JS URL
        add_extra_js_url(hass, versioned_url)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wheel of the Year from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
