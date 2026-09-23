# QuantumFX 2.2.1 · Verification report

Verification date: September 23, 2026.

## Coverage

The automated suite covers decimal calculations and rounding, fee comparisons, input limits, unavailable currencies, API/cache validation, malformed files, network failures, storage failures, CSV formula neutralization, and Unicode exports.

GUI coverage includes comparison sorting, favorite deduplication, currency search, outdated chart responses, constant charts, the background queue, DEMO labeling, result invalidation, scrolling at 980 × 700, fullscreen controls, saved animation preferences, and collapsed active fees.

Snake coverage includes growth, scoring, wall/self collisions, occupied cells, reverse-direction prevention, multiple direction changes, a full board, high-score persistence, and automatic pause on navigation.

## Release checks

The English build passed all 75 automated tests, including 20 real Tk interface tests. The rebuilt Windows EXE completed its self-test with `ok: true` and exit code 0, displaying the result as `1,042.13 EUR`. The packaged self-test checks conversion, history, fee comparison, chart drawing, section switching, and Snake initialization using a temporary profile without network access.

The previous 2.2.0 release passed 75 tests and the EXE self-test. Its interface was visually inspected in windowed and fullscreen modes, including Snake. That visual check predates the English translation.

Historical live-data checks on September 22, 2026 returned 30 currencies with a rate date of September 21, 2026, and 64 EUR/USD chart points from June 24 through September 21. These are recorded observations, not a claim about current provider availability.

## Environment and limits

- Windows 11 x64, build 26200.
- Python 3.12.14; Tcl/Tk 8.6.
- PyInstaller 6.22.3; pytest 9.1.1.
- Tests: set QUANTUMFX_GUI_TESTS=1, then run python -m pytest -q.
- Build: build.ps1, using the checked-in source and assets.
- No separate verification on a second Windows PC.
- The EXE is not digitally signed; no system security settings were changed.

GitHub Actions runs tests, the Windows build, and the packaged self-test. Its actual status is visible under Actions; local results do not establish a successful CI run. SHA256SUMS.txt accompanies the release downloads.
