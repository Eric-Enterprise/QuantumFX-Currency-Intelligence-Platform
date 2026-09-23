<div align="center">

![QuantumFX — Currencies. Clearly.](assets/readme-banner.svg)

**Your currency companion for the Windows desktop.**

Compare rates, understand fees, and keep your conversions in view.

[![Version](https://img.shields.io/badge/Version-2.3.0-a998ff?style=flat-square)](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/tag/v2.3.0)
![Windows](https://img.shields.io/badge/Windows-10%20%2F%2011%20%C2%B7%20x64-72e7cf?style=flat-square)
![Languages](https://img.shields.io/badge/Languages-EN%20%C2%B7%20DE%20%C2%B7%20KO%20%C2%B7%20SV-c8c3ef?style=flat-square)
[![Build](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/actions/workflows/python-app.yml/badge.svg)](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/actions/workflows/python-app.yml)

### [↓ Download QuantumFX.exe](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/download/v2.3.0/QuantumFX.exe)

**No installation. No account. Python included.**

[All downloads](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/latest) · [Features](#-what-quantumfx-can-do) · [Quick start](#-ready-in-a-minute) · [Development](#-for-developers)

</div>

---

## ✨ What QuantumFX can do

A calm, dark interface with purple and mint accents, rounded glass-style surfaces, and clearly labeled icons. Optional animations provide feedback, fullscreen gives you room to focus, and smaller windows automatically adapt the layout.

| | Feature | What you get |
| :---: | :--- | :--- |
| 💱 | **Currency converter** | Convert available currency pairs using decimal arithmetic and swap currencies instantly. |
| 📈 | **Rate charts** | Explore historical daily rates over 30, 90, or 365 days; hover to inspect values. |
| ⚖️ | **Fee comparison** | Compare three offers with your own percentage and fixed fees. |
| ⭐ | **Favorites & search** | Save frequently used pairs and find currencies quickly. |
| 🗂️ | **History & export** | Keep up to 1,000 conversions locally; export history, rates, and chart data as CSV. |
| 📴 | **Saved rates** | Use the last retrieved rate snapshot when a connection is unavailable. |
| 🐍 | **Snake Arcade** | Take a break with three speeds, smooth movement, and a locally saved high score. |

## 🚀 Ready in a minute

1. **[Download QuantumFX.exe](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/download/v2.3.0/QuantumFX.exe)** and double-click to launch.
2. **Enter an amount and choose currencies**, such as `100` from EUR to USD.
3. Optionally expand **Add fees** and enter your deductions.
4. Select **Convert & save**. Your result appears immediately and is saved in local history.

Select **Load history** to display a rate chart. Reload after changing the currency pair or period.

> **Windows 10/11 · 64-bit:** No installer or separate Python installation is required. Unpacking the embedded runtime may take a few seconds on first launch. The EXE is not digitally signed. Tested on Windows 11 x64; other PCs have not been separately verified.

### Downloads

| File | Contents |
| :--- | :--- |
| [**QuantumFX.exe**](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/download/v2.3.0/QuantumFX.exe) | Ready-to-run Windows application. |
| [**Windows package (.zip)**](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/download/v2.3.0/QuantumFX-2.3.0-Windows-x64.zip) | EXE, guide, verification report, and license notices. |
| [**SHA256 checksums**](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/download/v2.3.0/SHA256SUMS.txt) | Checksums for verifying downloaded files. |

## 🌍 Choose your language

Use **Language** at the bottom of the sidebar to switch the interface immediately:

| Language | Selector label |
| :--- | :--- |
| English | English |
| German | Deutsch |
| Korean (South Korea) | 한국어 |
| Swedish | Svenska |

Your choice is saved for the next launch. Switching keeps your amount, currencies, fees, custom offers, history, and chart data. Snake pauses safely and retains its current board. Menus, help, tooltips, validation messages, and game controls are translated. Korean uses a Windows font with Hangul support.

Displayed amounts follow the selected language: `1,234.56` in English/Korean, `1.234,56` in German, and `1 234,56` in Swedish. Dot and comma decimal input remain accepted without thousands separators. CSV columns and stored values stay stable across languages. Windows file dialogs and operating-system errors may use the system language.

## ⌨️ Less clicking, faster results

| Shortcut | Action |
| :--- | :--- |
| `Enter` | Convert in the calculator |
| `Ctrl` + `F` | Open currency search |
| `Ctrl` + `R` | Refresh rates |
| `Ctrl` + `S` | Swap source and target currencies |
| `F11` | Toggle fullscreen |
| `Esc` | Leave fullscreen and pause Snake |

**Snake:** Click the board, steer with arrow keys or `WASD`, pause with Space, and start a new game with `Enter`. Switching sections pauses the game automatically.

<details>
<summary><strong>Amounts, fees, and rounding</strong></summary>

Enter amounts without thousands separators: `1234.56` or `1234,56`. Negative values, scientific notation, more than eight decimal places, and amounts above one trillion are rejected.

Fixed fees use the source currency. The calculation is:

```text
(amount − amount × percentage / 100 − fixed fee) × target rate / base rate
```

Only displayed amounts are rounded (`ROUND_HALF_UP`) and use the selected language’s formatting. CSV exports retain unrounded decimal values, use UTF-8 with a BOM, and separate columns with semicolons. Fee comparison uses the same reference rate for every offer; individual exchange-rate markups are not included.

Entered fees remain active when their fields are collapsed, with a visible indicator.

</details>

## 🌐 Understanding your rates

QuantumFX uses **daily reference rates from Frankfurter v1 / the ECB**. The verified online request returned 30 currencies; availability depends on the provider. These are reference values, not real-time prices or guaranteed bank offers. Rate dates may be older on weekends and holidays.

| Status | Meaning |
| :--- | :--- |
| **Online** | Validated rates with their actual rate date. |
| **Offline / saved rates** | The last locally saved snapshot, which may be older. |
| **DEMO** | Undated samples for trying the app, also marked as DEMO in history and CSV exports. |

Charts contain only retrieved or saved historical data. Missing values are never invented.

## 🔒 Your data, kept local

**No account, no telemetry, no broker connection.** Conversion amounts and history are not sent to the rate provider. Requests contain currencies, date ranges, and standard connection information.

Application data is stored under `%LOCALAPPDATA%\QuantumFX`. The EXE needs no installation; preferences and history are saved separately in this user folder. Existing profiles remain compatible with the multilingual release.

<details>
<summary><strong>Stored files and launch options</strong></summary>

| File | Contents |
| :--- | :--- |
| `settings.json` | Preferences, favorites, and Snake high score |
| `rates.json` | Last rate snapshot with rate and retrieval dates |
| `chart-*.json` | Saved historical series |
| `history.json` | Up to 1,000 conversions |
| `QuantumFX.log` | Error log; up to three files of approximately 1 MB each |

```powershell
# Start in a regular window
.\QuantumFX.exe --windowed

# Skip the automatic rate request at startup
.\QuantumFX.exe --offline
```

Manual requests remain available with `--offline`. Set `QUANTUMFX_DATA_DIR` to use a separate data folder for profiles or tests. **Clear history** removes saved conversions. Automatic application updates are not included.

</details>

## 🛠️ For developers

Translations are stored in `quantumfx/i18n.py`. Each language uses the same message keys and formatting placeholders. Tests check catalog completeness, placeholder compatibility, live switching, saved preferences, icons, and localized amounts. Add a complete catalog and a native-language label in `LANGUAGES` to introduce another language.


**Python 3.10+ with Tk.** The application needs no external Python runtime packages. Test and build dependencies are listed in `requirements-dev.txt`.

```powershell
git clone https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform.git
cd QuantumFX-Currency-Intelligence-Platform
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe main.py
```

<details>
<summary><strong>Run tests and build the Windows EXE</strong></summary>

```powershell
# Logic tests
.venv/Scripts/python.exe -m pytest

# Include the real Tk interface tests
$env:QUANTUMFX_GUI_TESTS = '1'
.venv/Scripts/python.exe -m pytest

# Build a standalone Windows executable
./build.ps1 -Python .venv/Scripts/python.exe
```

The result is `dist/QuantumFX.exe`. An icon is included; regenerating it with `tools/create_icon.py` requires Pillow.

Run the packaged self-test with a temporary profile:

```powershell
./dist/QuantumFX.exe --smoke-test C:/Path/smoke-result.json
```

After the process exits, the JSON file contains `ok: true` or an error. GitHub Actions runs the tests and Windows build, and makes successful builds available as downloadable artifacts.

</details>

### Project structure

```text
quantumfx/
├── app.py       Interface and user workflows
├── core.py      Rates, calculations, and local storage
├── ui.py        Styling, icons, and animations
├── snake.py     Game rules and arcade interface
└── i18n.py      Translation catalogs and locale-specific presentation
main.py          Application entry point
assets/          Graphics and application icon
tests/           Tests for the current application
tools/           Release packaging and icon utilities
legacy/          Original project archive
```

See the [verification report](VERIFICATION.md) for test results and limitations, and the [changelog](CHANGELOG.md) for release history.

## 📚 Origin & license

QuantumFX is based on the [original project by oneiric-hammer](https://github.com/oneiric-hammer/QuantumFX-Currency-Intelligence-Platform), starting from commit `1a431f630f32f57b2b93e8c1d1df5aab4b9cae38`. The [original license](LICENSE) is preserved. Bundled runtime license notices are in [licenses/](licenses/).

The original multilingual interface and README remain archived under [legacy/](legacy/). This historical archive retains its original language resources. The current application supports English, German, Korean, and Swedish. Repository documentation remains in English; the original application is not included in the new EXE.

---

<div align="center">

**QuantumFX · Currencies. Clearly.**

[Download](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/releases/latest) · [Changelog](CHANGELOG.md) · [Report an issue](https://github.com/Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform/issues)

</div>
