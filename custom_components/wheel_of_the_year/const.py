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
        "dark_color": "#2a4a5c",
        "description": (
            "Yule marks the Winter Solstice, the longest night and the rebirth of the Sun. "
            "The Goddess gives birth to the God as the Oak King, heralding the return of the light. "
            "It is a time of hope, renewal, hearth fires, evergreen boughs, and gift-giving — "
            "celebrating the promise that even in deepest darkness, the light will return."
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
        "dark_color": "#5a5548",
        "description": (
            "Imbolc celebrates the first stirrings of spring. Sacred to the goddess Brigid, "
            "it honors the quickening of the land, the lengthening days, and the return of the "
            "Maiden aspect of the Goddess. Ewes begin to lactate, snowdrops push through frozen "
            "earth, and the promise of spring becomes palpable. It is a festival of purification, "
            "inspiration, and the creative fire."
        ),
        "traditions": "Brigid's cross, candle ceremonies, spring cleaning, milk and dairy offerings, poetry",
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
        "dark_color": "#2d5a2f",
        "description": (
            "Ostara celebrates the Spring Equinox, when day and night stand in perfect balance "
            "before light triumphs. Named for the Germanic goddess Ēostre, it is a time of "
            "fertility, new growth, and joyful renewal. The God, now a youth, walks the greening "
            "land with the Maiden Goddess. Seeds are planted both literally and metaphorically."
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
        "dark_color": "#6a2040",
        "description": (
            "Beltane is the great festival of fertility and the sacred union of the God and "
            "Goddess. The veil between the worlds thins as faeries roam freely. Fires are lit "
            "on hilltops to purify and protect, and the Maypole dance weaves the masculine and "
            "feminine energies together. It celebrates passion, creativity, vitality, and the "
            "full eruption of life."
        ),
        "traditions": "Maypole dancing, bonfires, flower crowns, handfasting, fairy offerings, dew washing",
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
        "dark_color": "#6a5a20",
        "description": (
            "Litha, the Summer Solstice, is the longest day and the peak of the Sun's power. "
            "The God stands at the height of his strength as the Holly King prepares to challenge "
            "the Oak King. It is a day of abundance, magic, and faery enchantment — yet also holds "
            "the bittersweet knowledge that the light now begins its slow retreat toward winter."
        ),
        "traditions": "Bonfires, sun wheels, herb gathering, mead, St. John's Wort, staying up all night",
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
        "dark_color": "#5a3e14",
        "description": (
            "Lughnasadh, or Lammas, is the first of three harvest festivals. Named for the god "
            "Lugh, it honors the sacrifice of the God who gives his life force into the grain so "
            "the people may live. The first loaf is baked from the new grain in thanksgiving. It "
            "is a time of gratitude, skill, competition, and the first acknowledgment that summer wanes."
        ),
        "traditions": "Baking bread, corn dollies, games and competitions, berry picking, grain offerings",
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
        "dark_color": "#5a2a14",
        "description": (
            "Mabon marks the Autumn Equinox, the second harvest, and another moment of perfect "
            "balance. The God prepares to enter the underworld, and the Goddess begins her descent "
            "into her Crone aspect. It is the Pagan Thanksgiving — a time of gratitude, reflection, "
            "and preparing for the coming darkness. The scales tip, and night begins to dominate."
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
        "dark_color": "#3a1848",
        "description": (
            "Samhain is the Witch's New Year and the most sacred of Sabbats. The veil between "
            "the worlds of the living and the dead is thinnest, allowing communion with ancestors "
            "and departed loved ones. The God has fully passed into the underworld, and the Crone "
            "Goddess rules the longest nights. It is a time of divination, remembrance, endings, "
            "and the profound mystery of death and rebirth."
        ),
        "traditions": "Ancestor altars, divination, dumb supper, jack-o-lanterns, spirit communication",
    },
]

# ── Zodiac Signs ─────────────────────────────────────────────────────

ZODIAC = [
    {
        "name": "Aries", "symbol": "♈", "element": "Fire", "quality": "Cardinal", "ruler": "Mars",
        "start_month": 3, "start_day": 21, "end_month": 4, "end_day": 19,
        "description": (
            "The Ram — bold, pioneering, and courageous. Aries initiates the zodiacal year with "
            "fiery independence, daring leadership, and an irrepressible drive to forge new paths."
        ),
    },
    {
        "name": "Taurus", "symbol": "♉", "element": "Earth", "quality": "Fixed", "ruler": "Venus",
        "start_month": 4, "start_day": 20, "end_month": 5, "end_day": 20,
        "description": (
            "The Bull — steadfast, sensual, and grounded. Taurus savors the material world with "
            "patience and determination, finding beauty in stability, nature, and life's earthly pleasures."
        ),
    },
    {
        "name": "Gemini", "symbol": "♊", "element": "Air", "quality": "Mutable", "ruler": "Mercury",
        "start_month": 5, "start_day": 21, "end_month": 6, "end_day": 20,
        "description": (
            "The Twins — curious, adaptable, and communicative. Gemini bridges worlds with quicksilver "
            "wit, an insatiable thirst for knowledge, and a gift for weaving connections between ideas."
        ),
    },
    {
        "name": "Cancer", "symbol": "♋", "element": "Water", "quality": "Cardinal", "ruler": "Moon",
        "start_month": 6, "start_day": 21, "end_month": 7, "end_day": 22,
        "description": (
            "The Crab — nurturing, intuitive, and protective. Cancer holds the mysteries of home, "
            "memory, and the tides of emotion, guarding those they love with fierce devotion."
        ),
    },
    {
        "name": "Leo", "symbol": "♌", "element": "Fire", "quality": "Fixed", "ruler": "Sun",
        "start_month": 7, "start_day": 23, "end_month": 8, "end_day": 22,
        "description": (
            "The Lion — radiant, creative, and generous. Leo shines with the warmth of the Sun itself, "
            "commanding stages and hearts with dramatic flair and wholehearted loyalty."
        ),
    },
    {
        "name": "Virgo", "symbol": "♍", "element": "Earth", "quality": "Mutable", "ruler": "Mercury",
        "start_month": 8, "start_day": 23, "end_month": 9, "end_day": 22,
        "description": (
            "The Maiden — analytical, devoted, and skilled. Virgo serves the world through craft and "
            "discernment, weaving order from chaos with humble precision and quiet mastery."
        ),
    },
    {
        "name": "Libra", "symbol": "♎", "element": "Air", "quality": "Cardinal", "ruler": "Venus",
        "start_month": 9, "start_day": 23, "end_month": 10, "end_day": 22,
        "description": (
            "The Scales — harmonious, diplomatic, and aesthetic. Libra seeks balance and beauty in "
            "all things, mediating opposites and bringing grace to relationships and art alike."
        ),
    },
    {
        "name": "Scorpio", "symbol": "♏", "element": "Water", "quality": "Fixed", "ruler": "Pluto / Mars",
        "start_month": 10, "start_day": 23, "end_month": 11, "end_day": 21,
        "description": (
            "The Scorpion — intense, transformative, and perceptive. Scorpio plumbs the deepest waters "
            "of the psyche, fearlessly confronting shadows and emerging reborn through sheer force of will."
        ),
    },
    {
        "name": "Sagittarius", "symbol": "♐", "element": "Fire", "quality": "Mutable", "ruler": "Jupiter",
        "start_month": 11, "start_day": 22, "end_month": 12, "end_day": 21,
        "description": (
            "The Archer — adventurous, philosophical, and free. Sagittarius aims arrows at distant "
            "horizons, seeking truth, meaning, and the expansion of the spirit through exploration."
        ),
    },
    {
        "name": "Capricorn", "symbol": "♑", "element": "Earth", "quality": "Cardinal", "ruler": "Saturn",
        "start_month": 12, "start_day": 22, "end_month": 1, "end_day": 19,
        "description": (
            "The Sea-Goat — ambitious, disciplined, and wise. Capricorn ascends the mountain of "
            "achievement with patient resolve, mastering time and structure to build enduring legacies."
        ),
    },
    {
        "name": "Aquarius", "symbol": "♒", "element": "Air", "quality": "Fixed", "ruler": "Uranus / Saturn",
        "start_month": 1, "start_day": 20, "end_month": 2, "end_day": 18,
        "description": (
            "The Water-Bearer — visionary, humanitarian, and unconventional. Aquarius pours forth "
            "the waters of innovation and collective consciousness, dreaming the future into being."
        ),
    },
    {
        "name": "Pisces", "symbol": "♓", "element": "Water", "quality": "Mutable", "ruler": "Neptune / Jupiter",
        "start_month": 2, "start_day": 19, "end_month": 3, "end_day": 20,
        "description": (
            "The Fish — mystical, compassionate, and transcendent. Pisces dissolves boundaries between "
            "self and cosmos, channeling the infinite through dreams, art, and boundless empathy."
        ),
    },
]

# ── Moon Phases ──────────────────────────────────────────────────────

MOON_PHASES = [
    {"name": "New Moon", "emoji": "🌑",
     "magick": "New beginnings, intention setting, banishing, shadow work",
     "description": (
         "The Moon is dark, conjunct the Sun. A time for new beginnings, setting intentions, "
         "and planting seeds of manifestation. The Goddess is in her Dark Moon aspect — rest, "
         "dream, and look inward."
     )},
    {"name": "Waxing Crescent", "emoji": "🌒",
     "magick": "Attraction, courage, hope, building plans",
     "description": (
         "A sliver of light emerges. Energy builds as the seeds of intention take root. "
         "This is a time of hope, faith, and gentle forward momentum."
     )},
    {"name": "First Quarter", "emoji": "🌓",
     "magick": "Strength, determination, overcoming obstacles",
     "description": (
         "The Moon is half-lit and growing. Challenges arise that test your intentions. "
         "Take decisive action, overcome obstacles, and commit to your path."
     )},
    {"name": "Waxing Gibbous", "emoji": "🌔",
     "magick": "Refinement, patience, adjustment, nurturing growth",
     "description": (
         "Nearly full, the Moon swells with power. Refine and adjust your intentions. "
         "Patience and trust are key as things build toward their peak."
     )},
    {"name": "Full Moon", "emoji": "🌕",
     "magick": "Manifestation, divination, charging crystals, healing, abundance",
     "description": (
         "The Moon shines at maximum brilliance, fully illuminated by the Sun. The Goddess is "
         "in her Mother aspect — abundant, powerful, and fertile. Emotions and psychic abilities "
         "peak. Magic is at its most potent."
     )},
    {"name": "Waning Gibbous", "emoji": "🌖",
     "magick": "Gratitude, sharing knowledge, introspection, forgiveness",
     "description": (
         "The light begins to recede. A time for gratitude, sharing wisdom, and giving back. "
         "Reflect on what the Full Moon revealed."
     )},
    {"name": "Third Quarter", "emoji": "🌗",
     "magick": "Release, letting go, banishing, breaking habits",
     "description": (
         "Half-lit and diminishing. Release what no longer serves you. Break bad habits, "
         "let go of negativity, and clear space for the new."
     )},
    {"name": "Waning Crescent", "emoji": "🌘",
     "magick": "Rest, surrender, wisdom, psychic visions, closure",
     "description": (
         "The last thin crescent before darkness. The Goddess is in her Crone aspect — wise, "
         "still, and introspective. Surrender, rest, recuperate, and prepare for rebirth."
     )},
]

# ── Planets ──────────────────────────────────────────────────────────

PLANETS = [
    {"name": "Sun", "symbol": "☉", "color": "#e8c55a",
     "L0": 280.46646, "rate": 36000.76983, "L1": 0.0003032},
    {"name": "Moon", "symbol": "☽", "color": "#b8c4d0",
     "L0": 218.3165, "rate": 481267.8813, "L1": 0},
    {"name": "Mercury", "symbol": "☿", "color": "#a0a8b0",
     "L0": 252.2509, "rate": 149472.6746, "L1": 0},
    {"name": "Venus", "symbol": "♀", "color": "#d4a0c0",
     "L0": 181.9798, "rate": 58517.8157, "L1": 0},
    {"name": "Mars", "symbol": "♂", "color": "#c05040",
     "L0": 355.4330, "rate": 19140.2993, "L1": 0},
    {"name": "Jupiter", "symbol": "♃", "color": "#c4a060",
     "L0": 34.3515, "rate": 3034.9057, "L1": 0},
    {"name": "Saturn", "symbol": "♄", "color": "#8a8a6a",
     "L0": 50.0774, "rate": 1222.1138, "L1": 0},
    {"name": "Uranus", "symbol": "♅", "color": "#60b8c4",
     "L0": 314.055, "rate": 428.467, "L1": 0},
    {"name": "Neptune", "symbol": "♆", "color": "#5070b0",
     "L0": 304.349, "rate": 218.486, "L1": 0},
    {"name": "Pluto", "symbol": "⯓", "color": "#906070",
     "L0": 238.929, "rate": 145.205, "L1": 0},
]

# ── Solar Cycle ──────────────────────────────────────────────────────

SOLAR_CYCLE = {
    "cycle_number": 25,
    "minimum_year": 2019,
    "minimum_month": 12,
    "maximum_year": 2025,
    "maximum_month": 7,
    "next_minimum_year": 2030,
    "next_minimum_month": 6,
}

# ── Seasons ──────────────────────────────────────────────────────────

SEASONS = {
    "Spring": {
        "months": [3, 4, 5],
        "icon": "mdi:flower",
        "emoji": "🌱",
        "description": "The season of awakening and renewal.",
        "long_description": (
            "The season of awakening and renewal. The God grows as a youth, and the Maiden "
            "Goddess dances the land into bloom. Day overtakes night, seeds germinate, and "
            "the world surges with fresh vitality. In the Craft, spring is a time for new "
            "projects, cleansing rituals, and spells of growth."
        ),
    },
    "Summer": {
        "months": [6, 7, 8],
        "icon": "mdi:white-balance-sunny",
        "emoji": "☀️",
        "description": "The season of fullness and abundance.",
        "long_description": (
            "The season of fullness and abundance. The Sun God reigns at his zenith, and the "
            "Goddess is lush and fertile in her Mother aspect. Long days pour golden light upon "
            "flourishing gardens. Magic is strong, herbs are gathered, and the fae are most active. "
            "A time for love, passion, and joyful celebration."
        ),
    },
    "Autumn": {
        "months": [9, 10, 11],
        "icon": "mdi:leaf-maple",
        "emoji": "🍂",
        "description": "The season of harvest and reflection.",
        "long_description": (
            "The season of harvest and reflection. The God prepares to enter the underworld as "
            "the Goddess turns toward her Crone wisdom. Leaves blaze and fall, fruits ripen, and "
            "the veil between worlds thins. It is a time for gratitude, preservation, divination, "
            "and honoring what must be released."
        ),
    },
    "Winter": {
        "months": [12, 1, 2],
        "icon": "mdi:snowflake",
        "emoji": "❄️",
        "description": "The season of stillness and introspection.",
        "long_description": (
            "The season of stillness and introspection. The Crone Goddess holds vigil over the "
            "longest nights while the God rests in the underworld, awaiting rebirth at Yule. The "
            "bare land sleeps beneath frost and snow. It is a time for inner work, dreamcraft, "
            "hearthcraft, and the quiet gathering of wisdom."
        ),
    },
}
