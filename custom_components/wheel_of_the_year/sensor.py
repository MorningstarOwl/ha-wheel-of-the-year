"""Sensor platform for the Wheel of the Year integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .calculations import (
    days_until_sabbat,
    get_current_season,
    get_moon_phase_info,
    get_next_sabbat_date,
    get_planetary_positions,
    get_solar_cycle_phase,
    get_sun_sign,
)
from .const import DOMAIN, PLANETS, SABBATS, SEASONS, ZODIAC

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

DEVICE_INFO = DeviceInfo(
    identifiers={(DOMAIN, "wheel_of_the_year")},
    name="Wheel of the Year",
    manufacturer="Pagan Calendar",
    model="Astronomical",
    sw_version="1.1.0",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wheel of the Year sensors from a config entry."""
    entities: list[SensorEntity] = []

    # ── Sabbat sensors (one per sabbat) ──
    for sabbat in SABBATS:
        entities.append(SabbatSensor(sabbat))

    # ── Next Sabbat sensor ──
    entities.append(NextSabbatSensor())

    # ── Moon Phase sensor ──
    entities.append(MoonPhaseSensor())

    # ── Sun Sign sensor ──
    entities.append(SunSignSensor())

    # ── Season sensor ──
    entities.append(SeasonSensor())

    # ── Planetary position sensors ──
    for planet in PLANETS:
        entities.append(PlanetSensor(planet))

    # ── Solar Cycle sensor ──
    entities.append(SolarCycleSensor())

    # ── Wheel State sensor (aggregate for the Lovelace card) ──
    entities.append(WheelStateSensor())

    async_add_entities(entities, True)


class SabbatSensor(SensorEntity):
    """Sensor for an individual Sabbat showing days until next occurrence."""

    _attr_has_entity_name = True
    _attr_device_class = None
    _attr_state_class = None

    def __init__(self, sabbat: dict) -> None:
        slug = sabbat["name"].lower()
        self._sabbat = sabbat
        self._attr_unique_id = f"wheel_sabbat_{slug}"
        self._attr_name = sabbat["name"]
        self._attr_icon = sabbat["icon"]
        self._attr_native_unit_of_measurement = "days"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()
        days = days_until_sabbat(self._sabbat, now)
        self._attr_native_value = days

        next_date = get_next_sabbat_date(self._sabbat, now)
        self._attr_extra_state_attributes = {
            "sabbat_name": self._sabbat["name"],
            "alt_name": self._sabbat["alt_name"],
            "type": self._sabbat["type"],
            "emoji": self._sabbat["emoji"],
            "next_date": next_date.strftime("%Y-%m-%d"),
            "color": self._sabbat["color"],
            "dark_color": self._sabbat["dark_color"],
            "description": self._sabbat["description"],
            "traditions": self._sabbat["traditions"],
            "is_today": days == 0,
        }


class NextSabbatSensor(SensorEntity):
    """Sensor showing the name of the next upcoming Sabbat."""

    _attr_has_entity_name = True
    _attr_unique_id = "wheel_next_sabbat"
    _attr_name = "Next Sabbat"
    _attr_icon = "mdi:calendar-star"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()
        nearest = None
        nearest_days = float("inf")

        for sabbat in SABBATS:
            days = days_until_sabbat(sabbat, now)
            if days < nearest_days:
                nearest_days = days
                nearest = sabbat

        if nearest:
            next_date = get_next_sabbat_date(nearest, now)
            self._attr_native_value = nearest["name"]
            self._attr_extra_state_attributes = {
                "alt_name": nearest["alt_name"],
                "days_until": nearest_days,
                "next_date": next_date.strftime("%Y-%m-%d"),
                "emoji": nearest["emoji"],
                "type": nearest["type"],
                "color": nearest["color"],
                "description": nearest["description"],
                "traditions": nearest["traditions"],
            }


class MoonPhaseSensor(SensorEntity):
    """Sensor for the current moon phase."""

    _attr_has_entity_name = True
    _attr_unique_id = "wheel_moon_phase"
    _attr_name = "Moon Phase"
    _attr_icon = "mdi:moon-waning-crescent"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()
        info = get_moon_phase_info(now)
        self._attr_native_value = info["name"]

        # Dynamic icon based on phase
        icon_map = {
            0: "mdi:moon-new",
            1: "mdi:moon-waxing-crescent",
            2: "mdi:moon-first-quarter",
            3: "mdi:moon-waxing-gibbous",
            4: "mdi:moon-full",
            5: "mdi:moon-waning-gibbous",
            6: "mdi:moon-last-quarter",
            7: "mdi:moon-waning-crescent",
        }
        self._attr_icon = icon_map.get(info["index"], "mdi:moon-waning-crescent")

        self._attr_extra_state_attributes = {
            "emoji": info["emoji"],
            "illumination": info["illumination"],
            "phase_number": info["phase"],
            "phase_index": info["index"],
            "magick": info["magick"],
            "description": info.get("description", ""),
        }


class SunSignSensor(SensorEntity):
    """Sensor for the current Sun sign."""

    _attr_has_entity_name = True
    _attr_unique_id = "wheel_sun_sign"
    _attr_name = "Sun Sign"
    _attr_icon = "mdi:zodiac-leo"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()
        sign = get_sun_sign(now)
        self._attr_native_value = sign["name"]

        # Dynamic icon
        icon_map = {
            "Aries": "mdi:zodiac-aries",
            "Taurus": "mdi:zodiac-taurus",
            "Gemini": "mdi:zodiac-gemini",
            "Cancer": "mdi:zodiac-cancer",
            "Leo": "mdi:zodiac-leo",
            "Virgo": "mdi:zodiac-virgo",
            "Libra": "mdi:zodiac-libra",
            "Scorpio": "mdi:zodiac-scorpio",
            "Sagittarius": "mdi:zodiac-sagittarius",
            "Capricorn": "mdi:zodiac-capricorn",
            "Aquarius": "mdi:zodiac-aquarius",
            "Pisces": "mdi:zodiac-pisces",
        }
        self._attr_icon = icon_map.get(sign["name"], "mdi:zodiac-leo")

        self._attr_extra_state_attributes = {
            "symbol": sign["symbol"],
            "element": sign["element"],
            "quality": sign["quality"],
            "ruler": sign["ruler"],
            "description": sign.get("description", ""),
            "start_date": f"{sign['start_month']:02d}-{sign['start_day']:02d}",
            "end_date": f"{sign['end_month']:02d}-{sign['end_day']:02d}",
        }


class SeasonSensor(SensorEntity):
    """Sensor for the current season."""

    _attr_has_entity_name = True
    _attr_unique_id = "wheel_season"
    _attr_name = "Current Season"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()
        season_name = get_current_season(now)
        season = SEASONS[season_name]

        self._attr_native_value = season_name
        self._attr_icon = season["icon"]
        self._attr_extra_state_attributes = {
            "description": season["description"],
            "long_description": season.get("long_description", season["description"]),
            "emoji": season.get("emoji", ""),
        }


class PlanetSensor(SensorEntity):
    """Sensor for a planet's current zodiac position."""

    _attr_has_entity_name = True

    def __init__(self, planet: dict) -> None:
        slug = planet["name"].lower()
        self._planet = planet
        self._attr_unique_id = f"wheel_planet_{slug}"
        self._attr_name = f"{planet['name']} Position"
        self._attr_icon = "mdi:earth"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()
        positions = get_planetary_positions(now)

        for p in positions:
            if p["name"] == self._planet["name"]:
                self._attr_native_value = f"{p['sign_name']} {p['sign_degree']:.0f}°"
                self._attr_extra_state_attributes = {
                    "planet_symbol": p["symbol"],
                    "planet_color": p.get("color", "#ccc"),
                    "sign_name": p["sign_name"],
                    "sign_symbol": p["sign_symbol"],
                    "sign_degree": p["sign_degree"],
                    "ecliptic_longitude": p["longitude"],
                }
                break


class SolarCycleSensor(SensorEntity):
    """Sensor for solar cycle activity."""

    _attr_has_entity_name = True
    _attr_unique_id = "wheel_solar_cycle"
    _attr_name = "Solar Cycle"
    _attr_icon = "mdi:white-balance-sunny"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now(tz=timezone.utc)
        info = get_solar_cycle_phase(now)
        self._attr_native_value = info["label"]
        self._attr_extra_state_attributes = {
            "cycle_number": info["cycle_number"],
            "progress": info["progress"],
            "phase": info["phase"],
            "sunspot_estimate": info["sunspot_estimate"],
            "years_remaining": info["years_remaining"],
        }


class WheelStateSensor(SensorEntity):
    """Aggregate sensor providing full state for the Lovelace card."""

    _attr_has_entity_name = True
    _attr_unique_id = "wheel_state"
    _attr_name = "Wheel State"
    _attr_icon = "mdi:rotate-right"

    @property
    def device_info(self) -> DeviceInfo:
        return DEVICE_INFO

    def update(self) -> None:
        now = datetime.now()

        # Moon
        moon_info = get_moon_phase_info(now)

        # Sun sign
        sun_sign = get_sun_sign(now)

        # Season
        season_name = get_current_season(now)
        season_data = SEASONS[season_name]

        # Solar cycle
        solar_cycle = get_solar_cycle_phase(
            datetime.now(tz=timezone.utc)
        )

        # Next sabbat
        nearest = None
        nearest_days = float("inf")
        sabbat_data = []
        for sabbat in SABBATS:
            days = days_until_sabbat(sabbat, now)
            next_date = get_next_sabbat_date(sabbat, now)
            sabbat_data.append({
                "name": sabbat["name"],
                "alt_name": sabbat["alt_name"],
                "emoji": sabbat["emoji"],
                "days_until": days,
                "next_date": next_date.strftime("%Y-%m-%d"),
                "color": sabbat["color"],
                "dark_color": sabbat["dark_color"],
                "description": sabbat["description"],
                "traditions": sabbat["traditions"],
            })
            if days < nearest_days:
                nearest_days = days
                nearest = sabbat

        # Planets
        planet_positions = get_planetary_positions(now)

        self._attr_native_value = nearest["name"] if nearest else "Unknown"
        self._attr_extra_state_attributes = {
            "moon_phase": moon_info["name"],
            "moon_illumination": moon_info["illumination"],
            "moon_emoji": moon_info["emoji"],
            "moon_phase_number": moon_info["phase"],
            "moon_magick": moon_info.get("magick", ""),
            "moon_description": moon_info.get("description", ""),
            "sun_sign": sun_sign["name"],
            "sun_sign_symbol": sun_sign["symbol"],
            "sun_sign_element": sun_sign["element"],
            "sun_sign_quality": sun_sign["quality"],
            "sun_sign_ruler": sun_sign["ruler"],
            "sun_sign_description": sun_sign.get("description", ""),
            "season": season_name,
            "season_emoji": season_data.get("emoji", ""),
            "season_description": season_data.get("long_description", season_data["description"]),
            "solar_cycle": solar_cycle,
            "next_sabbat": nearest["name"] if nearest else None,
            "next_sabbat_days": nearest_days,
            "sabbats": sabbat_data,
            "planets": planet_positions,
        }
