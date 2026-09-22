param([string]$Python = "python")
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
& $Python -m pytest
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
& $Python -m PyInstaller --noconfirm --clean --onefile --windowed --name QuantumFX --icon assets/quantumfx.ico --add-data 'LICENSE;.' --add-data 'licenses;licenses' --add-data 'assets/quantumfx.ico;assets' main.py
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
Write-Output 'Ready: dist/QuantumFX.exe'
