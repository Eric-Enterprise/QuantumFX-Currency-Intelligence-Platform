"""Collect distributable files without caches, Git history or development environments."""
import argparse
import hashlib
import re
import shutil
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("output", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
version = re.search(r'__version__ = "([\d.]+)"', (root / "quantumfx/__init__.py").read_text(encoding="utf-8")).group(1)
source_name = f"QuantumFX-{version}-Source.zip"
windows_name = f"QuantumFX-{version}-Windows-x64.zip"
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
shutil.copy2(root / "dist/QuantumFX.exe", out / "QuantumFX.exe")
for name in ("README.md", "VERIFICATION.md", "CHANGELOG.md", "SECURITY.md"):
    shutil.copy2(root / name, out / name)
shutil.copy2(root / "LICENSE", out / "LICENSE")
excluded = {".git", ".venv", "__pycache__", ".pytest_cache", "build", "dist"}
sources = [p for p in root.rglob("*") if p.is_file()
           and not excluded.intersection(p.relative_to(root).parts) and p.suffix != ".spec"]
with zipfile.ZipFile(out / source_name, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(sources):
        archive.write(path, Path("QuantumFX") / path.relative_to(root))
with zipfile.ZipFile(out / windows_name, "w", zipfile.ZIP_DEFLATED) as archive:
    for name in ("QuantumFX.exe", "README.md", "VERIFICATION.md", "CHANGELOG.md", "SECURITY.md", "LICENSE"):
        archive.write(out / name, name)
    archive.write(root / "assets/readme-banner.svg", "assets/readme-banner.svg")
    for path in (root / "licenses").iterdir():
        archive.write(path, Path("licenses") / path.name)
lines = []
for name in ("QuantumFX.exe", source_name, windows_name):
    path = out / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {name}")
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
    print(f"{name}: {path.stat().st_size:,} bytes, SHA256 {digest}")
(out / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="ascii")
