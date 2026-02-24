/**
 * Wheel of the Year — Custom Lovelace Card for Home Assistant
 * v1.1.0
 *
 * Renders the full interactive Wheel of the Year visualization,
 * reading live data from the wheel_of_the_year integration sensors.
 *
 * Features:
 *   - Months ring (outermost) with current month highlight
 *   - Days ring with today marker
 *   - Zodiac ring with element coloring
 *   - Sabbat ring with gradient fills
 *   - Individual planet orbit rings
 *   - Solar Cycle 25 ring
 *   - Animated moon phase in center
 *   - Date marker line
 *   - Hover tooltips for all elements
 *   - Info panels: moon, sun sign, sabbat countdowns, planets, season
 */

const SABBATS = [
  { name: 'Yule', icon: '🕯️', color: '#6ba3c7', darkColor: '#2a4a5c' },
  { name: 'Imbolc', icon: '🔥', color: '#e8e0d0', darkColor: '#5a5548' },
  { name: 'Ostara', icon: '🌱', color: '#7cc47e', darkColor: '#2d5a2f' },
  { name: 'Beltane', icon: '🌸', color: '#e05a80', darkColor: '#6a2040' },
  { name: 'Litha', icon: '☀️', color: '#e8c55a', darkColor: '#6a5a20' },
  { name: 'Lughnasadh', icon: '🌾', color: '#d4943a', darkColor: '#5a3e14' },
  { name: 'Mabon', icon: '🍂', color: '#c46030', darkColor: '#5a2a14' },
  { name: 'Samhain', icon: '🎃', color: '#9050a0', darkColor: '#3a1848' },
];

const ZODIAC = [
  { name: 'Aries', symbol: '♈', element: 'Fire' },
  { name: 'Taurus', symbol: '♉', element: 'Earth' },
  { name: 'Gemini', symbol: '♊', element: 'Air' },
  { name: 'Cancer', symbol: '♋', element: 'Water' },
  { name: 'Leo', symbol: '♌', element: 'Fire' },
  { name: 'Virgo', symbol: '♍', element: 'Earth' },
  { name: 'Libra', symbol: '♎', element: 'Air' },
  { name: 'Scorpio', symbol: '♏', element: 'Water' },
  { name: 'Sagittarius', symbol: '♐', element: 'Fire' },
  { name: 'Capricorn', symbol: '♑', element: 'Earth' },
  { name: 'Aquarius', symbol: '♒', element: 'Air' },
  { name: 'Pisces', symbol: '♓', element: 'Water' },
];

const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const MONTH_NAMES_FULL = ['January','February','March','April','May','June','July','August','September','October','November','December'];

const MONTH_COLORS = [
  'rgba(100,140,200,0.20)', 'rgba(120,130,180,0.20)', 'rgba(100,170,100,0.20)',
  'rgba(120,190,110,0.20)', 'rgba(160,200,90,0.20)',  'rgba(210,190,60,0.20)',
  'rgba(220,170,50,0.20)',  'rgba(210,140,50,0.20)',  'rgba(190,110,50,0.20)',
  'rgba(160,80,60,0.20)',   'rgba(120,70,90,0.20)',   'rgba(80,100,150,0.20)',
];

const PLANET_RING_NAMES = ['Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto'];

class WheelOfTheYearCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this._initialized) {
      this._init();
      this._initialized = true;
    }
    this._update();
  }

  setConfig(config) {
    this._config = {
      entity: config.entity || 'sensor.wheel_of_the_year_wheel_state',
      title: config.title,
      show_title: config.show_title !== false,
      show_info_panels: config.show_info_panels !== false,
      show_stars: config.show_stars !== false,
      size: config.size || 'auto',
      ...config,
    };
  }

  getCardSize() {
    return this._config.show_info_panels ? 14 : 8;
  }

  static getConfigElement() {
    return document.createElement('wheel-of-the-year-card-editor');
  }

  static getStubConfig() {
    return {
      entity: 'sensor.wheel_of_the_year_wheel_state',
      show_title: true,
      show_info_panels: true,
      show_stars: true,
    };
  }

  _init() {
    this.attachShadow({ mode: 'open' });

    const style = document.createElement('style');
    style.textContent = `
      :host { display: block; }
      .card {
        background: linear-gradient(145deg, #0a0e14, #0d1520);
        border-radius: 12px;
        padding: 16px;
        position: relative;
        overflow: hidden;
        color: #e8dcc8;
        font-family: Georgia, 'Times New Roman', serif;
      }
      .stars {
        position: absolute; inset: 0; overflow: hidden; pointer-events: none;
      }
      .star {
        position: absolute; border-radius: 50%; background: white;
        animation: twinkle var(--dur) ease-in-out infinite alternate;
      }
      @keyframes twinkle {
        0% { opacity: var(--min-o, 0.1); transform: scale(1); }
        100% { opacity: var(--max-o, 0.8); transform: scale(1.3); }
      }
      .title {
        text-align: center; font-size: 1.4em; font-weight: 700;
        color: #c9a84c; letter-spacing: 0.12em;
        text-shadow: 0 0 20px rgba(201,168,76,0.3);
        margin-bottom: 4px; position: relative; z-index: 1;
      }
      .subtitle {
        text-align: center; font-size: 0.85em; color: #b8c4d0;
        font-style: italic; letter-spacing: 0.15em;
        margin-bottom: 12px; position: relative; z-index: 1;
      }
      .wheel-container {
        display: flex; justify-content: center;
        position: relative; z-index: 1;
      }
      canvas { max-width: 100%; display: block; }

      /* ── Info Grid ── */
      .info-grid {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 10px; margin-top: 14px;
        position: relative; z-index: 1;
      }
      @media (max-width: 500px) { .info-grid { grid-template-columns: 1fr; } }
      .info-panel {
        background: rgba(18,15,10,0.85);
        border: 1px solid rgba(201,168,76,0.18);
        border-radius: 8px; padding: 10px 12px;
        position: relative; overflow: hidden;
      }
      .info-panel::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0;
        height: 1.5px;
        background: linear-gradient(90deg, transparent, rgba(201,168,76,0.3), transparent);
      }
      .info-panel h3 {
        font-size: 0.82em; color: #c9a84c; letter-spacing: 0.08em;
        margin-bottom: 6px; text-align: center; font-weight: 600;
        margin-top: 0;
      }
      .info-value {
        font-size: 0.9em; text-align: center; color: #e8dcc8; line-height: 1.5;
      }
      .info-value .big { font-size: 1.6em; display: block; margin-bottom: 2px; }
      .info-value .label { color: #c9a84c; font-weight: 600; }
      .info-value .detail { font-size: 0.85em; color: #b8c4d0; font-style: italic; }

      /* ── Countdown rows ── */
      .countdown-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 3px 6px; border-radius: 4px; margin-bottom: 2px; font-size: 0.78em;
      }
      .countdown-row.is-next {
        background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.25);
      }
      .countdown-row .name { color: #c9a84c; font-weight: 600; }
      .countdown-row .days { color: #b8c4d0; }
      .countdown-row .days .time-d { color: #c05040; margin-left: 1px; }
      .countdown-row .days .time-h { color: #6ba3c7; margin-left: 1px; }
      .countdown-row .days .time-m { color: #8a6f2f; margin-left: 1px; }

      /* ── Planet rows ── */
      .planet-row {
        display: flex; align-items: center; gap: 6px;
        padding: 2px 4px; font-size: 0.78em;
      }
      .planet-row .psym { font-size: 1em; width: 1.2em; text-align: center; }
      .planet-row .pname { color: #e8dcc8; }
      .planet-row .psign { color: #c9a84c; }

      /* ── Tooltip ── */
      .tooltip {
        position: fixed; z-index: 10000;
        background: rgba(15,12,8,0.97);
        border: 1px solid rgba(201,168,76,0.35);
        border-radius: 8px; padding: 10px 14px;
        max-width: 320px; pointer-events: none;
        opacity: 0; transition: opacity 0.2s ease;
        box-shadow: 0 6px 24px rgba(0,0,0,0.6);
      }
      .tooltip.visible { opacity: 1; }
      .tooltip h4 { color: #c9a84c; margin: 0 0 4px; font-size: 0.95em; }
      .tooltip .tip-date { color: #b87333; font-style: italic; font-size: 0.82em; margin-bottom: 4px; }
      .tooltip p { font-size: 0.85em; line-height: 1.5; color: #e8dcc8; margin: 0; white-space: pre-line; }
      .tooltip .tip-sym { font-size: 1.4em; text-align: center; margin-bottom: 2px; }
    `;
    this.shadowRoot.appendChild(style);

    const card = document.createElement('div');
    card.className = 'card';
    this._card = card;

    // Stars
    if (this._config.show_stars) {
      const stars = document.createElement('div');
      stars.className = 'stars';
      for (let i = 0; i < 80; i++) {
        const s = document.createElement('div');
        s.className = 'star';
        const sz = Math.random() * 2 + 0.5;
        s.style.cssText = `width:${sz}px;height:${sz}px;left:${Math.random()*100}%;top:${Math.random()*100}%;--dur:${2+Math.random()*5}s;--min-o:${Math.random()*0.15};--max-o:${0.3+Math.random()*0.5};animation-delay:${Math.random()*5}s;`;
        stars.appendChild(s);
      }
      card.appendChild(stars);
    }

    // Title
    if (this._config.show_title) {
      const title = document.createElement('div');
      title.className = 'title';
      title.textContent = this._config.title || 'The Wheel of the Year';
      card.appendChild(title);
      this._subtitleEl = document.createElement('div');
      this._subtitleEl.className = 'subtitle';
      card.appendChild(this._subtitleEl);
    }

    // Canvas
    const wheelDiv = document.createElement('div');
    wheelDiv.className = 'wheel-container';
    this._canvas = document.createElement('canvas');
    wheelDiv.appendChild(this._canvas);
    card.appendChild(wheelDiv);

    // Tooltip
    this._tooltip = document.createElement('div');
    this._tooltip.className = 'tooltip';
    this._tooltip.innerHTML = `
      <div class="tip-sym" id="tsym"></div>
      <h4 id="ttitle"></h4>
      <div class="tip-date" id="tdate"></div>
      <p id="tdesc"></p>
    `;
    card.appendChild(this._tooltip);

    // Info panels
    if (this._config.show_info_panels) {
      this._infoGrid = document.createElement('div');
      this._infoGrid.className = 'info-grid';
      card.appendChild(this._infoGrid);
    }

    this.shadowRoot.appendChild(card);

    this._hitZones = [];
    this._canvas.addEventListener('mousemove', (e) => this._onMouseMove(e));
    this._canvas.addEventListener('mouseleave', () => this._hideTooltip());
    this._canvas.addEventListener('touchstart', (e) => {
      const t = e.touches[0];
      this._onMouseMove({ clientX: t.clientX, clientY: t.clientY });
    }, { passive: true });
    this._canvas.addEventListener('touchend', () => this._hideTooltip());

    this._ro = new ResizeObserver(() => this._draw());
    this._ro.observe(this._card);
  }

  _update() {
    if (!this._hass || !this._config) return;
    const entity = this._hass.states[this._config.entity];
    if (!entity) return;
    this._stateAttrs = entity.attributes || {};

    if (this._subtitleEl) {
      const now = new Date();
      this._subtitleEl.textContent = now.toLocaleDateString('en-US', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
        hour: 'numeric', minute: '2-digit'
      });
    }

    this._draw();
    if (this._infoGrid) this._updateInfoPanels();
  }

  // ════════════════════════════════════════════════════════════
  // DRAWING
  // ════════════════════════════════════════════════════════════

  _draw() {
    const c = this._canvas;
    const wrapper = c.parentElement;
    if (!wrapper) return;

    const maxSize = this._config.size === 'auto' ? wrapper.clientWidth : parseInt(this._config.size);
    const size = Math.min(maxSize, 780);
    if (size <= 0) return;

    const dpr = window.devicePixelRatio || 1;
    c.width = size * dpr;
    c.height = size * dpr;
    c.style.width = size + 'px';
    c.style.height = size + 'px';

    const ctx = c.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, size, size);

    const CX = size / 2;
    const CY = size / 2;
    const R = size / 2 - 10;

    this._CX = CX;
    this._CY = CY;
    this._R = R;
    this._hitZones = [];

    // Ring radii (outside → in)
    const monthsOuter = R;
    const monthsInner = R * 0.94;
    const daysOuter = monthsInner;
    const daysInner = R * 0.88;
    const zodiacOuter = daysInner;
    const zodiacInner = R * 0.76;
    const sabbatOuter = zodiacInner;
    const sabbatInner = R * 0.52;
    const innerCircle = R * 0.48;
    const centerR = R * 0.19;
    const solarRingInner = centerR + R * 0.015;
    const solarRingOuter = centerR + R * 0.05;

    // Planet rings
    const planetRingStart = solarRingOuter + R * 0.015;
    const planetRingEnd = innerCircle - R * 0.01;
    const planetRingSpacing = (planetRingEnd - planetRingStart) / PLANET_RING_NAMES.length;
    const planetRings = PLANET_RING_NAMES.map((_, i) => planetRingStart + planetRingSpacing * (i + 0.5));

    const now = new Date();
    const year = now.getFullYear();
    const isLeap = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    const totalDays = isLeap ? 366 : 365;
    const yuleDay = isLeap ? 356 : 355;
    const currentMonth = now.getMonth() + 1;

    const dayOfYear = (d) => {
      const start = new Date(d.getFullYear(), 0, 0);
      return Math.floor((d - start) / 86400000);
    };
    const currentDOY = dayOfYear(now);

    const doyForDate = (m, d) => {
      const dt = new Date(year, m - 1, d);
      const start = new Date(year, 0, 0);
      return Math.floor((dt - start) / 86400000);
    };

    const wheelAngleForDoy = (doy) => {
      const shifted = (doy - yuleDay + totalDays) % totalDays;
      return (shifted / totalDays) * 360;
    };

    // ── Outer glow ──
    const glow = ctx.createRadialGradient(CX, CY, R * 0.4, CX, CY, R * 1.05);
    glow.addColorStop(0, 'rgba(201,168,76,0.02)');
    glow.addColorStop(0.7, 'rgba(201,168,76,0.04)');
    glow.addColorStop(1, 'transparent');
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, size, size);

    // ── Months Ring ──
    const MONTHS = [
      { name: 'Jan', days: 31, month: 1 }, { name: 'Feb', days: isLeap ? 29 : 28, month: 2 },
      { name: 'Mar', days: 31, month: 3 }, { name: 'Apr', days: 30, month: 4 },
      { name: 'May', days: 31, month: 5 }, { name: 'Jun', days: 30, month: 6 },
      { name: 'Jul', days: 31, month: 7 }, { name: 'Aug', days: 31, month: 8 },
      { name: 'Sep', days: 30, month: 9 }, { name: 'Oct', days: 31, month: 10 },
      { name: 'Nov', days: 30, month: 11 }, { name: 'Dec', days: 31, month: 12 },
    ];

    for (let mi = 0; mi < 12; mi++) {
      const m = MONTHS[mi];
      const startDoy = doyForDate(m.month, 1);
      const nextMonth = m.month === 12 ? 1 : m.month + 1;
      const endDoy = m.month === 12 ? doyForDate(12, 31) + 1 : doyForDate(nextMonth, 1);
      const startDeg = wheelAngleForDoy(startDoy) - 90;
      const endDeg = wheelAngleForDoy(endDoy === 0 ? totalDays : endDoy) - 90;
      let startRad = startDeg * Math.PI / 180;
      let endRad = endDeg * Math.PI / 180;
      if (endRad < startRad) endRad += Math.PI * 2;

      ctx.beginPath();
      ctx.arc(CX, CY, monthsOuter, startRad, endRad);
      ctx.arc(CX, CY, monthsInner, endRad, startRad, true);
      ctx.closePath();

      const isCurrent = m.month === currentMonth;
      ctx.fillStyle = isCurrent
        ? MONTH_COLORS[mi].replace('0.20', '0.40')
        : MONTH_COLORS[mi];
      ctx.fill();
      ctx.strokeStyle = 'rgba(201,168,76,0.2)';
      ctx.lineWidth = 0.5;
      ctx.stroke();

      // Label
      const midRad = (startRad + endRad) / 2;
      const labelR = (monthsOuter + monthsInner) / 2;
      const lx = CX + Math.cos(midRad) * labelR;
      const ly = CY + Math.sin(midRad) * labelR;
      ctx.save();
      ctx.translate(lx, ly);
      const textRot = midRad + Math.PI / 2;
      if ([3,4,5,6,7].includes(mi)) ctx.rotate(textRot - Math.PI);
      else ctx.rotate(textRot);
      ctx.font = `600 ${R * 0.03}px Georgia, serif`;
      ctx.fillStyle = isCurrent ? 'rgba(232,197,90,0.95)' : 'rgba(201,168,76,0.6)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(m.name, 0, 0);
      ctx.restore();

      this._hitZones.push({
        type: 'month', index: mi,
        startAngle: startRad % (Math.PI * 2),
        endAngle: endRad % (Math.PI * 2),
        innerR: monthsInner, outerR: monthsOuter,
        data: m,
      });
    }

    // Months outer border
    ctx.beginPath(); ctx.arc(CX, CY, monthsOuter, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(201,168,76,0.45)'; ctx.lineWidth = 2; ctx.stroke();

    // ── Days Ring ──
    const dayArcSpan = 360 / totalDays;
    const dayGap = 0.15;
    for (let d = 1; d <= totalDays; d++) {
      const startDeg = wheelAngleForDoy(d) - 90 - dayArcSpan / 2 + dayGap / 2;
      const endDeg = startDeg + dayArcSpan - dayGap;
      const startRad = startDeg * Math.PI / 180;
      const endRad = endDeg * Math.PI / 180;

      ctx.beginPath();
      ctx.arc(CX, CY, daysOuter - 1, startRad, endRad);
      ctx.arc(CX, CY, daysInner + 1, endRad, startRad, true);
      ctx.closePath();

      const isToday = d === currentDOY;
      if (isToday) {
        ctx.fillStyle = 'rgba(255,220,100,0.8)';
        ctx.shadowColor = 'rgba(255,220,100,0.5)';
        ctx.shadowBlur = 6;
      } else {
        ctx.fillStyle = d % 2 === 0
          ? 'rgba(201,168,76,0.08)' : 'rgba(201,168,76,0.04)';
        ctx.shadowBlur = 0;
      }
      ctx.fill();
      ctx.shadowBlur = 0;

      if (d % 7 === 0 && !isToday) {
        ctx.fillStyle = 'rgba(201,168,76,0.15)';
        ctx.fill();
      }
    }

    // Days ring borders
    ctx.beginPath(); ctx.arc(CX, CY, daysOuter, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(201,168,76,0.3)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX, CY, daysInner, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(201,168,76,0.3)'; ctx.lineWidth = 1; ctx.stroke();

    // ── Zodiac Ring ──
    for (let i = 0; i < 12; i++) {
      const startDeg = this._zodiacStartAngle(i) - 90;
      const endDeg = startDeg + 30;
      const startRad = startDeg * Math.PI / 180;
      const endRad = endDeg * Math.PI / 180;

      const elem = ZODIAC[i].element;
      let fill;
      if (elem === 'Fire') fill = 'rgba(180,60,30,0.15)';
      else if (elem === 'Earth') fill = 'rgba(60,120,50,0.15)';
      else if (elem === 'Air') fill = 'rgba(100,140,180,0.15)';
      else fill = 'rgba(50,80,160,0.15)';

      ctx.beginPath();
      ctx.arc(CX, CY, zodiacOuter, startRad, endRad);
      ctx.arc(CX, CY, zodiacInner, endRad, startRad, true);
      ctx.closePath();
      ctx.fillStyle = fill;
      ctx.fill();
      ctx.strokeStyle = 'rgba(201,168,76,0.25)';
      ctx.lineWidth = 0.5;
      ctx.stroke();

      const midAngle = (startDeg + 15) * Math.PI / 180;
      const lr = (zodiacOuter + zodiacInner) / 2;
      ctx.font = `${R * 0.055}px serif`;
      ctx.fillStyle = 'rgba(201,168,76,0.8)';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(ZODIAC[i].symbol, CX + Math.cos(midAngle) * lr, CY + Math.sin(midAngle) * lr);

      this._hitZones.push({
        type: 'zodiac', index: i,
        startAngle: startRad, endAngle: endRad,
        innerR: zodiacInner, outerR: zodiacOuter,
      });
    }

    // ── Sabbat Ring ──
    for (let i = 0; i < 8; i++) {
      const startDeg = i * 45 - 90 - 22.5;
      const endDeg = startDeg + 45;
      const startRad = startDeg * Math.PI / 180;
      const endRad = endDeg * Math.PI / 180;
      const sabbat = SABBATS[i];

      ctx.beginPath();
      ctx.arc(CX, CY, sabbatOuter, startRad, endRad);
      ctx.arc(CX, CY, sabbatInner, endRad, startRad, true);
      ctx.closePath();

      const midAngle = (startDeg + 22.5) * Math.PI / 180;
      const gx = CX + Math.cos(midAngle) * sabbatOuter * 0.5;
      const gy = CY + Math.sin(midAngle) * sabbatOuter * 0.5;
      const grad = ctx.createRadialGradient(gx, gy, 0, CX, CY, sabbatOuter);
      grad.addColorStop(0, sabbat.darkColor + '60');
      grad.addColorStop(1, sabbat.darkColor + '20');
      ctx.fillStyle = grad;
      ctx.fill();
      ctx.strokeStyle = 'rgba(201,168,76,0.2)';
      ctx.lineWidth = 0.5;
      ctx.stroke();

      // Icon
      const iconR = (sabbatOuter + sabbatInner) / 2 + R * 0.05;
      const iconAngle = (startDeg + 22.5) * Math.PI / 180;
      const ix = CX + Math.cos(iconAngle) * iconR;
      const iy = CY + Math.sin(iconAngle) * iconR;
      ctx.font = `${R * 0.06}px serif`;
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(sabbat.icon, ix, iy);

      // Name
      const nameR = (sabbatOuter + sabbatInner) / 2 - R * 0.055;
      ctx.save();
      const nx = CX + Math.cos(iconAngle) * nameR;
      const ny = CY + Math.sin(iconAngle) * nameR;
      ctx.translate(nx, ny);
      const tr = iconAngle + Math.PI / 2;
      if (iconAngle > 0 && iconAngle < Math.PI) ctx.rotate(tr - Math.PI);
      else ctx.rotate(tr);
      ctx.font = `600 ${R * 0.04}px Georgia, serif`;
      ctx.fillStyle = sabbat.color;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(sabbat.name, 0, 0);
      ctx.restore();

      this._hitZones.push({
        type: 'sabbat', index: i,
        startAngle: startRad, endAngle: endRad,
        innerR: sabbatInner, outerR: sabbatOuter,
      });
    }

    // ── Ring Borders ──
    ctx.beginPath(); ctx.arc(CX, CY, innerCircle, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(201,168,76,0.3)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX, CY, sabbatOuter, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(201,168,76,0.35)'; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX, CY, zodiacOuter, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(201,168,76,0.35)'; ctx.lineWidth = 1.5; ctx.stroke();

    // ── Solar Cycle Ring ──
    const solarData = this._stateAttrs.solar_cycle || {};
    for (let deg = 0; deg < 360; deg += 1) {
      const rad1 = (deg - 90) * Math.PI / 180;
      const rad2 = (deg - 89) * Math.PI / 180;
      const t = (1 + Math.cos(deg * Math.PI / 180)) / 2;
      const r = Math.round(60 + 180 * t);
      const g = Math.round(30 + 100 * t);
      const b = Math.round(10 + 20 * t);
      const a = 0.08 + 0.15 * t;
      ctx.beginPath();
      ctx.arc(CX, CY, solarRingOuter, rad1, rad2);
      ctx.arc(CX, CY, solarRingInner, rad2, rad1, true);
      ctx.closePath();
      ctx.fillStyle = `rgba(${r},${g},${b},${a})`;
      ctx.fill();
    }

    ctx.beginPath(); ctx.arc(CX, CY, solarRingOuter, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(232,160,50,0.2)'; ctx.lineWidth = 0.5; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX, CY, solarRingInner, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(232,160,50,0.2)'; ctx.lineWidth = 0.5; ctx.stroke();

    // Solar marker
    const solarProgress = solarData.progress || 0;
    const solarPhase = solarData.phase || 0;
    let solarAngleDeg;
    if (solarProgress <= 0.5) {
      solarAngleDeg = 180 - (solarProgress / 0.5) * 180;
    } else {
      solarAngleDeg = ((solarProgress - 0.5) / 0.5) * 180;
    }
    const solarAngleRad = (solarAngleDeg - 90) * Math.PI / 180;
    const solarMarkerR = (solarRingInner + solarRingOuter) / 2;
    const smx = CX + Math.cos(solarAngleRad) * solarMarkerR;
    const smy = CY + Math.sin(solarAngleRad) * solarMarkerR;

    ctx.save();
    ctx.shadowColor = `rgba(255,${Math.round(160 + 60 * solarPhase)},50,0.7)`;
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.arc(smx, smy, R * 0.015, 0, Math.PI * 2);
    const warmth = solarPhase;
    ctx.fillStyle = `rgb(${Math.round(200+55*warmth)},${Math.round(120+80*warmth)},${Math.round(30+30*warmth)})`;
    ctx.fill();
    ctx.restore();

    // ☉ and min labels
    ctx.font = `${R * 0.025}px serif`;
    ctx.fillStyle = 'rgba(232,197,90,0.4)';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('☉', CX, CY - solarMarkerR);
    ctx.fillStyle = 'rgba(150,130,90,0.25)';
    ctx.font = `${R * 0.018}px serif`;
    ctx.fillText('min', CX, CY + solarMarkerR);

    this._hitZones.push({
      type: 'solar_cycle',
      cx: smx, cy: smy,
      radius: R * 0.04,
      data: solarData,
    });

    // ── Planet Rings ──
    const planets = this._stateAttrs.planets || [];
    planetRings.forEach((pr, i) => {
      ctx.beginPath(); ctx.arc(CX, CY, pr, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(201,168,76,${0.05 + i * 0.008})`;
      ctx.lineWidth = 0.5; ctx.stroke();
    });

    planets.forEach((p) => {
      if (p.name === 'Sun' || p.name === 'Moon') return;
      const ringIdx = PLANET_RING_NAMES.indexOf(p.name);
      if (ringIdx === -1) return;

      const pr = planetRings[ringIdx];
      const eclipticToWheel = (p.longitude - 270 + 360) % 360;
      const aRad = (eclipticToWheel - 90) * Math.PI / 180;
      const px = CX + Math.cos(aRad) * pr;
      const py = CY + Math.sin(aRad) * pr;
      ctx.font = `${R * 0.032}px serif`;
      ctx.fillStyle = p.color || '#ccc';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(p.symbol, px, py);

      this._hitZones.push({
        type: 'planet',
        cx: px, cy: py,
        radius: R * 0.025,
        data: p,
      });
    });

    // ── Date Marker ──
    const currentAngle = this._dateToWheelAngle(now);
    const markerRad = (currentAngle - 90) * Math.PI / 180;
    ctx.save();
    ctx.strokeStyle = 'rgba(255,220,100,0.7)';
    ctx.lineWidth = 2;
    ctx.shadowColor = 'rgba(255,220,100,0.6)';
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.moveTo(CX + Math.cos(markerRad) * centerR, CY + Math.sin(markerRad) * centerR);
    ctx.lineTo(CX + Math.cos(markerRad) * monthsOuter, CY + Math.sin(markerRad) * monthsOuter);
    ctx.stroke();
    ctx.restore();

    const dotR = (sabbatOuter + sabbatInner) / 2;
    const dotX = CX + Math.cos(markerRad) * dotR;
    const dotY = CY + Math.sin(markerRad) * dotR;
    ctx.save();
    ctx.shadowColor = 'rgba(255,220,100,0.8)';
    ctx.shadowBlur = 15;
    ctx.beginPath(); ctx.arc(dotX, dotY, R * 0.02, 0, Math.PI * 2);
    ctx.fillStyle = '#ffdc64'; ctx.fill();
    ctx.restore();

    // ── Moon in Center ──
    const moonPhase = this._stateAttrs.moon_phase_number || 0;
    const centerGrad = ctx.createRadialGradient(CX, CY, 0, CX, CY, centerR);
    centerGrad.addColorStop(0, 'rgba(15,15,25,0.95)');
    centerGrad.addColorStop(1, 'rgba(10,10,18,0.9)');
    ctx.beginPath(); ctx.arc(CX, CY, centerR, 0, Math.PI * 2);
    ctx.fillStyle = centerGrad; ctx.fill();
    ctx.strokeStyle = 'rgba(201,168,76,0.3)'; ctx.lineWidth = 1.5; ctx.stroke();

    this._drawMoon(ctx, CX, CY - centerR * 0.12, centerR * 0.4, moonPhase);

    ctx.font = `500 ${R * 0.038}px Georgia, serif`;
    ctx.fillStyle = '#d0d8e4';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(this._stateAttrs.moon_phase || 'Moon', CX, CY + centerR * 0.42);

    const illum = this._stateAttrs.moon_illumination;
    if (illum != null) {
      ctx.font = `${R * 0.028}px Georgia, serif`;
      ctx.fillStyle = 'rgba(184,196,208,0.6)';
      ctx.fillText(`${Math.round(illum)}% illuminated`, CX, CY + centerR * 0.62);
    }

    // Moon hit zone
    this._hitZones.push({
      type: 'moon',
      cx: CX, cy: CY,
      radius: centerR,
    });
  }

  _drawMoon(ctx, x, y, r, phase) {
    ctx.save();
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = '#1a1a2e'; ctx.fill();
    ctx.strokeStyle = 'rgba(180,200,220,0.3)'; ctx.lineWidth = 1; ctx.stroke();

    ctx.beginPath();
    if (phase < 0.5) {
      const sweep = (0.5 - phase) * 2;
      ctx.arc(x, y, r, -Math.PI / 2, Math.PI / 2, false);
      const bx = r * Math.cos(Math.PI * sweep);
      ctx.ellipse(x, y, Math.abs(bx), r, 0, Math.PI / 2, -Math.PI / 2, sweep > 0.5);
    } else {
      const sweep = (phase - 0.5) * 2;
      ctx.arc(x, y, r, Math.PI / 2, -Math.PI / 2, false);
      const bx = r * Math.cos(Math.PI * sweep);
      ctx.ellipse(x, y, Math.abs(bx), r, 0, -Math.PI / 2, Math.PI / 2, sweep > 0.5);
    }
    ctx.closePath();
    const mg = ctx.createRadialGradient(x - r * 0.2, y - r * 0.2, 0, x, y, r);
    mg.addColorStop(0, '#e8eef4'); mg.addColorStop(0.5, '#c8d4e0'); mg.addColorStop(1, '#a0b0c0');
    ctx.fillStyle = mg; ctx.fill();
    ctx.restore();

    ctx.save();
    ctx.beginPath(); ctx.arc(x, y, r * 1.4, 0, Math.PI * 2);
    const gg = ctx.createRadialGradient(x, y, r * 0.8, x, y, r * 1.4);
    gg.addColorStop(0, 'rgba(200,212,224,0.08)'); gg.addColorStop(1, 'transparent');
    ctx.fillStyle = gg; ctx.fill();
    ctx.restore();
  }

  // ════════════════════════════════════════════════════════════
  // HELPERS
  // ════════════════════════════════════════════════════════════

  _zodiacStartAngle(index) {
    const capIdx = 9;
    const offset = (index - capIdx + 12) % 12;
    return offset * 30;
  }

  _dateToWheelAngle(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const doy = Math.floor((date - start) / 86400000);
    const isLeap = (date.getFullYear() % 4 === 0 && date.getFullYear() % 100 !== 0) || (date.getFullYear() % 400 === 0);
    const total = isLeap ? 366 : 365;
    const yuleDay = isLeap ? 356 : 355;
    const shifted = (doy - yuleDay + total) % total;
    return (shifted / total) * 360;
  }

  // ════════════════════════════════════════════════════════════
  // TOOLTIP / HOVER
  // ════════════════════════════════════════════════════════════

  _onMouseMove(e) {
    const rect = this._canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const zone = this._getHoveredZone(mx, my);

    if (zone) {
      this._canvas.style.cursor = 'pointer';
      let data = {};
      const sabbats = this._stateAttrs.sabbats || [];

      if (zone.type === 'sabbat') {
        const s = SABBATS[zone.index];
        const sd = sabbats[zone.index] || {};
        data = {
          sym: s.icon,
          title: `${s.name} — ${sd.alt_name || ''}`,
          date: sd.next_date ? `Next: ${sd.next_date}` : '',
          desc: (sd.description || '') + (sd.traditions ? '\n\nTraditions: ' + sd.traditions : ''),
        };
      } else if (zone.type === 'zodiac') {
        const z = ZODIAC[zone.index];
        data = { sym: z.symbol, title: z.name, date: z.element, desc: '' };
      } else if (zone.type === 'month') {
        const m = zone.data;
        const isCurrent = m.month === (new Date()).getMonth() + 1;
        data = {
          sym: '📅', title: MONTH_NAMES_FULL[m.month - 1],
          date: `${m.days} days`,
          desc: isCurrent ? 'Current month' : '',
        };
      } else if (zone.type === 'planet') {
        const p = zone.data;
        data = {
          sym: p.symbol,
          title: `${p.name} in ${p.sign_name}`,
          date: `${p.sign_symbol} ${p.sign_degree.toFixed(1)}° ${p.sign_name}`,
          desc: `${p.name} is currently transiting ${p.sign_name}.`,
        };
      } else if (zone.type === 'moon') {
        data = {
          sym: this._stateAttrs.moon_emoji || '🌙',
          title: this._stateAttrs.moon_phase || 'Moon',
          date: `${Math.round(this._stateAttrs.moon_illumination || 0)}% illuminated`,
          desc: (this._stateAttrs.moon_description || '') +
                (this._stateAttrs.moon_magick ? '\n\nMagick: ' + this._stateAttrs.moon_magick : ''),
        };
      } else if (zone.type === 'solar_cycle') {
        const sc = zone.data;
        data = {
          sym: '☉',
          title: `Solar Cycle ${sc.cycle_number || 25} — ${sc.label || ''}`,
          date: `Activity: ${((sc.phase || 0) * 100).toFixed(0)}% · Est. sunspots: ~${sc.sunspot_estimate || 0}`,
          desc: `Currently ${((sc.progress || 0) * 100).toFixed(0)}% through Cycle ${sc.cycle_number || 25}, with ~${sc.years_remaining || '?'} years until the next solar minimum.`,
        };
      }
      this._showTooltip(e.clientX, e.clientY, data);
    } else {
      this._canvas.style.cursor = 'default';
      this._hideTooltip();
    }
  }

  _getHoveredZone(mx, my) {
    // Check point-based zones first (planets, solar cycle)
    for (const zone of this._hitZones) {
      if (zone.type === 'planet' || zone.type === 'solar_cycle') {
        const dx = mx - zone.cx;
        const dy = my - zone.cy;
        if (dx * dx + dy * dy <= zone.radius * zone.radius * 4) return zone;
      }
    }

    // Check moon center
    for (const zone of this._hitZones) {
      if (zone.type === 'moon') {
        const dx = mx - zone.cx;
        const dy = my - zone.cy;
        if (dx * dx + dy * dy <= zone.radius * zone.radius) return zone;
      }
    }

    // Check ring zones
    const dx = mx - this._CX;
    const dy = my - this._CY;
    const dist = Math.sqrt(dx * dx + dy * dy);
    let angle = Math.atan2(dy, dx);

    for (const zone of this._hitZones) {
      if (['zodiac', 'sabbat', 'month'].includes(zone.type)) {
        if (dist >= zone.innerR && dist <= zone.outerR) {
          let a = ((angle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
          let s = ((zone.startAngle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
          let ee = ((zone.endAngle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
          if (s < ee) { if (a >= s && a <= ee) return zone; }
          else { if (a >= s || a <= ee) return zone; }
        }
      }
    }
    return null;
  }

  _showTooltip(x, y, data) {
    const t = this._tooltip;
    t.querySelector('#tsym').textContent = data.sym || '';
    t.querySelector('#ttitle').textContent = data.title || '';
    t.querySelector('#tdate').textContent = data.date || '';
    t.querySelector('#tdesc').textContent = data.desc || '';
    t.classList.add('visible');
    let tx = x + 14, ty = y - 8;
    if (tx + 300 > window.innerWidth) tx = x - 300;
    if (ty < 10) ty = 10;
    t.style.left = tx + 'px'; t.style.top = ty + 'px';
  }

  _hideTooltip() {
    this._tooltip.classList.remove('visible');
  }

  // ════════════════════════════════════════════════════════════
  // INFO PANELS
  // ════════════════════════════════════════════════════════════

  _updateInfoPanels() {
    const grid = this._infoGrid;
    if (!grid) return;
    const a = this._stateAttrs;
    const sabbats = a.sabbats || [];
    const planets = a.planets || [];
    const sc = a.solar_cycle || {};

    // Find next sabbat
    let nextIdx = 0, minDays = Infinity;
    sabbats.forEach((s, i) => { if (s.days_until < minDays) { minDays = s.days_until; nextIdx = i; } });

    // Build countdown HTML with hours/minutes
    const now = new Date();
    const countdownRows = sabbats.map((s, i) => {
      let timeStr;
      if (s.days_until === 0) {
        timeStr = '🎉 Today!';
      } else if (s.days_until <= 7) {
        timeStr = `${s.days_until}<span class="time-d">d</span>`;
      } else {
        timeStr = `${s.days_until}<span class="time-d">d</span>`;
      }
      return `<div class="countdown-row ${i === nextIdx ? 'is-next' : ''}">
        <span>${s.emoji} <span class="name">${s.name}</span></span>
        <span class="days">${timeStr}</span>
      </div>`;
    }).join('');

    // Build planet list
    const planetRows = planets.map(p => `
      <div class="planet-row">
        <span class="psym" style="color:${p.color || '#ccc'}">${p.symbol}</span>
        <span class="pname">${p.name}</span>
        <span class="psign">${p.sign_symbol} ${p.sign_name} ${p.sign_degree.toFixed(0)}°</span>
      </div>
    `).join('');

    grid.innerHTML = `
      <div class="info-panel">
        <h3>☽ Moon Phase</h3>
        <div class="info-value">
          <span class="big">${a.moon_emoji || '🌙'}</span>
          <span class="label">${a.moon_phase || ''}</span><br>
          <span class="detail">${a.moon_illumination != null ? Math.round(a.moon_illumination) + '% illuminated' : ''}</span>
          ${a.moon_magick ? '<br><span class="detail">Magick: ' + a.moon_magick + '</span>' : ''}
        </div>
      </div>
      <div class="info-panel">
        <h3>✦ Sun Sign</h3>
        <div class="info-value">
          <span class="big">${a.sun_sign_symbol || '☉'}</span>
          <span class="label">${a.sun_sign || ''}</span><br>
          <span class="detail">${a.sun_sign_element || ''} · ${a.sun_sign_quality || ''} · Ruled by ${a.sun_sign_ruler || ''}</span><br>
          <span class="detail">Season of ${a.season || ''} ${a.season_emoji || ''}</span>
        </div>
      </div>
      <div class="info-panel">
        <h3>⊛ Sabbat Countdowns</h3>
        ${countdownRows}
      </div>
      <div class="info-panel">
        <h3>☿ Planetary Positions</h3>
        ${planetRows}
      </div>
      <div class="info-panel">
        <h3>☉ Solar Cycle ${sc.cycle_number || 25}</h3>
        <div class="info-value">
          <span class="label">${sc.label || 'Unknown'}</span><br>
          <span class="detail">Activity: ${((sc.phase || 0) * 100).toFixed(0)}% · ~${sc.sunspot_estimate || 0} sunspots</span><br>
          <span class="detail">${((sc.progress || 0) * 100).toFixed(0)}% through cycle · ~${sc.years_remaining || '?'}y remaining</span>
        </div>
      </div>
      <div class="info-panel">
        <h3>❧ ${a.season || 'Season'} ${a.season_emoji || ''}</h3>
        <div class="info-value">
          <span class="detail">${a.season_description || ''}</span>
        </div>
      </div>
    `;
  }

  disconnectedCallback() {
    if (this._ro) this._ro.disconnect();
  }
}

customElements.define('wheel-of-the-year-card', WheelOfTheYearCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'wheel-of-the-year-card',
  name: 'Wheel of the Year',
  description: 'An interactive Wheel of the Year with months, days, Sabbats, zodiac, moon phases, planetary positions, and solar cycle.',
  preview: true,
  documentationURL: 'https://github.com/MorningstarOwl/ha-wheel-of-the-year',
});

console.info(
  '%c WHEEL OF THE YEAR %c v1.1.0 ',
  'color: #c9a84c; background: #0a0e14; font-weight: bold; padding: 2px 6px; border-radius: 4px 0 0 4px;',
  'color: #e8dcc8; background: #1a1410; padding: 2px 6px; border-radius: 0 4px 4px 0;'
);
