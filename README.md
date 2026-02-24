# 🕯️ Wheel of the Year — Home Assistant Integration

A Home Assistant custom integration that brings the Wheel of the Year to your smart home dashboard. It creates sensor entities for all eight Sabbats, moon phases, zodiac positions, planetary transits, solar cycle activity, and seasons — plus a stunning custom Lovelace card that renders the full interactive wheel.

![Wheel of the Year](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?style=flat&logo=home-assistant)
![Version](https://img.shields.io/badge/version-1.1.0-c9a84c)

---

## Features

### Sensor Entities (24 total)

| Entity | State | Attributes |
|--------|-------|------------|
| **8× Sabbat sensors** | Days until next occurrence | Date, description, traditions, color, alt name |
| **Next Sabbat** | Name of upcoming sabbat | Days until, date, description |
| **Moon Phase** | Current phase name | Illumination %, emoji, magickal correspondences, description |
| **Sun Sign** | Current zodiac sign | Symbol, element, quality, ruling planet, description |
| **Current Season** | Season name | Short & long description, emoji |
| **10× Planet sensors** | Sign + degree (e.g. "Pisces 12°") | Ecliptic longitude, sign details, color |
| **Solar Cycle** | Current phase label | Cycle number, progress, sunspot estimate, years remaining |
| **Wheel State** | Next sabbat name | Full aggregate data for Lovelace card |

### Custom Lovelace Card

- **Months ring** (outermost) with current month highlighted
- **Days ring** with today marker and weekly tick marks
- **Zodiac ring** with element-based coloring
- **Sabbat ring** with gradient fills and icons
- **Individual planet orbit rings** (Mercury through Pluto each on their own track)
- **Solar Cycle 25 ring** with activity marker
- **Animated moon phase** in the center
- **Date marker line** showing current position on the wheel
- **Hover tooltips** for all elements (sabbats, zodiac, months, planets, moon, solar cycle)
- **Info panels** with moon phase, sun sign, sabbat countdowns, planetary positions, solar cycle, and season
- **Starfield background** animation
- **Fully responsive** design

---

## Installation

### Via HACS (recommended)

1. Add this repository as a custom repository in HACS under **Integrations**
2. Install **Wheel of the Year**
3. Restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration**, search for **"Wheel of the Year"**, and click **Submit**
5. Register the Lovelace card resource (see Step 3 below)

### Manual Installation

Copy the `custom_components/wheel_of_the_year/` folder to your Home Assistant `config/custom_components/` directory:

```
config/
└── custom_components/
    └── wheel_of_the_year/
        ├── __init__.py
        ├── calculations.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── sensor.py
        ├── strings.json
        ├── www/
        │   └── wheel-of-the-year-card.js
        └── translations/
            └── en.json
```

Restart Home Assistant, then add the integration via **Settings → Devices & Services**.

### Step 3: Restart and Add the Card

The integration automatically registers the Lovelace card resource on startup — no manual resource registration needed. Just restart Home Assistant and the card will be available.

### Step 4: Add the Card to Your Dashboard

Add the card to any dashboard using YAML:

```yaml
type: custom:wheel-of-the-year-card
entity: sensor.wheel_of_the_year_wheel_state
```

---

## Card Configuration Options

```yaml
type: custom:wheel-of-the-year-card
entity: sensor.wheel_of_the_year_wheel_state  # Required
title: The Wheel of the Year                   # Optional custom title
show_title: true                               # Show/hide title (default: true)
show_info_panels: true                         # Show/hide info panels below wheel (default: true)
show_stars: true                               # Show/hide starfield background (default: true)
size: auto                                     # Wheel size in px or 'auto' (default: auto)
```

---

## Example Automations

### Notify on Sabbat Day

```yaml
automation:
  - alias: "Sabbat Day Notification"
    trigger:
      - platform: state
        entity_id: sensor.wheel_of_the_year_yule
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_imbolc
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_ostara
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_beltane
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_litha
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_lughnasadh
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_mabon
        to: "0"
      - platform: state
        entity_id: sensor.wheel_of_the_year_samhain
        to: "0"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🕯️ Blessed Sabbat!"
          message: >
            Today is {{ state_attr('sensor.wheel_of_the_year_next_sabbat', 'alt_name') }}.
            {{ state_attr('sensor.wheel_of_the_year_next_sabbat', 'description') }}
```

### Full Moon Notification

```yaml
automation:
  - alias: "Full Moon Alert"
    trigger:
      - platform: state
        entity_id: sensor.wheel_of_the_year_moon_phase
        to: "Full Moon"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🌕 Full Moon Tonight"
          message: >
            The Moon is full in {{ states('sensor.wheel_of_the_year_sun_sign') }}.
            Illumination: {{ state_attr('sensor.wheel_of_the_year_moon_phase', 'illumination') }}%.
            Magick: {{ state_attr('sensor.wheel_of_the_year_moon_phase', 'magick') }}
```

### Set Lights for Season

```yaml
automation:
  - alias: "Seasonal Ambient Lighting"
    trigger:
      - platform: state
        entity_id: sensor.wheel_of_the_year_current_season
    action:
      - choose:
          - conditions:
              - condition: state
                entity_id: sensor.wheel_of_the_year_current_season
                state: "Spring"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ambient
                data:
                  color_name: "green"
                  brightness: 180
          - conditions:
              - condition: state
                entity_id: sensor.wheel_of_the_year_current_season
                state: "Summer"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ambient
                data:
                  color_name: "gold"
                  brightness: 255
          - conditions:
              - condition: state
                entity_id: sensor.wheel_of_the_year_current_season
                state: "Autumn"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ambient
                data:
                  color_name: "orange"
                  brightness: 200
          - conditions:
              - condition: state
                entity_id: sensor.wheel_of_the_year_current_season
                state: "Winter"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ambient
                data:
                  color_name: "blue"
                  brightness: 150
```

### Solar Maximum Alert

```yaml
automation:
  - alias: "Solar Maximum Alert"
    trigger:
      - platform: state
        entity_id: sensor.wheel_of_the_year_solar_cycle
        to: "Solar Maximum"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "☉ Solar Maximum"
          message: >
            Solar Cycle {{ state_attr('sensor.wheel_of_the_year_solar_cycle', 'cycle_number') }}
            has reached solar maximum. Estimated sunspot number:
            {{ state_attr('sensor.wheel_of_the_year_solar_cycle', 'sunspot_estimate') }}.
```

---

## Entity IDs Reference

| Entity ID | Type |
|-----------|------|
| `sensor.wheel_of_the_year_yule` | Sabbat (days until) |
| `sensor.wheel_of_the_year_imbolc` | Sabbat |
| `sensor.wheel_of_the_year_ostara` | Sabbat |
| `sensor.wheel_of_the_year_beltane` | Sabbat |
| `sensor.wheel_of_the_year_litha` | Sabbat |
| `sensor.wheel_of_the_year_lughnasadh` | Sabbat |
| `sensor.wheel_of_the_year_mabon` | Sabbat |
| `sensor.wheel_of_the_year_samhain` | Sabbat |
| `sensor.wheel_of_the_year_next_sabbat` | Next sabbat name |
| `sensor.wheel_of_the_year_moon_phase` | Moon phase name |
| `sensor.wheel_of_the_year_sun_sign` | Zodiac sign |
| `sensor.wheel_of_the_year_current_season` | Season name |
| `sensor.wheel_of_the_year_solar_cycle` | Solar cycle phase |
| `sensor.wheel_of_the_year_sun_position` | Planet position |
| `sensor.wheel_of_the_year_moon_position` | Planet position |
| `sensor.wheel_of_the_year_mercury_position` | Planet position |
| `sensor.wheel_of_the_year_venus_position` | Planet position |
| `sensor.wheel_of_the_year_mars_position` | Planet position |
| `sensor.wheel_of_the_year_jupiter_position` | Planet position |
| `sensor.wheel_of_the_year_saturn_position` | Planet position |
| `sensor.wheel_of_the_year_uranus_position` | Planet position |
| `sensor.wheel_of_the_year_neptune_position` | Planet position |
| `sensor.wheel_of_the_year_pluto_position` | Planet position |
| `sensor.wheel_of_the_year_wheel_state` | Aggregate (for card) |

---

## What's New in v1.1.0

- **Months ring** — outermost ring showing all 12 calendar months with current month highlighted
- **Days ring** — 365/366 day cells with today brightly lit and weekly tick marks
- **Solar Cycle sensor & ring** — tracks Solar Cycle 25 activity phase, progress, and estimated sunspot count
- **Individual planet orbit rings** — each planet (Mercury through Pluto) on its own concentric track
- **Enriched data** — zodiac descriptions, moon phase descriptions, longer sabbat & season lore, planet colors
- **Expanded tooltips** — hover info for months, individual planets, solar cycle marker, and moon center
- **6 info panels** — added solar cycle and season panels below the wheel
- **Touch support** — tooltips now work on mobile via touch events

---

## Notes

- All astronomical calculations are approximate (simplified orbital models)
- Sabbat dates use traditional fixed dates; solar sabbats may vary by ±1 day in practice
- Planetary positions use mean longitude approximations — suitable for general zodiac placement, not precision astrology
- Solar cycle data is based on Solar Cycle 25 predictions and uses a sinusoidal approximation
- The integration has no external dependencies and requires no API keys
- Updates every 5 minutes by default

---

## License

MIT
