"""Collect distributable files without caches, Git history or development environments."""
import argparse
import hashlib
import shutil
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("output", type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
shutil.copy2(root / "dist/QuantumFX.exe", out / "QuantumFX.exe")
shutil.copy2(root / "README.md", out / "Anleitung.md")
shutil.copy2(root / "PRUEFBERICHT.md", out / "Pruefbericht.md")
shutil.copy2(root / "LICENSE", out / "LICENSE")
excluded = {".git", ".venv", "__pycache__", ".pytest_cache", "build", "dist"}
sources = [p for p in root.rglob("*") if p.is_file()
           and not excluded.intersection(p.relative_to(root).parts) and p.suffix != ".spec"]
with zipfile.ZipFile(out / "QuantumFX-2.2-Quellcode.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(sources):
        archive.write(path, Path("QuantumFX") / path.relative_to(root))
with zipfile.ZipFile(out / "QuantumFX-2.2-Windows-x64.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for name in ("QuantumFX.exe", "Anleitung.md", "Pruefbericht.md", "LICENSE"):
        archive.write(out / name, name)
    for path in (root / "licenses").iterdir():
        archive.write(path, Path("licenses") / path.name)
lines = []
for name in ("QuantumFX.exe", "QuantumFX-2.2-Quellcode.zip", "QuantumFX-2.2-Windows-x64.zip"):
    path = out / name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {name}")
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
    print(f"{name}: {path.stat().st_size:,} bytes, SHA256 {digest}")
(out / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="ascii")
