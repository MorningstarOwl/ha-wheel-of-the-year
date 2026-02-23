"""Astronomical calculations for the Wheel of the Year."""

from __future__ import annotations

import math
from datetime import datetime, timezone

from .const import MOON_PHASES, PLANETS, ZODIAC

# Known new moon reference: Jan 6, 2000 18:14 UTC
_KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14, 0, tzinfo=timezone.utc)
_SYNODIC_MONTH = 29.53058770576


def julian_day(dt: datetime) -> float:
    """Calculate Julian Day Number from a datetime."""
    d = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    y = d.year
    m = d.month
    day = d.day
    hr = d.hour + d.minute / 60 + d.second / 3600
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    jd = (
        day
        + (153 * mm + 2) // 5
        + 365 * yy
        + yy // 4
        - yy // 100
        + yy // 400
        - 32045
        + (hr - 12) / 24
    )
    return jd


def get_moon_phase(dt: datetime) -> float:
    """Return moon phase as 0..1 (0=new, 0.5=full)."""
    d = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    days_since = (d - _KNOWN_NEW_MOON).total_seconds() / 86400
    lunations = days_since / _SYNODIC_MONTH
    return lunations - math.floor(lunations)


def get_moon_phase_info(dt: datetime) -> dict:
    """Return detailed moon phase info."""
    phase = get_moon_phase(dt)
    idx = int(phase * 8 + 0.5) % 8
    illumination = (1 - math.cos(phase * 2 * math.pi)) / 2 * 100
    info = MOON_PHASES[idx].copy()
    info["phase"] = round(phase, 4)
    info["illumination"] = round(illumination, 1)
    info["index"] = idx
    return info


def _normalize_deg(deg: float) -> float:
    return deg % 360


def get_planetary_positions(dt: datetime) -> list[dict]:
    """Return approximate ecliptic longitudes for all planets."""
    jd = julian_day(dt)
    T = (jd - 2451545.0) / 36525  # Julian centuries from J2000.0

    positions = []
    for planet in PLANETS:
        lon = _normalize_deg(
            planet["L0"] + planet["rate"] * T + planet.get("L1", 0) * T * T
        )
        sign_idx = int(lon / 30) % 12
        sign_deg = lon % 30
        zodiac_sign = ZODIAC[sign_idx]

        positions.append(
            {
                "name": planet["name"],
                "symbol": planet["symbol"],
                "longitude": round(lon, 2),
                "sign_index": sign_idx,
                "sign_degree": round(sign_deg, 1),
                "sign_name": zodiac_sign["name"],
                "sign_symbol": zodiac_sign["symbol"],
            }
        )
    return positions


def get_sun_sign(dt: datetime) -> dict:
    """Return the current Sun sign based on date."""
    m = dt.month
    d = dt.day
    for z in ZODIAC:
        if z["name"] == "Capricorn":
            if (m == 12 and d >= 22) or (m == 1 and d <= 19):
                return z
        else:
            if (m == z["start_month"] and d >= z["start_day"]) or (
                m == z["end_month"] and d <= z["end_day"]
            ):
                return z
    return ZODIAC[0]


def get_current_season(dt: datetime) -> str:
    """Return current season name."""
    m = dt.month
    if 3 <= m <= 5:
        return "Spring"
    elif 6 <= m <= 8:
        return "Summer"
    elif 9 <= m <= 11:
        return "Autumn"
    else:
        return "Winter"


def get_sabbat_date(sabbat: dict, year: int) -> datetime:
    """Get the date of a sabbat for a given year."""
    return datetime(year, sabbat["month"], sabbat["day"])


def get_next_sabbat_date(sabbat: dict, now: datetime) -> datetime:
    """Get the next occurrence of a sabbat from now."""
    d = get_sabbat_date(sabbat, now.year)
    if d.date() < now.date():
        d = get_sabbat_date(sabbat, now.year + 1)
    return d


def days_until_sabbat(sabbat: dict, now: datetime) -> int:
    """Return days until next occurrence of a sabbat."""
    next_date = get_next_sabbat_date(sabbat, now)
    return (next_date.date() - now.date()).days
