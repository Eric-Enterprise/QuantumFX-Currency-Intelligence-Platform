# QuantumFX 2.3.0 · Verification report

Verification date: September 23, 2026.

## Coverage

The automated suite covers decimal calculations and rounding, fee comparisons, input limits, unavailable currencies, API/cache validation, malformed files, network failures, storage failures, CSV formula neutralization, and Unicode exports.

GUI coverage includes comparison sorting, favorite deduplication, currency search, outdated chart responses, constant charts, the background queue, DEMO labeling, result invalidation, scrolling at 980 × 700, fullscreen controls, saved animation preferences, and collapsed active fees.

Snake coverage includes growth, scoring, wall/self collisions, occupied cells, reverse-direction prevention, multiple direction changes, a full board, high-score persistence, and automatic pause on navigation.

## Release checks

The multilingual build passed all 91 automated tests, including 26 real Tk interface tests. The Windows EXE was successfully built, but Windows Application Control blocked it from launching on this computer. Its packaged self-test therefore could not be completed. No security policy was changed. The same self-test passed through the Python source with `ok: true`, one saved conversion, and all four languages (`en`, `de`, `ko`, `sv`). This does not establish that the packaged EXE can run on every Windows configuration. The packaged self-test checks conversion, history, fee comparison, chart drawing, section switching, and Snake initialization using a temporary profile without network access.

The previous 2.2.0 release passed 75 tests and the EXE self-test. Its interface was visually inspected in windowed and fullscreen modes, including Snake. That visual check predates the English translation.

Historical live-data checks on September 22, 2026 returned 30 currencies with a rate date of September 21, 2026, and 64 EUR/USD chart points from June 24 through September 21. These are recorded observations, not a claim about current provider availability.

## Multilingual coverage

Catalog tests check identical message keys and format placeholders in English, German, Korean, and Swedish. GUI tests switch every language, preserve values and custom offers, retain chart data, pause Snake, keep icons, and verify navigation fits the minimum window size. Additional tests exercise pending requests, preference-save failures, and restoring a saved language in a new window.

System file dialogs and operating-system error text may follow the Windows display language. The translations have not had an independent native-speaker review.

## Environment and limits

- Windows 11 x64, build 26200.
- Python 3.12.14; Tcl/Tk 8.6.
- PyInstaller 6.22.3; pytest 9.1.1.
- Tests: set QUANTUMFX_GUI_TESTS=1, then run python -m pytest -q.
- Build: build.ps1, using the checked-in source and assets.
- No separate verification on a second Windows PC.
- The EXE is not digitally signed; no system security settings were changed.

GitHub Actions runs tests, the Windows build, and the packaged self-test. Its actual status is visible under Actions; local results do not establish a successful CI run. SHA256SUMS.txt accompanies the release downloads.
