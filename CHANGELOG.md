# Änderungen in 2.0.0

- Monolithischen Rechner in Daten-/Rechenlogik und Desktop-Oberfläche aufgeteilt.
- Windows-Paketierung mit eingebettetem Python/Tk und reproduzierbarem Build ergänzt.
- Neue deutsche Oberfläche mit fünf Bereichen und eigenem App-Icon.
- Acht fest vorgegebene Währungen durch die validierte API-Auswahl ersetzt.
- Tagesreferenzkurse mit echtem Kursdatum statt irreführender Echtzeit-Bezeichnung.
- Undatierte Ersatzkurse eindeutig als DEMO markiert; Kennzeichnung auch in CSV und Verlauf.
- Netzwerkabrufe aus dem GUI-Thread entfernt; verspätete Diagrammantworten verworfen.
- Float-Rechnung durch Decimal und explizite Eingabevalidierung ersetzt.
- Prozent-/Fixgebühren und Vergleich von drei selbst definierten Angeboten.
- Historische Kursdiagramme (30/90/365 Tage) mit Mauswerten und Offline-Zeitreihencache.
- Favoriten, Währungssuche, Kursübersicht, Verlauf und CSV-Export hinzugefügt.
- Sichere lokale Speicherung im Benutzerprofil, atomare JSON-Dateien und rotierende Logs.
- Neue Testsuite mit 61 Kern- und GUI-Tests sowie integriertem Paket-Selbsttest.
- Veraltete README und Sicherheitsvorlage durch konkrete Dokumentation ersetzt.
- Originalcode, ursprüngliche Tests und README unter legacy/ archiviert;
  Original-Lizenz unverändert erhalten. Neue EXE-Oberfläche ausschließlich Deutsch.
