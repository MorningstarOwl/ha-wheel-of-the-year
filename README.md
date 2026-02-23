# 🕯️ Wheel of the Year — Home Assistant Integration

A Home Assistant custom integration that brings the Wheel of the Year to your smart home dashboard. It creates sensor entities for all eight Sabbats, moon phases, zodiac positions, planetary transits, and seasons — plus a stunning custom Lovelace card that renders the full interactive wheel.

![Wheel of the Year](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?style=flat&logo=home-assistant)

---

## Features

### Sensor Entities (19 total)

| Entity | State | Attributes |
|--------|-------|------------|
| **8× Sabbat sensors** | Days until next occurrence | Date, description, traditions, color, alt name |
| **Next Sabbat** | Name of upcoming sabbat | Days until, date, description |
| **Moon Phase** | Current phase name | Illumination %, emoji, magickal correspondences |
| **Sun Sign** | Current zodiac sign | Symbol, element, quality, ruling planet |
| **Current Season** | Season name | Description |
| **10× Planet sensors** | Sign + degree (e.g. "Pisces 12°") | Ecliptic longitude, sign details |
| **Wheel State** | Next sabbat name | Full aggregate data for Lovelace card |

### Custom Lovelace Card

- Full interactive wheel with zodiac ring, sabbat ring, and planetary positions
- Animated moon phase in the center
- Real-time date marker showing current position on the wheel
- Hover tooltips with sabbat and zodiac details
- Info panels with moon phase, sun sign, and sabbat countdowns
- Starfield background animation
- Fully responsive

---

## Installation

### Step 1: Copy the Integration

Copy the `custom_components/wheel_of_the_year/` folder to your Home Assistant `config/custom_components/` directory:

```
config/
├── custom_components/
│   └── wheel_of_the_year/
│       ├── __init__.py
│       ├── calculations.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── sensor.py
│       ├── strings.json
│       └── translations/
│           └── en.json
```

### Step 2: Copy the Lovelace Card

Copy `www/wheel-of-the-year-card.js` to your Home Assistant `config/www/` directory:

```
config/
├── www/
│   └── wheel-of-the-year-card.js
```

### Step 3: Restart Home Assistant

Restart Home Assistant to pick up the new integration.

### Step 4: Add the Integration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **"Wheel of the Year"**
3. Click **Submit** (no configuration needed)

All 19 sensor entities will be created automatically under a single "Wheel of the Year" device.

### Step 5: Register the Lovelace Card

Add the card as a resource in your Lovelace dashboard:

1. Go to **Settings → Dashboards → Resources** (or use the three-dot menu → Resources in your dashboard)
2. Click **Add Resource**
3. Set URL to: `/local/wheel-of-the-year-card.js`
4. Set Type to: **JavaScript Module**

Alternatively, add it to your `configuration.yaml`:

```yaml
lovelace:
  resources:
    - url: /local/wheel-of-the-year-card.js
      type: module
```

### Step 6: Add the Card to Your Dashboard

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

## Notes

- All astronomical calculations are approximate (simplified orbital models)
- Sabbat dates use traditional fixed dates; solar sabbats may vary by ±1 day in practice
- Planetary positions use mean longitude approximations — suitable for general zodiac placement, not precision astrology
- The integration has no external dependencies and requires no API keys
- Updates every 5 minutes by default

---

## License

MIT
