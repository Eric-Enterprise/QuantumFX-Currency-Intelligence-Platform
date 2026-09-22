# QuantumFX 2.1 · Prüfbericht

Prüfdatum: 22. September 2026.

## Erfolgreich geprüft

- 71 automatisierte Tests bestanden: 55 Tests der Berechnungs-, Speicher-,
  Kurs- und Spiellogik sowie 16 Tests mit echter Tk-Oberfläche.
- Dezimalrechnung mit Kreuzkursen und Gebühren; Grenzwerte, leere und ungültige
  Eingaben, Rundung, fehlende Währungen und Gebühren über dem Ausgangsbetrag.
- Validierung von API und Cache; beschädigte Dateien, zukünftige Datumswerte,
  Netzwerkausfälle und Schreibfehler. Online-Daten bleiben bei Cache-Schreibfehlern
  verwendbar. Historische Daten werden bei Ausfall nicht erfunden.
- Verlauf speichern/laden/löschen, unveränderte Daten bei Schreibfehlern,
  CSV-Export mit Formelentschärfung und Unicode.
- GUI: Gebührenvergleich und Sortierung, Favoritenduplikate, Suche und Paarwahl,
  veraltete Diagrammantworten, konstante Diagramme, Hintergrund-Queue, DEMO-Hinweis,
  Ergebnisinvalidierung und Scrollbarkeit bei 980 × 700.
- Vollbild und Escape, automatische Snake-Pause beim Bereichswechsel,
  Highscore-Speicherung, abschaltbare Animationen und Eric-Hinweis.
- Snake: Wachstum, Punkte, Wand-/Selbstkollisionen, belegte Felder,
  Umkehrverbot, doppelte Richtungswechsel und vollständig belegtes Spielfeld.
- Echter HTTPS-Abruf: 30 Währungen, Kursdatum 21. September 2026.
- Echter EUR/USD-Zeitreihenabruf: 64 Datenpunkte, 24. Juni bis 21. September 2026.
- Start und integrierter Selbsttest der Python-Anwendung erfolgreich.
- Windows-x64-EXE mit PyInstaller erfolgreich erstellt, inklusive Python, Tk,
  Icon und Lizenzdateien. Build-Warnungen betreffen plattformspezifische oder
  optionale Module, die die Anwendung nicht verwendet.

## Prüfung der fertigen EXE

Der neue 2.1-Build wurde erfolgreich als verpackte EXE gestartet. Der integrierte
Selbsttest meldete ok: true; der Prozess endete mit Exit-Code 0. Geprüft wurden
unter anderem Umrechnung, Verlauf, Gebührenvergleich und Initialisierung von Snake.
Die frühere Windows-Startblockade trat bei diesem Build nicht auf. Die EXE ist
nicht digital signiert. Es wurden keine Sicherheitsrichtlinien geändert.

Die aktuelle Oberfläche wurde im Fenster und im Vollbild visuell geprüft,
einschließlich des Snake-Bereichs. Es erfolgte keine Prüfung der fertigen EXE auf
einem zweiten Windows-PC. Die erfolgreichen lokalen Tests garantieren keine
Kompatibilität mit jeder Windows-Konfiguration.

## Umgebung und Reproduzierbarkeit

- Windows 11 x64, Build 26200.
- Python 3.12.14; Tcl/Tk 8.6.
- PyInstaller 6.22.3; pytest 9.1.1.
- Original-Commit: 1a431f630f32f57b2b93e8c1d1df5aab4b9cae38.
- Tests: QUANTUMFX_GUI_TESTS=1, python -m pytest -q.
- Build: build.ps1; Quellcode und notwendige Assets sind beigefügt.
- Der GitHub-Actions-Workflow führt Tests, Windows-Build und Paket-Selbsttest aus.
  Sein tatsächlicher Status ist unter Actions im Eric-Enterprise-Fork einsehbar.
  Die oben genannten Testzahlen stammen vom lokalen Testlauf.

Die SHA-256-Prüfsummen stehen in SHA256SUMS.txt neben den gelieferten Dateien.
