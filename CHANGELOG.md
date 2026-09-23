# Changelog

## 2.3.0 — Multilingual desktop

- Switch instantly between English, German, Korean, and Swedish from the sidebar.
- Save the selected language and restore it on the next launch.
- Translate navigation, help, tooltips, errors, fee comparisons, and Snake controls.
- Retain current inputs, offers, chart data, and saved history during switching.
- Pause Snake safely while preserving its board and score.
- Format displayed amounts for the selected language and use a Korean-capable font.
- Keep stored data and CSV formats compatible across languages.
- Add catalog validation and GUI regression tests for language changes.

## 2.2.1 — English edition

- Translate the current interface, help, tooltips, errors, and Snake controls into English.
- Use English number formatting for displayed amounts; still accept decimal dots or commas as input.
- Translate the README, banner, security notes, verification report, and release documentation.
- Use English names for packaged documentation and source archives.
- Preserve existing local preferences, saved conversions, and original project attribution.

## 2.2.0

- Layered glass-style gradients, light edges, and rounded surfaces.
- Scalable line icons, labeled buttons, keyboard focus, and tooltips.
- Simpler navigation and clearly labeled source and target currency fields.
- Collapsible fee fields with an indicator when fees remain active.
- Responsive results, clear input errors, and copying only for valid current results.
- Currency search with Ctrl+F, reset action, and more readable tables.
- Better export controls in smaller windows.
- Remove the design slogan and personal development credit from the interface.

## 2.1.0

- Fullscreen desktop layout with sidebar, hero area, and responsive converter.
- F11 and Escape controls, plus visible window and close buttons.
- Animated hover states, section transitions, result feedback, and chart drawing.
- Saved preference for disabling animations.
- Snake with smooth movement, three speeds, pause, local high score, and automatic pause when switching sections.
- Development and original-project credits in the interface at that time.
- Historical chart CSV export and additional game and interface tests.

## 2.0.0

- Split the original calculator into data/calculation logic and desktop interface modules.
- Add Windows packaging with embedded Python/Tk and a reproducible build.
- Introduce a five-section desktop interface and application icon.
- Replace eight fixed currencies with validated API currency availability.
- Show daily reference rates and actual rate dates rather than claiming real-time prices.
- Mark undated fallback values as DEMO in the interface, history, and exports.
- Move network requests off the GUI thread and discard outdated chart responses.
- Replace floating-point calculations with Decimal and explicit input validation.
- Add percentage/fixed fees and comparison of three user-defined offers.
- Add 30/90/365-day charts with hover values and historical caching.
- Add favorites, search, rate tables, history, and CSV exports.
- Store local data in the user profile with atomic JSON writes and rotating logs.
- Add a test suite and packaged application self-test.
- Archive original code, tests, and README under legacy/; preserve the original license.
- This initial replacement interface was German; version 2.2.1 switches it to English.
