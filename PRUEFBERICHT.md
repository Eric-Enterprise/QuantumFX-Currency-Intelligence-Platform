# QuantumFX 2.0 · Prüfbericht

Prüfdatum: 22. September 2026.

## Erfolgreich geprüft

- 61 automatisierte Tests bestanden: 49 Tests der Berechnungs-, Speicher- und
  Kurslogik sowie 12 Tests mit echter Tk-Oberfläche.
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
- Echter HTTPS-Abruf: 30 Währungen, Kursdatum 21. September 2026.
- Echter EUR/USD-Zeitreihenabruf: 64 Datenpunkte, 24. Juni bis 21. September 2026.
- Start und integrierter Selbsttest der Python-Anwendung erfolgreich.
- Windows-x64-EXE mit PyInstaller erfolgreich erstellt, inklusive Python, Tk,
  Icon und Lizenzdateien. Build-Warnungen betreffen plattformspezifische oder
  optionale Module, die die Anwendung nicht verwendet.

## Grenze der abschließenden Prüfung

Der Start der fertig verpackten EXE wurde auf diesem Rechner von Windows mit
„Eine Anwendungssteuerungsrichtlinie hat diese Datei blockiert“ verhindert.
Der EXE-Selbsttest konnte deshalb nicht laufen. Die EXE ist nicht digital signiert.
Die Sicherheitsrichtlinie wurde nicht verändert oder umgangen.

Die Computer-Use-Sichtprüfung wurde vom Benutzer per Escape beendet. Danach
wurden keine weiteren Bildschirmaktionen ausgeführt. Es erfolgte keine Prüfung
der fertigen EXE auf einem zweiten Windows-PC. Der Build ist daher geliefert,
sein tatsächlicher Start als EXE bleibt auf einem dafür freigegebenen System zu prüfen.

## Umgebung und Reproduzierbarkeit

- Windows 11 x64, Build 26200.
- Python 3.12.14; Tcl/Tk 8.6.
- PyInstaller 6.22.3; pytest 9.1.1.
- Original-Commit: 1a431f630f32f57b2b93e8c1d1df5aab4b9cae38.
- Tests: QUANTUMFX_GUI_TESTS=1, python -m pytest -q.
- Build: build.ps1; Quellcode und notwendige Assets sind beigefügt.
- Der beigefügte GitHub-Actions-Workflow wurde lokal vorbereitet, aber nicht auf
  GitHub ausgeführt. Kein Push, kein öffentliches Release.

Die SHA-256-Prüfsummen stehen in SHA256SUMS.txt neben den gelieferten Dateien.
