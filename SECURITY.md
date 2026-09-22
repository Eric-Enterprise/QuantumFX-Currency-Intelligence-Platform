# Sicherheit und Datenschutz

Diese lokale Weiterentwicklung trägt die Version 2.0.0. Es gibt keinen
zugesicherten Supportzeitraum und keinen automatischen Updater.

Die Anwendung führt ausschließlich HTTPS-Leseabfragen an api.frankfurter.dev aus.
Zertifikate werden über Pythons Standard-TLS-Konfiguration geprüft. Beträge,
Gebühren und Verlauf verlassen die Anwendung nicht über den Kursabruf.

Cache-Dateien werden als JSON gelesen, strukturell geprüft und atomar ersetzt.
Aus lokalen Dateien wird kein Code ausgeführt. CSV-Exporte entschärfen führende
Formelzeichen. Lokale Daten sind nicht verschlüsselt und für andere Prozesse
mit den Rechten des Benutzers lesbar. Fehlerprotokolle werden größenbegrenzt.

Bei einem Fehler keine persönlichen Umrechnungsverläufe ungeprüft veröffentlichen.
Fehlerbeschreibung, Programmversion und bereinigte Protokollauszüge reichen
normalerweise zur Untersuchung. Zugang zu Rechner oder Datenordner nicht teilen.

Die EXE ist nicht digital signiert. Der beiliegende SHA-256-Wert dient der
Integritätsprüfung der gelieferten Datei, nicht als Ersatz für eine Herausgebersignatur.
