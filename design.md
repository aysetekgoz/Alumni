# İÜ YBS Alumni — Design Reference
> Bosphorus obsidian & hairline precision with Imperial Gold punctuation. An institutional MIS design system where 1453 academic heritage meets kinetic, data-driven SaaS craft.

**Theme:** dark-executive (with light-editorial print & report contrast)

Source measurements are tailored for the **İstanbul Üniversitesi — Yönetim Bilişim Sistemleri (YBS / MIS)** Alumni Tracking System. Design tokens are structured in the `awesome-design-md` format so both developers and AI agents can generate consistent, animated, brand-faithful interfaces.

İÜ YBS Alumni operates in a disciplined, high-contrast executive register: deep Bosphorus obsidian (`#070b14`) and midnight slate (`#0f172a`) carry the canvas, structured by `1px` hairline borders rather than heavy drop shadows. **Imperial Gold (`#d4af37`)** and **İÜ Crimson (`#8b1e3f`)** serve as measured institutional punctuation — reserved for graduation milestones, prestige badges, and active focus — while **Sapphire (`#2563eb`)** and **Data Cyan (`#38bdf8`)** drive primary interactive actions and MIS telemetry. Geometry pairs generous container rounding (`24px` cards, `9999px` pill nav segments) with crisp `12px`–`14px` interactive controls. Motion is purposeful and GPU-composited: staggered viewport reveals, magnetic button lifts, and subtle gold-hairline shimmers bring the interface to life without ever sacrificing academic authority.

---

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Bosphorus Obsidian | `#070b14` | `--color-obsidian` | Deepest canvas background — anchors the viewport with near-black warmth and blue undertone |
| Midnight Navy | `#0f172a` | `--color-midnight` | Primary elevated container surface, sticky header base, and dark table backgrounds |
| Executive Slate | `#162033` | `--color-slate` | Interactive card hover surface, dropdown panels, and secondary Bento blocks |
| Hairline Steel | `#1e293b` | `--color-steel` | Structural `1px` borders, table dividers, and subtle input outlines |
| Mist Gray | `#94a3b8` | `--color-mist` | Muted metadata, timestamps, inactive navigation links, and helper copy |
| Silver Ink | `#cbd5e1` | `--color-silver` | Body copy, card descriptions, and secondary table values |
| Ivory Snow | `#f8fafc` | `--color-ivory` | Hero display headlines, card titles, primary KPI numbers, and high-contrast labels |
| Academic Sapphire | `#2563eb` | `--color-sapphire` | Primary CTA button fill, active focus rings, and primary interactive links |
| Sapphire Deep | `#1d4ed8` | `--color-sapphire-deep` | Primary CTA hover fill and pressed state |
| Data Cyan | `#38bdf8` | `--color-cyan` | Telemetry highlights, chart accents, inline action arrows, and hover text links |
| Imperial Gold | `#d4af37` | `--color-gold` | Institutional prestige accent — graduation year badges, top KPI highlights, and active hairline borders |
| Gold Soft | `rgba(212, 175, 55, 0.14)` | `--color-gold-soft` | Translucent gold wash for prestige pills and institutional callouts |
| İÜ Crimson | `#8b1e3f` | `--color-crimson` | İstanbul Üniversitesi heritage accent — faculty tags, institutional seal dot, and rare editorial punctuation |
| Emerald Signal | `#10b981` | `--color-emerald` | Active system status, open job postings, and `GET` endpoint badges |
| Amber Pulse | `#f59e0b` | `--color-amber` | Pending application review states and warning indicators |
| Rose Alert | `#f43f5e` | `--color-rose` | Validation errors and `404`/`500` Guardian alerts |

---

## Tokens — Typography

### Plus Jakarta Sans — Display headlines, section titles, navigation, and card headings. Bold geometric proportions at weight 700–800 with tight negative tracking (`-0.03em`) give headlines institutional authority. · `--font-display`
- **Substitute:** DM Sans, Inter
- **Weights:** 500, 600, 700, 800
- **Sizes:** 18px, 24px, 32px, 44px, 56px
- **Line height:** 1.08–1.25
- **Letter spacing:** `-0.030em` at 56px, `-0.025em` at 44px, `-0.020em` at 24–32px
- **OpenType features:** `"cv02"`, `"cv03"`, `"cv04"`
- **Role:** Carries all display moments, hero statements, and module headings with crisp geometric clarity.

### Inter — Body copy, form inputs, descriptions, and dense UI tables. Weight 400–500 at 14–16px ensures effortless long-form reading across job descriptions and alumni profiles. · `--font-sans`
- **Substitute:** System UI (`-apple-system`, `Segoe UI`, `Roboto`)
- **Weights:** 400, 500, 600
- **Sizes:** 12px, 13px, 14px, 15px, 16px
- **Line height:** 1.45–1.65
- **Letter spacing:** `-0.005em` at 14–15px, `0em` at 12–13px
- **OpenType features:** `"calt"`
- **Role:** Quiet, neutral workhorse for descriptions, tables, and form controls.

### JetBrains Mono — MIS telemetry, KPI counters, graduation years (`2024`), API routes (`/api/users`), and uppercase micro-stamps. Always paired with `font-variant-numeric: tabular-nums`. · `--font-mono`
- **Substitute:** IBM Plex Mono, `ui-monospace`
- **Weights:** 400, 500, 700
- **Sizes:** 11px, 12px, 13px, 32px (KPI counters)
- **Line height:** 1.2–1.5
- **Letter spacing:** `0.04em` on uppercase micro-stamps, `-0.02em` on large KPI numbers
- **Role:** Gives the platform its Management Information Systems (YBS) precision and tabular alignment.

### Type Scale

| Role | Family | Weight | Size | Line Height | Letter Spacing | Token |
|------|--------|--------|------|-------------|----------------|-------|
| micro-stamp | JetBrains Mono | 700 | 11px | 1.2 | +0.06em | `--text-micro` |
| caption | Inter | 500 | 13px | 1.5 | 0em | `--text-caption` |
| body | Inter | 400 | 15px | 1.6 | -0.005em | `--text-body` |
| body-lg | Inter | 400 | 17px | 1.6 | -0.008em | `--text-body-lg` |
| card-title | Plus Jakarta Sans | 700 | 18px | 1.35 | -0.015em | `--text-card-title` |
| section | Plus Jakarta Sans | 700 | 28px | 1.2 | -0.020em | `--text-section` |
| kpi | JetBrains Mono | 700 | 32px | 1.1 | -0.025em | `--text-kpi` |
| heading-lg | Plus Jakarta Sans | 800 | 44px | 1.12 | -0.025em | `--text-heading-lg` |
| display | Plus Jakarta Sans | 800 | 56px | 1.08 | -0.030em | `--text-display` |

---

## Tokens — Spacing & Shapes

**Base unit:** 4px  
**Density:** balanced-executive

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 8 | 8px | `--spacing-8` |
| 12 | 12px | `--spacing-12` |
| 16 | 16px | `--spacing-16` |
| 20 | 20px | `--spacing-20` |
| 24 | 24px | `--spacing-24` |
| 32 | 32px | `--spacing-32` |
| 48 | 48px | `--spacing-48` |
| 64 | 64px | `--spacing-64` |
| 80 | 80px | `--spacing-80` |

### Border Radius

| Element | Value | Token |
|---------|-------|-------|
| badges / tags | 9999px | `--radius-pill` |
| inputs / buttons | 12px | `--radius-control` |
| inner list items | 14px | `--radius-item` |
| standard cards | 20px | `--radius-card` |
| hero / bento feature cards | 24px | `--radius-bento` |

### Layout

- **Page max-width:** `1200px`
- **Section gap:** `64px`
- **Card padding:** `24px`–`28px`
- **Grid gap:** `20px`

---

## Motion & Micro-Interactions

Motion expresses **precision and institutional poise** — crisp exponential deceleration (`ease-out-expo`), never bouncy or sluggish. Only GPU-composited properties (`transform`, `opacity`, `border-color`) are animated.

### Timing & Easing Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | Page entrance, card reveal, modal transitions |
| `--ease-spring-snappy` | `cubic-bezier(0.22, 1, 0.36, 1)` | Button hover lifts, pill tab switches |
| `--duration-fast` | `180ms` | Link underlines, border color shifts, micro-hovers |
| `--duration-base` | `320ms` | Card elevation lifts, dropdown reveals |
| `--duration-enter` | `650ms` | Staggered hero and Bento grid entrance animations |

### Signature Animation Patterns

1. **Staggered Bento Entrance (`fadeSlideUp`):** Hero badge (`0ms`), headline (`80ms`), subtitle (`160ms`), CTAs (`240ms`), and Bento/KPI cards (`320ms + index * 70ms`) translate `16px → 0px` with `opacity: 0 → 1`.
2. **Imperial Gold Hairline Sweep:** Featured cards and institutional badges reveal a subtle `1px` gold border highlight (`rgba(212, 175, 55, 0.45)`) on hover with a gentle `-3px` vertical lift.
3. **Live Pulse Beacon:** A `8px` Emerald (`#10b981`) or Gold (`#d4af37`) dot with an expanding radial ring (`@keyframes beacon-pulse`, `2.4s infinite`) indicating live FastAPI / database connectivity.
4. **Ambient Aurora Drift:** Ultra-slow (`18s ease-in-out infinite alternate`) subtle radial glow drift behind the hero so the obsidian canvas feels alive without distracting from text.
5. **Reduced Motion Compliance:** Always wrap entrance and ambient keyframes in `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }`.

---

## Components

### 1. Primary Action Button (Academic Sapphire)
**Role:** Main CTA — *"İş İlanlarını İncele"*, *"Mezun Ekle"*, *"Başvur"*

Background `#2563eb`, text `#f8fafc`, `12px` radius, `12px 22px` padding, Plus Jakarta Sans `600` at `15px`. Inset top highlight `inset 0 1px 0 rgba(255,255,255,0.2)`. Hover: `#1d4ed8` fill, `translateY(-2px)`, soft glow `0 10px 24px -6px rgba(37, 99, 235, 0.55)`.

### 2. Prestige Gold Outline Button
**Role:** Institutional / featured CTA — *"Mezuniyet Yıllığı"*, *"YBS Kariyer Ağı"*

Background `rgba(212, 175, 55, 0.08)`, `1px solid rgba(212, 175, 55, 0.40)`, text `#f3e5ab`, `12px` radius, `12px 22px` padding. Hover: background `rgba(212, 175, 55, 0.16)`, border `#d4af37`, `translateY(-2px)`.

### 3. Sticky Glass Navigation Bar (`_navbar.html`)
**Role:** Top-level persistent navigation

Height `68px`, background `rgba(7, 11, 20, 0.78)` with `backdrop-filter: blur(16px)`, bottom border `1px solid rgba(212, 175, 55, 0.18)`. Left: İÜ YBS emblem (`38px` square, `10px` radius, gold hairline border) + wordmark. Center/Right: pill-shaped nav links (`9999px` radius) where the active route gets `rgba(37, 99, 235, 0.22)` fill and `#f8fafc` text.

### 4. MIS KPI Stat Card
**Role:** Telemetry metrics — Mezun Sayısı, Aktif İlanlar, Başvurular

Background `rgba(15, 23, 42, 0.72)`, `1px solid #1e293b`, `20px` radius, `22px` padding. Top row: `11px` uppercase JetBrains Mono label in `#94a3b8` + `36px` icon container. Main metric: `32px` JetBrains Mono `700` (`tabular-nums`) in `#f8fafc`. Hover: border shifts to `rgba(56, 189, 248, 0.4)`.

### 5. Bento Module Card
**Role:** Core feature gateways (Mezunlar, İş İlanları, Başvurular, Duyurular)

Background `rgba(15, 23, 42, 0.68)`, `1px solid #1e293b`, `24px` radius, `28px` padding. Contains category pill tag, `18px` Plus Jakarta Sans `700` title, `15px` Inter `#94a3b8` description, and bottom action bar with `→` arrow that translates `+4px` right on card hover.

### 6. Institutional Seal Badge
**Role:** Hero eyebrow & faculty credential tag

`9999px` pill, `6px 14px` padding, background `rgba(139, 30, 63, 0.22)`, border `1px solid rgba(212, 175, 55, 0.45)`, text `#f8fafc` with animated beacon dot. Signals İstanbul Üniversitesi YBS identity at first glance.

### 7. Form Input & Select
**Role:** CRUD modals and filter bars

Background `rgba(7, 11, 20, 0.8)`, `1px solid #1e293b`, `12px` radius, `11px 14px` padding, `15px` Inter `#f8fafc`. Focus: border `#2563eb`, ring `0 0 0 3px rgba(37, 99, 235, 0.2)`.

---

## Do's and Don'ts

### Do
- Use `1px` hairline borders (`#1e293b` or `rgba(212, 175, 55, 0.35)`) as the primary structural separator instead of heavy drop shadows.
- Reserve **Imperial Gold (`#d4af37`)** and **İÜ Crimson (`#8b1e3f`)** for institutional seals, graduation years, and featured borders — scarcity preserves prestige.
- Always apply `font-variant-numeric: tabular-nums` and JetBrains Mono to KPI counts, dates, and API paths.
- Keep all interactive transitions between `180ms` and `320ms` using `--ease-out-expo` and GPU-composited properties only.
- Respect `prefers-reduced-motion` across every keyframe and transition.

### Don't
- Don't flood the UI with rainbow gradients or neon glows — keep the palette anchored in Bosphorus Obsidian (`#070b14`) and Midnight Navy (`#0f172a`).
- Don't mix sharp `0px` corners with `24px` Bento cards; adhere to the `12px` (controls) / `20px–24px` (cards) / `9999px` (pills) radius hierarchy.
- Don't animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`) — always animate `transform` and `opacity`.
- Don't use pure `#000000` or pure `#ffffff` flat fills; `#070b14` and `#f8fafc` maintain subtle tonal cohesion.

---

## Surfaces & Elevation

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Bosphorus Obsidian | `#070b14` | Root viewport canvas |
| 1 | Midnight Glass | `rgba(15, 23, 42, 0.72)` + `blur(16px)` | Primary Bento cards and KPI tiles |
| 2 | Executive Slate | `rgba(22, 32, 51, 0.88)` | Hovered cards, popovers, active row highlights |
| 3 | Sticky Header | `rgba(7, 11, 20, 0.78)` + `blur(16px)` | Persistent top navigation with gold hairline bottom border |

- **Card Elevation:** `0 1px 0 0 rgba(255, 255, 255, 0.04) inset, 0 12px 32px -12px rgba(0, 0, 0, 0.5)`
- **Hover Elevation:** `0 20px 40px -15px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(212, 175, 55, 0.3)`

---

## Imagery & Layout

- **Visual Motif:** Subtle `48px × 48px` architectural coordinate grid (`rgba(255, 255, 255, 0.025)`) paired with soft radial ambient glows (Sapphire top-left, Gold/Cyan bottom-right). No cluttered stock photos; data cards and clean vector icons (`1.5px` stroke) carry the visual weight.
- **Page Structure:** Centered `1200px` container with `64px` vertical section rhythm:
  1. Sticky institutional navbar
  2. Centered/split Hero with animated entrance & institutional seal badge
  3. 4-column MIS KPI strip (`tabular-nums`)
  4. 2×2 Bento module grid
  5. Live 2-column feed (Son Duyurular & Güncel İş İlanları)
  6. Compact developer/API status bar (`/api/swagger`, `/api/health`)

---

## Agent Prompt Guide

**Quick Color Reference**
- Canvas: `#070b14` | Card: `rgba(15, 23, 42, 0.72)` | Border: `#1e293b`
- Text Primary: `#f8fafc` | Text Secondary: `#cbd5e1` | Muted: `#94a3b8`
- Primary Action: `#2563eb` (Sapphire) | Telemetry Accent: `#38bdf8` (Cyan)
- Institutional Accent: `#d4af37` (Imperial Gold) & `#8b1e3f` (İÜ Crimson)

**Example Component Prompt**
> Build an İÜ YBS Alumni KPI card on `#070b14` canvas: `rgba(15, 23, 42, 0.72)` glass surface with `backdrop-filter: blur(16px)`, `1px solid #1e293b` hairline border, `20px` border-radius, `22px` padding. Top row has `11px` uppercase JetBrains Mono label in `#94a3b8` and a `36px` rounded-10px icon badge tinted with `rgba(212, 175, 55, 0.14)`. Metric value in `32px` JetBrains Mono `700` (`tabular-nums`) `#f8fafc`. On hover, animate `transform: translateY(-3px)` and border-color to `rgba(212, 175, 55, 0.45)` over `320ms cubic-bezier(0.16, 1, 0.3, 1)`.

---

## Geometry Philosophy & Similar Brands

Three radii govern the entire UI: **`9999px`** for status pills and nav segments, **`12px`** for buttons and inputs, and **`20px–24px`** for cards and Bento containers. This deliberate contrast keeps interactive controls crisp and utilitarian while giving content containers executive breathing room.

* **Linear** — Hairline border discipline, deep dark surfaces, and fast exponential micro-interactions.
* **Vercel** — High-contrast monochrome/slate canvas with functional color punctuation and tabular telemetry.
* **Stripe** — Editorial hierarchy, subtle ambient depth, and tactile inset button highlights.

---

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-obsidian: #070b14;
  --color-midnight: #0f172a;
  --color-slate: #162033;
  --color-steel: #1e293b;
  --color-mist: #94a3b8;
  --color-silver: #cbd5e1;
  --color-ivory: #f8fafc;
  --color-sapphire: #2563eb;
  --color-sapphire-deep: #1d4ed8;
  --color-cyan: #38bdf8;
  --color-gold: #d4af37;
  --color-gold-soft: rgba(212, 175, 55, 0.14);
  --color-crimson: #8b1e3f;
  --color-emerald: #10b981;
  --color-amber: #f59e0b;
  --color-rose: #f43f5e;

  /* Typography */
  --font-display: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-sans: 'Inter', 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;

  /* Spacing & Layout */
  --page-max-width: 1200px;
  --section-gap: 64px;
  --card-padding: 24px;
  --radius-control: 12px;
  --radius-item: 14px;
  --radius-card: 20px;
  --radius-bento: 24px;
  --radius-pill: 9999px;

  /* Surfaces & Elevation */
  --surface-card: rgba(15, 23, 42, 0.72);
  --surface-elevated: rgba(22, 32, 51, 0.88);
  --shadow-card: 0 1px 0 0 rgba(255, 255, 255, 0.04) inset, 0 12px 32px -12px rgba(0, 0, 0, 0.5);

  /* Motion */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spring-snappy: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-fast: 180ms;
  --duration-base: 320ms;
  --duration-enter: 650ms;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes beaconPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.55); }
  70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
