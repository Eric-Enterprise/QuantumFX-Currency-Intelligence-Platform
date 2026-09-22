# QuantumFX 2.2 · Windows Desktop

Deutschsprachiger Währungsrechner mit Tagesreferenzkursen, Kursdiagrammen,
Gebührenvergleich und lokalem Verlauf. Weiterentwicklung von
https://github.com/oneiric-hammer/QuantumFX-Currency-Intelligence-Platform

## Neu in 2.2 · Liquid Glass

Geschichtete Glasoptik mit Farbverläufen, Lichtkanten und animierten Schaltflächen.
Die Glasflächen werden in der Anwendung gezeichnet und bleiben gut lesbar.
Alle wichtigen Aktionen haben skalierbare Linien-Icons und Textbeschriftungen.
Kurze Navigationsnamen, Hilfetexte bei Mauszeiger oder Tastaturfokus und deutliche
Von-/Nach-Felder machen den Ablauf verständlicher. Optionale Gebühren können
aufgeklappt werden; eingetragene Werte bleiben beim Einklappen erhalten und werden
als aktiv gekennzeichnet. Ungültige Beträge werden am Feld markiert. Kopieren ist
erst mit einem gültigen aktuellen Ergebnis möglich. Strg+F öffnet die Währungssuche.
Tabellen haben abwechselnde Zeilenfarben und horizontale Scrollleisten.

## Funktionen seit 2.1 · Weiterentwickelt von Eric

Die neue Oberfläche startet im Vollbild mit Seitenleiste, violetten und mintfarbenen
Akzenten, animierten Schaltflächen, Diagrammaufbau und Ergebnisrückmeldung.
F11 wechselt den Vollbildmodus; Escape verlässt ihn. Mit --windowed startet die
Anwendung direkt im normalen Fenster. Auf schmalen Fenstern stehen Rechner und
Diagramm untereinander. Animationen lassen sich links abschalten; die Einstellung
wird gespeichert. Diagrammdaten können zusätzlich als CSV exportiert werden.

Snake Arcade ist direkt über die Seitenleiste erreichbar. Neues Spiel startet
eine Runde, Pfeiltasten oder WASD steuern die Schlange, Leertaste pausiert und
Enter beginnt neu. Zuerst das Spielfeld anklicken, falls die Tastatur einen anderen
Bereich fokussiert. Drei Geschwindigkeiten stehen bereit. Der Highscore wird lokal
gespeichert. Beim Bereichswechsel und bei Escape pausiert die Runde automatisch.
Der Hinweis „Weiterentwickelt von Eric“ steht dauerhaft in der Seitenleiste und
zusätzlich im Hilfebereich; die Herkunft des Originalprojekts bleibt genannt.

## Direkt starten

<<<<<<< HEAD
**Redefining the future of monetary value translation, one transaction at a time.**

=======
QuantumFX.exe per Doppelklick starten. Windows 10/11, 64 Bit (x64).
Die portable EXE enthält Python und Tk. Kein Installer, keine separate
Python-Installation und keine Administratorrechte für den normalen Betrieb nötig.
Beim ersten Start kann das Entpacken der enthaltenen Laufzeit einige Sekunden dauern.
Die Datei ist nicht digital signiert. Andere PCs wurden nicht separat geprüft.
>>>>>>> c9cff6a (feat: ship QuantumFX desktop platform)

## Funktionen

- 30 Währungen beim überprüften Online-Abruf; Umfang abhängig vom Kursanbieter.
- Dezimalgenaue Umrechnung beliebiger verfügbarer Währungspaare.
- Prozentuale und fixe Gebühren in der Ausgangswährung.
- Vergleich von drei selbst eingetragenen Gebührenangeboten.
- Historische Tageskurse über 30, 90 oder 365 Tage; Werte per Maus ablesen.
- Favoriten, Währungstausch und durchsuchbare Kursübersicht.
- Bis zu 1.000 gespeicherte Umrechnungen inklusive Kursdatum und Quelle.
- CSV-Export von Kursübersicht und Verlauf (UTF-8-BOM, Semikolon).
- Hintergrundabrufe, Offline-Cache, atomare Schreibvorgänge und Fehlerprotokoll.
- Größenveränderliches Fenster mit scrollbar erreichbarem Rechnerinhalt.

Die neue Oberfläche ist auf Deutsch. Die ursprüngliche Oberfläche mit vier
Sprachen ist unverändert unter legacy/QuantumFX-original.py archiviert.
Sie ist nicht Bestandteil der neuen EXE.

## Bedienung

1. Betrag ohne Tausendertrennzeichen eingeben: 1234,56 oder 1234.56.
2. Ausgangs- und Zielwährung wählen.
3. Optional Gebühren eintragen. Berechnung:
   (Betrag - Betrag * Prozent / 100 - Fixgebühr) * Zielkurs / Basiskurs.
4. Umrechnen & speichern drücken. Das Ergebnis wird lokal protokolliert.
5. Für Diagramme Verlauf laden wählen. Nach Paar- oder Zeitraumwechsel neu laden.

Enter rechnet um, Strg+R lädt aktuelle Kurse, Strg+S tauscht die Währungen.
Negative Werte, Exponentialschreibweise, Tausendertrennzeichen, mehr als acht
Nachkommastellen und Beträge über einer Billion werden abgewiesen.
Nur die Anzeige wird gerundet (ROUND_HALF_UP). CSV erhält Dezimalwerte ungerundet.
Der Gebührenvergleich nimmt für alle Angebote denselben Referenzkurs an;
individuelle Wechselkursaufschläge sind nicht enthalten.

## Datenqualität

Quelle: Frankfurter v1 / EZB, https://frankfurter.dev/v1/ .
Tagesreferenzkurse, keine Echtzeitkurse oder garantierten Bankangebote.
Wochenenden und Feiertage können das Kursdatum zurückliegen lassen.
v1 wird vom Anbieter weiterbetrieben, ist aber zugunsten von v2 abgekündigt.
Der Anbieterzugriff ist in quantumfx/core.py zentral gekapselt.

Online abgerufen: validierte API-Daten mit tatsächlichem Kursdatum.
Offline / gespeicherte Kurse: letzter gespeicherter Stand, auch wenn älter.
DEMO: undatierte Beispielwerte aus dem Originalprojekt, nur zum Ausprobieren.
Verlauf und CSV kennzeichnen diese Umrechnungen ausdrücklich als DEMO.
Diagramme verwenden nur abgerufene oder gespeicherte historische Daten.
Fehlende Daten werden nicht erfunden. Identische Währungspaare haben Kurs 1.

## Lokale Daten und Datenschutz

Standardordner: %LOCALAPPDATA%\QuantumFX
- settings.json: gewähltes Währungspaar und Favoriten.
- rates.json: letzter Kursstand mit Kurs- und Abrufdatum.
- chart-*.json: gespeicherte Zeitreihen nach Paar und Zeitraum.
- history.json: bis zu 1.000 Umrechnungen.
- QuantumFX.log: Fehlerprotokoll, maximal drei Dateien von je ca. 1 MB.

Beträge und Verlauf werden nicht an den Anbieter übertragen. Abfragen enthalten
nur Währungen, Zeitraum und normale Verbindungsdaten. Kein Konto, keine Telemetrie,
keine Broker-Verbindung, keine Handelsausführung.
QUANTUMFX_DATA_DIR kann für Tests oder getrennte Profile einen anderen Ordner setzen.
QuantumFX.exe --offline unterdrückt den automatischen Startabruf; manuelle Abrufe
bleiben möglich. Verlauf löschen entfernt die lokal gespeicherten Umrechnungen.

## Aus dem Quellcode starten und bauen

Python 3.10 oder neuer mit Tk. Keine externen Laufzeitpakete für die neue Anwendung.
Start: python main.py
Der ursprüngliche Dateiname startet ebenfalls die neue Anwendung.

Windows-Entwicklungsumgebung:
    python -m venv .venv
    .venv/Scripts/python.exe -m pip install -r requirements-dev.txt
    .venv/Scripts/python.exe -m pytest
    $env:QUANTUMFX_GUI_TESTS = '1'
    .venv/Scripts/python.exe -m pytest
    ./build.ps1 -Python .venv/Scripts/python.exe

Ergebnis: dist/QuantumFX.exe. Icon liegt bei. Nur die Neugenerierung mit
 tools/create_icon.py benötigt Pillow.

Verpackter Fenstertest mit temporärem Profil:
    ./dist/QuantumFX.exe --smoke-test C:/Pfad/smoke-result.json
Nach dem Prozessende enthält die JSON-Datei ok: true oder eine Fehlermeldung.
Tests unter tests/ prüfen die neue Produktionslogik. Historische Tests unter
legacy/ bleiben als Referenz archiviert und gehören nicht zur neuen Testsuite.

## Herkunft und Grenzen

Original-Commit: 1a431f630f32f57b2b93e8c1d1df5aab4b9cae38.
Original-Lizenz unverändert beigelegt. Die ursprüngliche README liegt unter legacy/.
Geprüft auf dem verfügbaren Windows-11-System (x64). Andere Windows-Versionen
und PCs sind nicht separat geprüft. Externer Kursdienst kann ausfallen.
Keine automatischen Updates. Kein Installer erforderlich.

Weiterentwicklung im Fork Eric-Enterprise/QuantumFX-Currency-Intelligence-Platform.
Das Original-Repository bleibt separat. Die Windows-EXE wird zusätzlich vom
GitHub-Actions-Workflow als herunterladbares Build-Artefakt bereitgestellt, wenn
Tests und Build erfolgreich durchlaufen. Ein GitHub-Release ist nicht erforderlich.
