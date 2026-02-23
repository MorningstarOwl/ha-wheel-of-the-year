"""Constants for the Wheel of the Year integration."""

DOMAIN = "wheel_of_the_year"
PLATFORMS = ["sensor"]

# ── Sabbats ──────────────────────────────────────────────────────────

SABBATS = [
    {
        "name": "Yule",
        "alt_name": "Winter Solstice",
        "icon": "mdi:candle",
        "emoji": "🕯️",
        "month": 12,
        "day": 21,
        "type": "solar",
        "color": "#6ba3c7",
        "description": (
            "Yule marks the Winter Solstice, the longest night and the rebirth of the Sun. "
            "The Goddess gives birth to the God as the Oak King, heralding the return of the light."
        ),
        "traditions": "Yule log, evergreen wreaths, candle lighting, wassailing, gift exchange",
    },
    {
        "name": "Imbolc",
        "alt_name": "Candlemas / Brigid's Day",
        "icon": "mdi:fire",
        "emoji": "🔥",
        "month": 2,
        "day": 1,
        "type": "cross",
        "color": "#e8e0d0",
        "description": (
            "Imbolc celebrates the first stirrings of spring. Sacred to the goddess Brigid, "
            "it honors the quickening of the land and the return of the Maiden."
        ),
        "traditions": "Brigid's cross, candle ceremonies, spring cleaning, milk offerings, poetry",
    },
    {
        "name": "Ostara",
        "alt_name": "Spring Equinox",
        "icon": "mdi:sprout",
        "emoji": "🌱",
        "month": 3,
        "day": 20,
        "type": "solar",
        "color": "#7cc47e",
        "description": (
            "Ostara celebrates the Spring Equinox, when day and night stand in perfect balance "
            "before light triumphs. A time of fertility, new growth, and joyful renewal."
        ),
        "traditions": "Egg decorating, planting seeds, balance rituals, spring altars, hare symbolism",
    },
    {
        "name": "Beltane",
        "alt_name": "May Day",
        "icon": "mdi:flower",
        "emoji": "🌸",
        "month": 5,
        "day": 1,
        "type": "cross",
        "color": "#e05a80",
        "description": (
            "Beltane is the great festival of fertility and the sacred union of the God and Goddess. "
            "Fires are lit on hilltops to purify and protect."
        ),
        "traditions": "Maypole dancing, bonfires, flower crowns, handfasting, fairy offerings",
    },
    {
        "name": "Litha",
        "alt_name": "Summer Solstice / Midsummer",
        "icon": "mdi:white-balance-sunny",
        "emoji": "☀️",
        "month": 6,
        "day": 21,
        "type": "solar",
        "color": "#e8c55a",
        "description": (
            "Litha, the Summer Solstice, is the longest day and the peak of the Sun's power. "
            "A day of abundance, magic, and faery enchantment."
        ),
        "traditions": "Bonfires, sun wheels, herb gathering, mead, staying up all night",
    },
    {
        "name": "Lughnasadh",
        "alt_name": "Lammas",
        "icon": "mdi:barley",
        "emoji": "🌾",
        "month": 8,
        "day": 1,
        "type": "cross",
        "color": "#d4943a",
        "description": (
            "Lughnasadh is the first of three harvest festivals. Named for the god Lugh, "
            "it honors the sacrifice of the God who gives his life force into the grain."
        ),
        "traditions": "Baking bread, corn dollies, games and competitions, berry picking",
    },
    {
        "name": "Mabon",
        "alt_name": "Autumn Equinox",
        "icon": "mdi:leaf",
        "emoji": "🍂",
        "month": 9,
        "day": 22,
        "type": "solar",
        "color": "#c46030",
        "description": (
            "Mabon marks the Autumn Equinox, the second harvest, and another moment of perfect balance. "
            "It is the Pagan Thanksgiving — a time of gratitude and reflection."
        ),
        "traditions": "Feast of thanks, wine-making, apple harvest, balance rituals, cornucopia",
    },
    {
        "name": "Samhain",
        "alt_name": "Halloween / All Hallows' Eve",
        "icon": "mdi:halloween",
        "emoji": "🎃",
        "month": 10,
        "day": 31,
        "type": "cross",
        "color": "#9050a0",
        "description": (
            "Samhain is the Witch's New Year and the most sacred of Sabbats. "
            "The veil between the worlds of the living and the dead is thinnest."
        ),
        "traditions": "Ancestor altars, divination, dumb supper, jack-o-lanterns, spirit communication",
    },
]

# ── Zodiac Signs ─────────────────────────────────────────────────────

ZODIAC = [
    {"name": "Aries", "symbol": "♈", "element": "Fire", "quality": "Cardinal", "ruler": "Mars",
     "start_month": 3, "start_day": 21, "end_month": 4, "end_day": 19},
    {"name": "Taurus", "symbol": "♉", "element": "Earth", "quality": "Fixed", "ruler": "Venus",
     "start_month": 4, "start_day": 20, "end_month": 5, "end_day": 20},
    {"name": "Gemini", "symbol": "♊", "element": "Air", "quality": "Mutable", "ruler": "Mercury",
     "start_month": 5, "start_day": 21, "end_month": 6, "end_day": 20},
    {"name": "Cancer", "symbol": "♋", "element": "Water", "quality": "Cardinal", "ruler": "Moon",
     "start_month": 6, "start_day": 21, "end_month": 7, "end_day": 22},
    {"name": "Leo", "symbol": "♌", "element": "Fire", "quality": "Fixed", "ruler": "Sun",
     "start_month": 7, "start_day": 23, "end_month": 8, "end_day": 22},
    {"name": "Virgo", "symbol": "♍", "element": "Earth", "quality": "Mutable", "ruler": "Mercury",
     "start_month": 8, "start_day": 23, "end_month": 9, "end_day": 22},
    {"name": "Libra", "symbol": "♎", "element": "Air", "quality": "Cardinal", "ruler": "Venus",
     "start_month": 9, "start_day": 23, "end_month": 10, "end_day": 22},
    {"name": "Scorpio", "symbol": "♏", "element": "Water", "quality": "Fixed", "ruler": "Pluto / Mars",
     "start_month": 10, "start_day": 23, "end_month": 11, "end_day": 21},
    {"name": "Sagittarius", "symbol": "♐", "element": "Fire", "quality": "Mutable", "ruler": "Jupiter",
     "start_month": 11, "start_day": 22, "end_month": 12, "end_day": 21},
    {"name": "Capricorn", "symbol": "♑", "element": "Earth", "quality": "Cardinal", "ruler": "Saturn",
     "start_month": 12, "start_day": 22, "end_month": 1, "end_day": 19},
    {"name": "Aquarius", "symbol": "♒", "element": "Air", "quality": "Fixed", "ruler": "Uranus / Saturn",
     "start_month": 1, "start_day": 20, "end_month": 2, "end_day": 18},
    {"name": "Pisces", "symbol": "♓", "element": "Water", "quality": "Mutable", "ruler": "Neptune / Jupiter",
     "start_month": 2, "start_day": 19, "end_month": 3, "end_day": 20},
]

# ── Moon Phases ──────────────────────────────────────────────────────

MOON_PHASES = [
    {"name": "New Moon", "emoji": "🌑",
     "magick": "New beginnings, intention setting, banishing, shadow work"},
    {"name": "Waxing Crescent", "emoji": "🌒",
     "magick": "Attraction, courage, hope, building plans"},
    {"name": "First Quarter", "emoji": "🌓",
     "magick": "Strength, determination, overcoming obstacles"},
    {"name": "Waxing Gibbous", "emoji": "🌔",
     "magick": "Refinement, patience, adjustment, nurturing growth"},
    {"name": "Full Moon", "emoji": "🌕",
     "magick": "Manifestation, divination, charging crystals, healing, abundance"},
    {"name": "Waning Gibbous", "emoji": "🌖",
     "magick": "Gratitude, sharing knowledge, introspection, forgiveness"},
    {"name": "Third Quarter", "emoji": "🌗",
     "magick": "Release, letting go, banishing, breaking habits"},
    {"name": "Waning Crescent", "emoji": "🌘",
     "magick": "Rest, surrender, wisdom, psychic visions, closure"},
]

# ── Planets ──────────────────────────────────────────────────────────

PLANETS = [
    {"name": "Sun", "symbol": "☉",
     "L0": 280.46646, "rate": 36000.76983, "L1": 0.0003032},
    {"name": "Moon", "symbol": "☽",
     "L0": 218.3165, "rate": 481267.8813, "L1": 0},
    {"name": "Mercury", "symbol": "☿",
     "L0": 252.2509, "rate": 149472.6746, "L1": 0},
    {"name": "Venus", "symbol": "♀",
     "L0": 181.9798, "rate": 58517.8157, "L1": 0},
    {"name": "Mars", "symbol": "♂",
     "L0": 355.4330, "rate": 19140.2993, "L1": 0},
    {"name": "Jupiter", "symbol": "♃",
     "L0": 34.3515, "rate": 3034.9057, "L1": 0},
    {"name": "Saturn", "symbol": "♄",
     "L0": 50.0774, "rate": 1222.1138, "L1": 0},
    {"name": "Uranus", "symbol": "♅",
     "L0": 314.055, "rate": 428.467, "L1": 0},
    {"name": "Neptune", "symbol": "♆",
     "L0": 304.349, "rate": 218.486, "L1": 0},
    {"name": "Pluto", "symbol": "⯓",
     "L0": 238.929, "rate": 145.205, "L1": 0},
]

# ── Seasons ──────────────────────────────────────────────────────────

SEASONS = {
    "Spring": {
        "months": [3, 4, 5],
        "icon": "mdi:flower",
        "description": "The season of awakening and renewal.",
    },
    "Summer": {
        "months": [6, 7, 8],
        "icon": "mdi:white-balance-sunny",
        "description": "The season of fullness and abundance.",
    },
    "Autumn": {
        "months": [9, 10, 11],
        "icon": "mdi:leaf-maple",
        "description": "The season of harvest and reflection.",
    },
    "Winter": {
        "months": [12, 1, 2],
        "icon": "mdi:snowflake",
        "description": "The season of stillness and introspection.",
    },
}
