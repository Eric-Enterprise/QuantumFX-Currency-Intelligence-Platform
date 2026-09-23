"""Complete application catalogs and per-window translation; no process-global locale."""
LANGUAGES = {"en": "English", "de": "Deutsch", "ko": "한국어", "sv": "Svenska"}

CATALOGS = {'en': {'Language': 'Language',
        'Language could not be saved.': 'Language could not be saved.',
        'Swap source and target currencies · Ctrl+S': 'Swap source and target currencies · Ctrl+S',
        'Convert using the displayed rates and save the result to history · Enter': 'Convert using the displayed rates '
                                                                                    'and save the result to history · '
                                                                                    'Enter',
        'Toggle fullscreen · F11. Press Escape to return to a window.': 'Toggle fullscreen · F11. Press Escape to '
                                                                        'return to a window.',
        'Refresh daily reference rates in the background · Ctrl+R': 'Refresh daily reference rates in the background · '
                                                                    'Ctrl+R',
        'Refresh rates': 'Refresh rates',
        'Refresh': 'Refresh',
        'Your currency converter': 'Your currency converter',
        '1  Enter an amount': '1  Enter an amount',
        'For example 1234.56 · no thousands separators': 'For example 1234.56 · no thousands separators',
        'Use a dot or comma as the decimal separator, e.g. 1234.56. Enter converts and saves.': 'Use a dot or comma as '
                                                                                                'the decimal '
                                                                                                'separator, e.g. '
                                                                                                '1234.56. Enter '
                                                                                                'converts and saves.',
        '2  Choose currencies': '2  Choose currencies',
        'From': 'From',
        'To': 'To',
        'Add fees · optional': 'Add fees · optional',
        'Percentage deducted from the source amount, from 0 to 100.': 'Percentage deducted from the source amount, '
                                                                      'from 0 to 100.',
        'Fixed deduction in the source currency. For example, 2 means EUR 2 when converting from EUR.': 'Fixed '
                                                                                                        'deduction in '
                                                                                                        'the source '
                                                                                                        'currency. For '
                                                                                                        'example, 2 '
                                                                                                        'means EUR 2 '
                                                                                                        'when '
                                                                                                        'converting '
                                                                                                        'from EUR.',
        'Convert & save  ↗': 'Convert & save  ↗',
        'Copy': 'Copy',
        'Rate trends': 'Rate trends',
        'Load history': 'Load history',
        'Favorites · double-click to open': 'Favorites · double-click to open',
        'All available currencies': 'All available currencies',
        "Rates per 1 unit of the converter's source currency. Double-click to select a target currency.": 'Rates per 1 '
                                                                                                          'unit of the '
                                                                                                          "converter's "
                                                                                                          'source '
                                                                                                          'currency. '
                                                                                                          'Double-click '
                                                                                                          'to select a '
                                                                                                          'target '
                                                                                                          'currency.',
        'Search by currency code, e.g. EUR or USD · Ctrl+F': 'Search by currency code, e.g. EUR or USD · Ctrl+F',
        'Your recent conversions': 'Your recent conversions',
        'Up to 1,000 entries are stored locally. CSV decimal values are not rounded.': 'Up to 1,000 entries are stored '
                                                                                       'locally. CSV decimal values '
                                                                                       'are not rounded.',
        'Understanding your numbers and data': 'Understanding your numbers and data',
        'What is left after fees?': 'What is left after fees?',
        'Compare three offers using the amount and currency pair from the converter.': 'Compare three offers using the '
                                                                                       'amount and currency pair from '
                                                                                       'the converter.',
        'Assumes the same reference rate. Percentage and fixed fees are deducted in the source currency.': 'Assumes '
                                                                                                           'the same '
                                                                                                           'reference '
                                                                                                           'rate. '
                                                                                                           'Percentage '
                                                                                                           'and fixed '
                                                                                                           'fees are '
                                                                                                           'deducted '
                                                                                                           'in the '
                                                                                                           'source '
                                                                                                           'currency.',
        'Loading rates in the background …': 'Loading rates in the background …',
        'Recalculate': 'Recalculate',
        'Pair changed · reload the chart.': 'Pair changed · reload the chart.',
        'Clear history': 'Clear history',
        'Permanently delete all saved conversions?': 'Permanently delete all saved conversions?',
        'Loading historical reference rates …': 'Loading historical reference rates …',
        'This action failed. See the local log file for details.': 'This action failed. See the local log file for '
                                                                   'details.',
        'Ready to convert': 'Ready to convert',
        'Choose a currency pair and load its rate history.': 'Choose a currency pair and load its rate history.',
        'Effects on': 'Effects on',
        'Effects off': 'Effects off',
        'Turn animations on or off. Your preference is saved.': 'Turn animations on or off. Your preference is saved.',
        'Overview': 'Overview',
        'Converter': 'Converter',
        'Currencies': 'Currencies',
        'Fees': 'Fees',
        'History': 'History',
        'Snake': 'Snake',
        'Help': 'Help',
        'Show optional percentage and fixed fees. Leave them at zero for no deductions.': 'Show optional percentage '
                                                                                          'and fixed fees. Leave them '
                                                                                          'at zero for no deductions.',
        'Offer': 'Offer',
        'Fee %': 'Fee %',
        'Fixed fee (source)': 'Fixed fee (source)',
        'Enter your own fees and compare offers.': 'Enter your own fees and compare offers.',
        'Inputs or rates changed · compare offers again.': 'Inputs or rates changed · compare offers again.',
        'DEMO · Undated sample rates · Do not use for actual conversions': 'DEMO · Undated sample rates · Do not use '
                                                                           'for actual conversions',
        'Retrieved online': 'Retrieved online',
        'Offline / saved rates': 'Offline / saved rates',
        'Result copied.': 'Result copied.',
        'This pair is not available in the current rate snapshot.': 'This pair is not available in the current rate '
                                                                    'snapshot.',
        'Export CSV': 'Export CSV',
        'Load a rate history first.': 'Load a rate history first.',
        'Close': 'Close',
        '★ Save pair': '★ Save pair',
        'Export chart CSV': 'Export chart CSV',
        'Remove selected pair': 'Remove selected pair',
        'Hide fees': 'Hide fees',
        'Window  Esc': 'Window  Esc',
        'Fullscreen  F11': 'Fullscreen  F11',
        'Could not save display preferences.': 'Could not save display preferences.',
        'Reset': 'Reset',
        'Export rates as CSV': 'Export rates as CSV',
        'Currency': 'Currency',
        'Rate': 'Rate',
        'Base': 'Base',
        'Rate date / source': 'Rate date / source',
        'Time': 'Time',
        'Amount': 'Amount',
        'Currency pair': 'Currency pair',
        'Result': 'Result',
        'Fee (source)': 'Fee (source)',
        'Rate date': 'Rate date',
        'Source': 'Source',
        'Compare offers': 'Compare offers',
        'Fees (source)': 'Fees (source)',
        'Payout (target)': 'Payout (target)',
        'Difference from best offer': 'Difference from best offer',
        'Check your input': 'Check your input',
        'Could not save favorites.': 'Could not save favorites.',
        'Export': 'Export',
        'CSV file saved.': 'CSV file saved.',
        'Selection changed · reload the chart.': 'Selection changed · reload the chart.',
        'Load rate history to see the trend': 'Load rate history to see the trend',
        'Frankfurter / ECB · Daily reference rates · Fees are your own estimates.': 'Frankfurter / ECB · Daily '
                                                                                    'reference rates · Fees are your '
                                                                                    'own estimates.',
        'Percent %': 'Percent %',
        'Fixed fee': 'Fixed fee',
        'Period (days)': 'Period (days)',
        'Fees active · edit': 'Fees active · edit',
        'Find currency': 'Find currency',
        'Conversion saved locally.': 'Conversion saved locally.',
        'Converted, but history could not be saved.': 'Converted, but history could not be saved.',
        'Export failed': 'Export failed',
        'Deletion failed': 'Deletion failed',
        ' DEMO rates used.': ' DEMO rates used.',
        'Cache': 'Cache',
        'Reference rates': 'Reference rates',
        'Pause / Resume': 'Pause / Resume',
        'Normal': 'Normal',
        'Arrow keys or WASD · Space to pause · Enter to restart': 'Arrow keys or WASD · Space to pause · Enter to '
                                                                  'restart',
        'YOU WIN!': 'YOU WIN!',
        'New game': 'New game',
        'Relaxed': 'Relaxed',
        'Fast': 'Fast',
        'GAME OVER': 'GAME OVER',
        'New game / Space': 'New game / Space',
        'A little break. A longer snake.': 'A little break. A longer snake.',
        'High score is kept for this session; saving failed.': 'High score is kept for this session; saving failed.',
        'PAUSE': 'PAUSE',
        'SNAKE ARCADE': 'SNAKE ARCADE',
        'Your money. In any currency.': 'Your money. In any currency.',
        'Enter an amount. Choose currencies. Get clarity.': 'Enter an amount. Choose currencies. Get clarity.',
        'Your result · after fees': 'Your result · after fees',
        'Enter a number without thousands separators, e.g. 1234.56 (up to 8 decimal places).': 'Enter a number without '
                                                                                               'thousands separators, '
                                                                                               'e.g. 1234.56 (up to 8 '
                                                                                               'decimal places).',
        'Amount must not exceed 1,000,000,000,000.': 'Amount must not exceed 1,000,000,000,000.',
        'No valid rate data.': 'No valid rate data.',
        'Invalid cache.': 'Invalid cache.',
        'Invalid cache date.': 'Invalid cache date.',
        'Invalid base currency.': 'Invalid base currency.',
        'Percentage fee must be between 0 and 100.': 'Percentage fee must be between 0 and 100.',
        'Currency not available in this rate snapshot.': 'Currency not available in this rate snapshot.',
        'Fees exceed the source amount.': 'Fees exceed the source amount.',
        'Invalid number.': 'Invalid number.',
        'Invalid currency.': 'Invalid currency.',
        'Invalid rate.': 'Invalid rate.',
        'Response is too large.': 'Response is too large.',
        'Rates loaded; the local cache could not be saved.': 'Rates loaded; the local cache could not be saved.',
        'Invalid period or currency.': 'Invalid period or currency.',
        'Negative or invalid amounts are not allowed.': 'Negative or invalid amounts are not allowed.',
        'Incorrect base currency.': 'Incorrect base currency.',
        'Rate date is in the future.': 'Rate date is in the future.',
        'Invalid time series.': 'Invalid time series.',
        'No rates available for the selected period.': 'No rates available for the selected period.',
        'Rate history is unavailable. Check your internet connection and try again.': 'Rate history is unavailable. '
                                                                                      'Check your internet connection '
                                                                                      'and try again.',
        'Request failed: {error}': 'Request failed: {error}',
        'Offer {n}': 'Offer {n}',
        '{amount} {base} → {target} · Rate date {date} · Sorted by payout. Individual exchange-rate markups are not included.': '{amount} '
                                                                                                                                '{base} '
                                                                                                                                '→ '
                                                                                                                                '{target} '
                                                                                                                                '· '
                                                                                                                                'Rate '
                                                                                                                                'date '
                                                                                                                                '{date} '
                                                                                                                                '· '
                                                                                                                                'Sorted '
                                                                                                                                'by '
                                                                                                                                'payout. '
                                                                                                                                'Individual '
                                                                                                                                'exchange-rate '
                                                                                                                                'markups '
                                                                                                                                'are '
                                                                                                                                'not '
                                                                                                                                'included.',
        '{source} · Rate date {date} · {count} currencies · Frankfurter / ECB': '{source} · Rate date {date} · {count} '
                                                                                'currencies · Frankfurter / ECB',
        '1 {base} = {rate} {target}\nFees: {fee} {base}\nBefore fees: {gross} {target}': '1 {base} = {rate} {target}\n'
                                                                                         'Fees: {fee} {base}\n'
                                                                                         'Before fees: {gross} '
                                                                                         '{target}',
        '{pair} · {change} % over the available period · {count} data points · {source}': '{pair} · {change} % over '
                                                                                          'the available period · '
                                                                                          '{count} data points · '
                                                                                          '{source}',
        'SCORE  {score}     /     BEST  {best}': 'SCORE  {score}     /     BEST  {best}',
        'help_body': 'HOW IT WORKS\n'
                     'Choose an amount and currency pair. Use a dot or comma for decimals, without thousands '
                     'separators. Percentage and fixed fees are deducted before conversion. Only displayed amounts are '
                     'rounded.\n'
                     '\n'
                     'RATE SOURCES\n'
                     'Online: daily ECB reference rates from Frankfurter. Dates may be older on weekends and holidays. '
                     'Offline: saved rates with their original date. DEMO: undated examples, not for actual '
                     'conversions. Charts use only retrieved or saved historical data.\n'
                     '\n'
                     'CONTROLS\n'
                     'Enter converts and saves. Ctrl+R refreshes rates. Ctrl+S swaps currencies. Ctrl+F opens search. '
                     'F11 toggles fullscreen. Escape leaves fullscreen and pauses Snake. Hover over charts for values. '
                     'Reload charts after changing pairs. Animations can be disabled in the sidebar.\n'
                     '\n'
                     'PRIVACY\n'
                     'Amounts, fees and history stay on this computer. The provider receives currency pairs, date '
                     'ranges and standard connection information. No account or telemetry. CSV files are saved only '
                     'where you choose.\n'
                     '\n'
                     'LANGUAGE\n'
                     'Choose a language in the sidebar. The interface updates immediately and your preference is '
                     'saved. Snake pauses during a language change. System file dialogs may follow your Windows '
                     'language.\n'
                     '\n'
                     'LOCAL DATA\n'
                     '{folder}\n'
                     '\n'
                     'QuantumFX {version}\n'
                     'Original project: oneiric-hammer/QuantumFX-Currency-Intelligence-Platform. The original license '
                     'is included.'},
 'de': {'Language': 'Sprache',
        'Language could not be saved.': 'Sprache konnte nicht gespeichert werden.',
        'Swap source and target currencies · Ctrl+S': 'Ausgangs- und Zielwährung tauschen · Strg+S',
        'Convert using the displayed rates and save the result to history · Enter': 'Berechnet mit den angezeigten '
                                                                                    'Kursen und speichert das Ergebnis '
                                                                                    'im Verlauf · Enter',
        'Toggle fullscreen · F11. Press Escape to return to a window.': 'Vollbild ein- oder ausschalten · F11. Escape '
                                                                        'führt zurück ins Fenster.',
        'Refresh daily reference rates in the background · Ctrl+R': 'Tagesreferenzkurse im Hintergrund aktualisieren · '
                                                                    'Strg+R',
        'Refresh rates': 'Kurse aktualisieren',
        'Refresh': 'Aktualisieren',
        'Your currency converter': 'Dein Währungsrechner',
        '1  Enter an amount': '1  Betrag eingeben',
        'For example 1234.56 · no thousands separators': 'Zum Beispiel 1234,56 · ohne Tausendertrennzeichen',
        'Use a dot or comma as the decimal separator, e.g. 1234.56. Enter converts and saves.': 'Komma oder Punkt als '
                                                                                                'Dezimaltrennzeichen, '
                                                                                                'z. B. 1234,56. Enter '
                                                                                                'berechnet und '
                                                                                                'speichert.',
        '2  Choose currencies': '2  Währungen wählen',
        'From': 'Von',
        'To': 'Nach',
        'Add fees · optional': 'Gebühren hinzufügen · optional',
        'Percentage deducted from the source amount, from 0 to 100.': 'Prozentualer Abzug vom Ausgangsbetrag, zwischen '
                                                                      '0 und 100.',
        'Fixed deduction in the source currency. For example, 2 means EUR 2 when converting from EUR.': 'Fester Abzug '
                                                                                                        'in der '
                                                                                                        'Von-Währung. '
                                                                                                        'Beispiel: 2 '
                                                                                                        'bedeutet 2 '
                                                                                                        'EUR bei '
                                                                                                        'Ausgangswährung '
                                                                                                        'EUR.',
        'Convert & save  ↗': 'Umrechnen & speichern  ↗',
        'Copy': 'Kopieren',
        'Rate trends': 'Kursentwicklung',
        'Load history': 'Verlauf laden',
        'Favorites · double-click to open': 'Favoriten · Doppelklick zum Öffnen',
        'All available currencies': 'Alle verfügbaren Währungen',
        "Rates per 1 unit of the converter's source currency. Double-click to select a target currency.": 'Kurse je 1 '
                                                                                                          'Einheit der '
                                                                                                          'Ausgangswährung '
                                                                                                          'im Rechner. '
                                                                                                          'Doppelklick '
                                                                                                          'übernimmt '
                                                                                                          'die '
                                                                                                          'Zielwährung.',
        'Search by currency code, e.g. EUR or USD · Ctrl+F': 'Nach Währungskürzel suchen, z. B. EUR oder USD · Strg+F',
        'Your recent conversions': 'Deine letzten Umrechnungen',
        'Up to 1,000 entries are stored locally. CSV decimal values are not rounded.': 'Bis zu 1.000 Einträge werden '
                                                                                       'lokal gespeichert. '
                                                                                       'Dezimalwerte im CSV bleiben '
                                                                                       'ungerundet.',
        'Understanding your numbers and data': 'Klarheit über Zahlen und Daten',
        'What is left after fees?': 'Was bleibt nach den Gebühren?',
        'Compare three offers using the amount and currency pair from the converter.': 'Vergleiche drei eigene '
                                                                                       'Angebote mit dem Betrag und '
                                                                                       'Währungspaar aus dem Rechner.',
        'Assumes the same reference rate. Percentage and fixed fees are deducted in the source currency.': 'Annahme: '
                                                                                                           'gleicher '
                                                                                                           'Referenzkurs. '
                                                                                                           'Prozent '
                                                                                                           'und '
                                                                                                           'Fixbetrag '
                                                                                                           'werden in '
                                                                                                           'der '
                                                                                                           'Ausgangswährung '
                                                                                                           'abgezogen.',
        'Loading rates in the background …': 'Kurse werden im Hintergrund geladen …',
        'Recalculate': 'Neu berechnen',
        'Pair changed · reload the chart.': 'Paar geändert · Verlauf erneut laden.',
        'Clear history': 'Verlauf löschen',
        'Permanently delete all saved conversions?': 'Alle gespeicherten Umrechnungen unwiderruflich löschen?',
        'Loading historical reference rates …': 'Historische Referenzkurse werden geladen …',
        'This action failed. See the local log file for details.': 'Diese Aktion ist fehlgeschlagen. Details stehen in '
                                                                   'der lokalen Protokolldatei.',
        'Ready to convert': 'Bereit zum Umrechnen',
        'Choose a currency pair and load its rate history.': 'Währungspaar wählen und Kursverlauf laden.',
        'Effects on': 'Effekte an',
        'Effects off': 'Effekte aus',
        'Turn animations on or off. Your preference is saved.': 'Animationen ein- oder ausschalten. Die Einstellung '
                                                                'bleibt gespeichert.',
        'Overview': 'Übersicht',
        'Converter': 'Rechner',
        'Currencies': 'Währungen',
        'Fees': 'Gebühren',
        'History': 'Verlauf',
        'Snake': 'Snake',
        'Help': 'Hilfe',
        'Show optional percentage and fixed fees. Leave them at zero for no deductions.': 'Optionale Prozent- und '
                                                                                          'Fixgebühren öffnen. Ohne '
                                                                                          'Eingabe wird keine Gebühr '
                                                                                          'abgezogen.',
        'Offer': 'Angebot',
        'Fee %': 'Gebühr in %',
        'Fixed fee (source)': 'Fixgebühr (Basis)',
        'Enter your own fees and compare offers.': 'Eigene Gebühren eintragen und vergleichen.',
        'Inputs or rates changed · compare offers again.': 'Eingaben oder Kurse geändert · Vergleich erneut berechnen.',
        'DEMO · Undated sample rates · Do not use for actual conversions': 'DEMO · Beispielkurse ohne Kursdatum · '
                                                                           'Nicht für tatsächliche Umrechnungen '
                                                                           'verwenden',
        'Retrieved online': 'Online abgerufen',
        'Offline / saved rates': 'Offline / gespeicherte Kurse',
        'Result copied.': 'Ergebnis kopiert.',
        'This pair is not available in the current rate snapshot.': 'Dieses Paar ist im aktuellen Kursstand nicht '
                                                                    'verfügbar.',
        'Export CSV': 'CSV exportieren',
        'Load a rate history first.': 'Zuerst einen Kursverlauf laden.',
        'Close': 'Schließen',
        '★ Save pair': '★ Paar merken',
        'Export chart CSV': 'Diagrammdaten als CSV',
        'Remove selected pair': 'Ausgewähltes Paar entfernen',
        'Hide fees': 'Gebühren ausblenden',
        'Window  Esc': 'Fenster  Esc',
        'Fullscreen  F11': 'Vollbild  F11',
        'Could not save display preferences.': 'Darstellung konnte nicht gespeichert werden.',
        'Reset': 'Zurücksetzen',
        'Export rates as CSV': 'Kurse als CSV exportieren',
        'Currency': 'Währung',
        'Rate': 'Kurs',
        'Base': 'Basis',
        'Rate date / source': 'Kursdatum / Quelle',
        'Time': 'Zeit',
        'Amount': 'Betrag',
        'Currency pair': 'Währungspaar',
        'Result': 'Ergebnis',
        'Fee (source)': 'Gebühr (Basis)',
        'Rate date': 'Kursdatum',
        'Source': 'Quelle',
        'Compare offers': 'Angebote vergleichen',
        'Fees (source)': 'Gebühren (Basis)',
        'Payout (target)': 'Auszahlung (Ziel)',
        'Difference from best offer': 'Abstand zum besten Angebot',
        'Check your input': 'Eingabe prüfen',
        'Could not save favorites.': 'Favoriten konnten nicht gespeichert werden.',
        'Export': 'Export',
        'CSV file saved.': 'CSV-Datei gespeichert.',
        'Selection changed · reload the chart.': 'Auswahl geändert · Verlauf erneut laden.',
        'Load rate history to see the trend': 'Kursverlauf laden, um die Entwicklung zu sehen',
        'Frankfurter / ECB · Daily reference rates · Fees are your own estimates.': 'Frankfurter / EZB · '
                                                                                    'Tagesreferenzkurse · Gebühren '
                                                                                    'sind eigene Annahmen.',
        'Percent %': 'Prozent %',
        'Fixed fee': 'Fixbetrag',
        'Period (days)': 'Zeitraum (Tage)',
        'Fees active · edit': 'Gebühren aktiv · bearbeiten',
        'Find currency': 'Währung suchen',
        'Conversion saved locally.': 'Umrechnung lokal gespeichert.',
        'Converted, but history could not be saved.': 'Berechnet; Verlauf konnte nicht gespeichert werden.',
        'Export failed': 'Export fehlgeschlagen',
        'Deletion failed': 'Löschen fehlgeschlagen',
        ' DEMO rates used.': ' DEMO-Kurse verwendet.',
        'Cache': 'Cache',
        'Reference rates': 'Referenzkurse',
        'Pause / Resume': 'Pause / Weiter',
        'Normal': 'Normal',
        'Arrow keys or WASD · Space to pause · Enter to restart': 'Pfeiltasten oder WASD · Leertaste pausiert · Enter '
                                                                  'startet neu',
        'YOU WIN!': 'GEWONNEN!',
        'New game': 'Neues Spiel',
        'Relaxed': 'Entspannt',
        'Fast': 'Schnell',
        'GAME OVER': 'SPIEL VORBEI',
        'New game / Space': 'Neues Spiel / Leertaste',
        'A little break. A longer snake.': 'Eine kleine Pause. Eine große Schlange.',
        'High score is kept for this session; saving failed.': 'Highscore bleibt für diese Sitzung erhalten; Speichern '
                                                               'fehlgeschlagen.',
        'PAUSE': 'PAUSE',
        'SNAKE ARCADE': 'SNAKE ARCADE',
        'Your money. In any currency.': 'Dein Geld. In jeder Währung.',
        'Enter an amount. Choose currencies. Get clarity.': 'Betrag eingeben. Währungen wählen. Klarheit gewinnen.',
        'Your result · after fees': 'Dein Ergebnis · nach Gebühren',
        'Enter a number without thousands separators, e.g. 1234.56 (up to 8 decimal places).': 'Zahl ohne '
                                                                                               'Tausendertrennzeichen '
                                                                                               'eingeben, z. B. '
                                                                                               '1234,56 (max. 8 '
                                                                                               'Nachkommastellen).',
        'Amount must not exceed 1,000,000,000,000.': 'Betrag darf höchstens 1.000.000.000.000 sein.',
        'No valid rate data.': 'Keine gültigen Kursdaten.',
        'Invalid cache.': 'Ungültiger Cache.',
        'Invalid cache date.': 'Ungültiges Cache-Datum.',
        'Invalid base currency.': 'Ungültige Basiswährung.',
        'Percentage fee must be between 0 and 100.': 'Prozentuale Gebühr muss zwischen 0 und 100 liegen.',
        'Currency not available in this rate snapshot.': 'Währung in diesem Kursstand nicht verfügbar.',
        'Fees exceed the source amount.': 'Die Gebühren übersteigen den Ausgangsbetrag.',
        'Invalid number.': 'Ungültige Zahl.',
        'Invalid currency.': 'Ungültige Währung.',
        'Invalid rate.': 'Ungültiger Kurs.',
        'Response is too large.': 'Antwort ist zu groß.',
        'Rates loaded; the local cache could not be saved.': 'Kurse geladen; lokaler Cache konnte nicht gespeichert '
                                                             'werden.',
        'Invalid period or currency.': 'Ungültiger Zeitraum oder Währung.',
        'Negative or invalid amounts are not allowed.': 'Negative oder ungültige Beträge sind nicht erlaubt.',
        'Incorrect base currency.': 'Falsche Basiswährung.',
        'Rate date is in the future.': 'Kursdatum liegt in der Zukunft.',
        'Invalid time series.': 'Ungültige Zeitreihe.',
        'No rates available for the selected period.': 'Keine Kurse im gewählten Zeitraum verfügbar.',
        'Rate history is unavailable. Check your internet connection and try again.': 'Kursverlauf nicht verfügbar. '
                                                                                      'Internetverbindung prüfen und '
                                                                                      'erneut laden.',
        'Request failed: {error}': 'Abruf fehlgeschlagen: {error}',
        'Offer {n}': 'Angebot {n}',
        '{amount} {base} → {target} · Rate date {date} · Sorted by payout. Individual exchange-rate markups are not included.': '{amount} '
                                                                                                                                '{base} '
                                                                                                                                '→ '
                                                                                                                                '{target} '
                                                                                                                                '· '
                                                                                                                                'Kursdatum '
                                                                                                                                '{date} '
                                                                                                                                '· '
                                                                                                                                'Nach '
                                                                                                                                'Auszahlung '
                                                                                                                                'sortiert. '
                                                                                                                                'Individuelle '
                                                                                                                                'Wechselkursaufschläge '
                                                                                                                                'sind '
                                                                                                                                'nicht '
                                                                                                                                'enthalten.',
        '{source} · Rate date {date} · {count} currencies · Frankfurter / ECB': '{source} · Kursdatum {date} · {count} '
                                                                                'Währungen · Frankfurter / EZB',
        '1 {base} = {rate} {target}\nFees: {fee} {base}\nBefore fees: {gross} {target}': '1 {base} = {rate} {target}\n'
                                                                                         'Gebühren: {fee} {base}\n'
                                                                                         'Ohne Gebühren: {gross} '
                                                                                         '{target}',
        '{pair} · {change} % over the available period · {count} data points · {source}': '{pair} · {change} % im '
                                                                                          'verfügbaren Zeitraum · '
                                                                                          '{count} Datenpunkte · '
                                                                                          '{source}',
        'SCORE  {score}     /     BEST  {best}': 'PUNKTE  {score}     /     BESTLEISTUNG  {best}',
        'help_body': 'SO FUNKTIONIERT ES\n'
                     'Betrag und Währungspaar wählen. Punkt oder Komma als Dezimaltrennzeichen verwenden, ohne '
                     'Tausendertrennzeichen. Prozentuale und fixe Gebühren werden vor der Umrechnung abgezogen. Nur '
                     'die Anzeige wird gerundet.\n'
                     '\n'
                     'KURSQUELLEN\n'
                     'Online: tägliche EZB-Referenzkurse von Frankfurter. An Wochenenden und Feiertagen kann das Datum '
                     'zurückliegen. Offline: gespeicherte Kurse mit ursprünglichem Datum. DEMO: undatierte Beispiele, '
                     'nicht für echte Umrechnungen. Diagramme verwenden nur abgerufene oder gespeicherte historische '
                     'Daten.\n'
                     '\n'
                     'BEDIENUNG\n'
                     'Enter rechnet um und speichert. Strg+R aktualisiert Kurse. Strg+S tauscht Währungen. Strg+F '
                     'öffnet die Suche. F11 wechselt Vollbild. Escape verlässt Vollbild und pausiert Snake. Maus über '
                     'Diagrammpunkte bewegen, um Werte abzulesen. Nach Paarwechsel Diagramm neu laden. Animationen '
                     'lassen sich in der Seitenleiste abschalten.\n'
                     '\n'
                     'DATENSCHUTZ\n'
                     'Beträge, Gebühren und Verlauf bleiben auf diesem Computer. Der Anbieter erhält Währungspaare, '
                     'Zeiträume und übliche Verbindungsdaten. Kein Konto, keine Telemetrie. CSV-Dateien werden nur am '
                     'gewählten Ort gespeichert.\n'
                     '\n'
                     'SPRACHE\n'
                     'Sprache in der Seitenleiste auswählen. Die Oberfläche ändert sich sofort; die Einstellung wird '
                     'gespeichert. Snake pausiert beim Sprachwechsel. Systemdateidialoge können die Windows-Sprache '
                     'verwenden.\n'
                     '\n'
                     'LOKALE DATEN\n'
                     '{folder}\n'
                     '\n'
                     'QuantumFX {version}\n'
                     'Originalprojekt: oneiric-hammer/QuantumFX-Currency-Intelligence-Platform. Die Original-Lizenz '
                     'ist beigefügt.'},
 'ko': {'Language': '언어',
        'Language could not be saved.': '언어 설정을 저장하지 못했습니다.',
        'Swap source and target currencies · Ctrl+S': '기준 통화와 대상 통화 바꾸기 · Ctrl+S',
        'Convert using the displayed rates and save the result to history · Enter': '표시된 환율로 환산하고 내역에 저장 · Enter',
        'Toggle fullscreen · F11. Press Escape to return to a window.': '전체 화면 전환 · F11. Esc를 누르면 창 모드로 돌아갑니다.',
        'Refresh daily reference rates in the background · Ctrl+R': '백그라운드에서 일일 기준 환율 업데이트 · Ctrl+R',
        'Refresh rates': '환율 업데이트',
        'Refresh': '새로고침',
        'Your currency converter': '나의 환율 계산기',
        '1  Enter an amount': '1  금액 입력',
        'For example 1234.56 · no thousands separators': '예: 1234.56 · 천 단위 구분 기호 없이 입력',
        'Use a dot or comma as the decimal separator, e.g. 1234.56. Enter converts and saves.': '소수점은 점 또는 쉼표를 사용하세요. '
                                                                                                '예: 1234.56. Enter로 '
                                                                                                '환산하고 저장합니다.',
        '2  Choose currencies': '2  통화 선택',
        'From': '기준 통화',
        'To': '대상 통화',
        'Add fees · optional': '수수료 추가 · 선택 사항',
        'Percentage deducted from the source amount, from 0 to 100.': '기준 금액에서 차감할 비율입니다. 0~100 사이로 입력하세요.',
        'Fixed deduction in the source currency. For example, 2 means EUR 2 when converting from EUR.': '기준 통화로 차감할 고정 '
                                                                                                        '수수료입니다. 기준 '
                                                                                                        '통화가 EUR이면 2는 '
                                                                                                        '2유로입니다.',
        'Convert & save  ↗': '환산 및 저장  ↗',
        'Copy': '복사',
        'Rate trends': '환율 추이',
        'Load history': '환율 내역 불러오기',
        'Favorites · double-click to open': '즐겨찾기 · 두 번 클릭하여 열기',
        'All available currencies': '사용 가능한 모든 통화',
        "Rates per 1 unit of the converter's source currency. Double-click to select a target currency.": '기준 통화 1단위당 '
                                                                                                          '환율입니다. 두 번 '
                                                                                                          '클릭하여 대상 통화를 '
                                                                                                          '선택하세요.',
        'Search by currency code, e.g. EUR or USD · Ctrl+F': '통화 코드로 검색, 예: EUR 또는 USD · Ctrl+F',
        'Your recent conversions': '최근 환산 내역',
        'Up to 1,000 entries are stored locally. CSV decimal values are not rounded.': '최대 1,000건을 이 기기에 저장합니다. CSV 소수 '
                                                                                       '값은 반올림하지 않습니다.',
        'Understanding your numbers and data': '수치와 데이터 안내',
        'What is left after fees?': '수수료 차감 후 얼마가 남을까요?',
        'Compare three offers using the amount and currency pair from the converter.': '계산기의 금액과 통화 쌍으로 세 가지 조건을 '
                                                                                       '비교하세요.',
        'Assumes the same reference rate. Percentage and fixed fees are deducted in the source currency.': '동일한 기준 환율을 '
                                                                                                           '가정합니다. 비율 '
                                                                                                           '및 고정 수수료는 '
                                                                                                           '기준 통화에서 '
                                                                                                           '차감됩니다.',
        'Loading rates in the background …': '백그라운드에서 환율을 불러오는 중 …',
        'Recalculate': '다시 계산',
        'Pair changed · reload the chart.': '통화 쌍 변경됨 · 차트를 다시 불러오세요.',
        'Clear history': '내역 삭제',
        'Permanently delete all saved conversions?': '저장된 환산 내역을 모두 영구 삭제할까요?',
        'Loading historical reference rates …': '과거 기준 환율을 불러오는 중 …',
        'This action failed. See the local log file for details.': '작업에 실패했습니다. 자세한 내용은 이 기기의 로그 파일을 확인하세요.',
        'Ready to convert': '환산 준비 완료',
        'Choose a currency pair and load its rate history.': '통화 쌍을 선택하고 환율 내역을 불러오세요.',
        'Effects on': '효과 켜짐',
        'Effects off': '효과 꺼짐',
        'Turn animations on or off. Your preference is saved.': '애니메이션을 켜거나 끕니다. 설정이 저장됩니다.',
        'Overview': '개요',
        'Converter': '환율 계산기',
        'Currencies': '통화',
        'Fees': '수수료',
        'History': '내역',
        'Snake': '스네이크',
        'Help': '도움말',
        'Show optional percentage and fixed fees. Leave them at zero for no deductions.': '비율 및 고정 수수료 입력란을 표시합니다. '
                                                                                          '수수료가 없으면 0으로 두세요.',
        'Offer': '조건',
        'Fee %': '수수료 %',
        'Fixed fee (source)': '고정 수수료 (기준)',
        'Enter your own fees and compare offers.': '수수료를 입력하여 조건을 비교하세요.',
        'Inputs or rates changed · compare offers again.': '입력값 또는 환율 변경됨 · 다시 비교하세요.',
        'DEMO · Undated sample rates · Do not use for actual conversions': '데모 · 날짜 없는 예시 환율 · 실제 환산에 사용하지 마세요',
        'Retrieved online': '온라인 환율',
        'Offline / saved rates': '오프라인 / 저장된 환율',
        'Result copied.': '결과를 복사했습니다.',
        'This pair is not available in the current rate snapshot.': '현재 환율 데이터에서 이 통화 쌍을 사용할 수 없습니다.',
        'Export CSV': 'CSV 내보내기',
        'Load a rate history first.': '먼저 환율 내역을 불러오세요.',
        'Close': '닫기',
        '★ Save pair': '★ 통화 쌍 저장',
        'Export chart CSV': '차트 CSV 내보내기',
        'Remove selected pair': '선택한 통화 쌍 삭제',
        'Hide fees': '수수료 숨기기',
        'Window  Esc': '창 모드  Esc',
        'Fullscreen  F11': '전체 화면  F11',
        'Could not save display preferences.': '화면 설정을 저장하지 못했습니다.',
        'Reset': '초기화',
        'Export rates as CSV': '환율 CSV 내보내기',
        'Currency': '통화',
        'Rate': '환율',
        'Base': '기준',
        'Rate date / source': '환율 기준일 / 출처',
        'Time': '시간',
        'Amount': '금액',
        'Currency pair': '통화 쌍',
        'Result': '결과',
        'Fee (source)': '수수료 (기준)',
        'Rate date': '환율 기준일',
        'Source': '출처',
        'Compare offers': '조건 비교',
        'Fees (source)': '수수료 (기준)',
        'Payout (target)': '수령액 (대상)',
        'Difference from best offer': '최고 조건과의 차이',
        'Check your input': '입력값을 확인하세요',
        'Could not save favorites.': '즐겨찾기를 저장하지 못했습니다.',
        'Export': '내보내기',
        'CSV file saved.': 'CSV 파일을 저장했습니다.',
        'Selection changed · reload the chart.': '선택 변경됨 · 차트를 다시 불러오세요.',
        'Load rate history to see the trend': '추이를 보려면 환율 내역을 불러오세요',
        'Frankfurter / ECB · Daily reference rates · Fees are your own estimates.': 'Frankfurter / ECB · 일일 기준 환율 · '
                                                                                    '수수료는 직접 입력한 추정값입니다.',
        'Percent %': '비율 %',
        'Fixed fee': '고정 수수료',
        'Period (days)': '기간 (일)',
        'Fees active · edit': '수수료 적용 중 · 수정',
        'Find currency': '통화 검색',
        'Conversion saved locally.': '환산 내역을 이 기기에 저장했습니다.',
        'Converted, but history could not be saved.': '환산했지만 내역을 저장하지 못했습니다.',
        'Export failed': '내보내기 실패',
        'Deletion failed': '삭제 실패',
        ' DEMO rates used.': ' 데모 환율이 사용되었습니다.',
        'Cache': '저장된 데이터',
        'Reference rates': '기준 환율',
        'Pause / Resume': '일시 정지 / 계속',
        'Normal': '보통',
        'Arrow keys or WASD · Space to pause · Enter to restart': '방향키 또는 WASD · Space로 일시 정지 · Enter로 새 게임',
        'YOU WIN!': '승리!',
        'New game': '새 게임',
        'Relaxed': '느리게',
        'Fast': '빠르게',
        'GAME OVER': '게임 종료',
        'New game / Space': '새 게임 / Space',
        'A little break. A longer snake.': '잠깐의 휴식. 더 길어진 뱀.',
        'High score is kept for this session; saving failed.': '저장에 실패했습니다. 최고 점수는 이번 실행 중에만 유지됩니다.',
        'PAUSE': '일시 정지',
        'SNAKE ARCADE': '스네이크 아케이드',
        'Your money. In any currency.': '어떤 통화든, 내 돈을 한눈에.',
        'Enter an amount. Choose currencies. Get clarity.': '금액 입력. 통화 선택. 명확한 결과.',
        'Your result · after fees': '수수료 차감 후 결과',
        'Enter a number without thousands separators, e.g. 1234.56 (up to 8 decimal places).': '천 단위 구분 기호 없이 숫자를 '
                                                                                               '입력하세요. 예: 1234.56 (소수점 '
                                                                                               '이하 최대 8자리).',
        'Amount must not exceed 1,000,000,000,000.': '금액은 1,000,000,000,000 이하여야 합니다.',
        'No valid rate data.': '유효한 환율 데이터가 없습니다.',
        'Invalid cache.': '저장된 데이터가 올바르지 않습니다.',
        'Invalid cache date.': '저장된 데이터의 날짜가 올바르지 않습니다.',
        'Invalid base currency.': '기준 통화가 올바르지 않습니다.',
        'Percentage fee must be between 0 and 100.': '비율 수수료는 0~100 사이여야 합니다.',
        'Currency not available in this rate snapshot.': '현재 환율 데이터에 해당 통화가 없습니다.',
        'Fees exceed the source amount.': '수수료가 기준 금액을 초과합니다.',
        'Invalid number.': '올바르지 않은 숫자입니다.',
        'Invalid currency.': '올바르지 않은 통화입니다.',
        'Invalid rate.': '올바르지 않은 환율입니다.',
        'Response is too large.': '응답 크기가 너무 큽니다.',
        'Rates loaded; the local cache could not be saved.': '환율을 불러왔지만 이 기기에 저장하지 못했습니다.',
        'Invalid period or currency.': '기간 또는 통화가 올바르지 않습니다.',
        'Negative or invalid amounts are not allowed.': '음수 또는 올바르지 않은 금액은 사용할 수 없습니다.',
        'Incorrect base currency.': '기준 통화가 일치하지 않습니다.',
        'Rate date is in the future.': '환율 기준일이 미래 날짜입니다.',
        'Invalid time series.': '시계열 데이터가 올바르지 않습니다.',
        'No rates available for the selected period.': '선택한 기간에 환율 데이터가 없습니다.',
        'Rate history is unavailable. Check your internet connection and try again.': '환율 내역을 사용할 수 없습니다. 인터넷 연결을 확인하고 '
                                                                                      '다시 시도하세요.',
        'Request failed: {error}': '요청 실패: {error}',
        'Offer {n}': '조건 {n}',
        '{amount} {base} → {target} · Rate date {date} · Sorted by payout. Individual exchange-rate markups are not included.': '{amount} '
                                                                                                                                '{base} '
                                                                                                                                '→ '
                                                                                                                                '{target} '
                                                                                                                                '· '
                                                                                                                                '환율 '
                                                                                                                                '기준일 '
                                                                                                                                '{date} '
                                                                                                                                '· '
                                                                                                                                '수령액순 '
                                                                                                                                '정렬. '
                                                                                                                                '개별 '
                                                                                                                                '환율 '
                                                                                                                                '가산율은 '
                                                                                                                                '포함하지 '
                                                                                                                                '않습니다.',
        '{source} · Rate date {date} · {count} currencies · Frankfurter / ECB': '{source} · 환율 기준일 {date} · {count}개 '
                                                                                '통화 · Frankfurter / ECB',
        '1 {base} = {rate} {target}\nFees: {fee} {base}\nBefore fees: {gross} {target}': '1 {base} = {rate} {target}\n'
                                                                                         '수수료: {fee} {base}\n'
                                                                                         '수수료 차감 전: {gross} {target}',
        '{pair} · {change} % over the available period · {count} data points · {source}': '{pair} · 제공 기간 변동률 {change} '
                                                                                          '% · {count}개 데이터 · {source}',
        'SCORE  {score}     /     BEST  {best}': '점수  {score}     /     최고  {best}',
        'help_body': '사용 방법\n'
                     '금액과 통화 쌍을 선택하세요. 소수점은 점 또는 쉼표를 사용하고 천 단위 구분 기호는 넣지 마세요. 비율 및 고정 수수료는 환산 전에 차감됩니다. 화면에 표시되는 금액만 '
                     '반올림됩니다.\n'
                     '\n'
                     '환율 출처\n'
                     '온라인: Frankfurter에서 제공하는 ECB 일일 기준 환율입니다. 주말과 공휴일에는 기준일이 이전 날짜일 수 있습니다. 오프라인: 원래 기준일과 함께 저장된 '
                     '환율입니다. 데모: 날짜 없는 예시이며 실제 환산에 사용하면 안 됩니다. 차트는 불러오거나 저장된 과거 데이터만 사용합니다.\n'
                     '\n'
                     '조작 방법\n'
                     'Enter로 환산 및 저장, Ctrl+R로 환율 새로고침, Ctrl+S로 통화 바꾸기, Ctrl+F로 검색합니다. F11은 전체 화면을 전환합니다. Esc는 전체 화면을 '
                     '종료하고 스네이크를 일시 정지합니다. 차트 위에 마우스를 올리면 값을 확인할 수 있습니다. 통화 쌍 변경 후 차트를 다시 불러오세요. 사이드바에서 애니메이션을 끌 수 '
                     '있습니다.\n'
                     '\n'
                     '개인정보\n'
                     '금액, 수수료, 내역은 이 컴퓨터에만 저장됩니다. 제공업체에는 통화 쌍, 기간 및 일반적인 연결 정보만 전송됩니다. 계정이나 사용 추적이 없습니다. CSV는 선택한 위치에만 '
                     '저장됩니다.\n'
                     '\n'
                     '언어\n'
                     '사이드바에서 언어를 선택하세요. 화면이 즉시 변경되고 설정이 저장됩니다. 언어 변경 시 스네이크가 일시 정지됩니다. 시스템 파일 창은 Windows 언어를 따를 수 '
                     '있습니다.\n'
                     '\n'
                     '로컬 데이터\n'
                     '{folder}\n'
                     '\n'
                     'QuantumFX {version}\n'
                     '원본 프로젝트: oneiric-hammer/QuantumFX-Currency-Intelligence-Platform. 원본 라이선스가 포함되어 있습니다.'},
 'sv': {'Language': 'Språk',
        'Language could not be saved.': 'Språkinställningen kunde inte sparas.',
        'Swap source and target currencies · Ctrl+S': 'Byt från- och tillvaluta · Ctrl+S',
        'Convert using the displayed rates and save the result to history · Enter': 'Omvandla med visade kurser och '
                                                                                    'spara i historiken · Enter',
        'Toggle fullscreen · F11. Press Escape to return to a window.': 'Växla helskärm · F11. Escape återgår till '
                                                                        'fönsterläge.',
        'Refresh daily reference rates in the background · Ctrl+R': 'Uppdatera dagliga referenskurser i bakgrunden · '
                                                                    'Ctrl+R',
        'Refresh rates': 'Uppdatera kurser',
        'Refresh': 'Uppdatera',
        'Your currency converter': 'Din valutaomvandlare',
        '1  Enter an amount': '1  Ange belopp',
        'For example 1234.56 · no thousands separators': 'Till exempel 1234,56 · utan tusentalsavgränsare',
        'Use a dot or comma as the decimal separator, e.g. 1234.56. Enter converts and saves.': 'Använd punkt eller '
                                                                                                'komma som '
                                                                                                'decimaltecken, t.ex. '
                                                                                                '1234,56. Enter '
                                                                                                'omvandlar och sparar.',
        '2  Choose currencies': '2  Välj valutor',
        'From': 'Från',
        'To': 'Till',
        'Add fees · optional': 'Lägg till avgifter · valfritt',
        'Percentage deducted from the source amount, from 0 to 100.': 'Procentandel som dras från ursprungsbeloppet, '
                                                                      'från 0 till 100.',
        'Fixed deduction in the source currency. For example, 2 means EUR 2 when converting from EUR.': 'Fast avdrag i '
                                                                                                        'frånvalutan. '
                                                                                                        'Till exempel '
                                                                                                        'betyder 2 ett '
                                                                                                        'avdrag på 2 '
                                                                                                        'EUR vid '
                                                                                                        'omvandling '
                                                                                                        'från EUR.',
        'Convert & save  ↗': 'Omvandla och spara  ↗',
        'Copy': 'Kopiera',
        'Rate trends': 'Kursutveckling',
        'Load history': 'Hämta kurshistorik',
        'Favorites · double-click to open': 'Favoriter · dubbelklicka för att öppna',
        'All available currencies': 'Alla tillgängliga valutor',
        "Rates per 1 unit of the converter's source currency. Double-click to select a target currency.": 'Kurser per '
                                                                                                          '1 enhet av '
                                                                                                          'frånvalutan. '
                                                                                                          'Dubbelklicka '
                                                                                                          'för att '
                                                                                                          'välja '
                                                                                                          'tillvaluta.',
        'Search by currency code, e.g. EUR or USD · Ctrl+F': 'Sök efter valutakod, t.ex. EUR eller USD · Ctrl+F',
        'Your recent conversions': 'Dina senaste omvandlingar',
        'Up to 1,000 entries are stored locally. CSV decimal values are not rounded.': 'Upp till 1 000 poster sparas '
                                                                                       'lokalt. Decimalvärden i CSV '
                                                                                       'avrundas inte.',
        'Understanding your numbers and data': 'Förstå dina siffror och data',
        'What is left after fees?': 'Vad återstår efter avgifterna?',
        'Compare three offers using the amount and currency pair from the converter.': 'Jämför tre erbjudanden med '
                                                                                       'beloppet och valutaparet från '
                                                                                       'omvandlaren.',
        'Assumes the same reference rate. Percentage and fixed fees are deducted in the source currency.': 'Samma '
                                                                                                           'referenskurs '
                                                                                                           'antas. '
                                                                                                           'Procentuella '
                                                                                                           'och fasta '
                                                                                                           'avgifter '
                                                                                                           'dras i '
                                                                                                           'frånvalutan.',
        'Loading rates in the background …': 'Hämtar kurser i bakgrunden …',
        'Recalculate': 'Beräkna igen',
        'Pair changed · reload the chart.': 'Valutaparet har ändrats · hämta diagrammet igen.',
        'Clear history': 'Rensa historik',
        'Permanently delete all saved conversions?': 'Radera alla sparade omvandlingar permanent?',
        'Loading historical reference rates …': 'Hämtar historiska referenskurser …',
        'This action failed. See the local log file for details.': 'Åtgärden misslyckades. Se den lokala loggfilen för '
                                                                   'detaljer.',
        'Ready to convert': 'Redo att omvandla',
        'Choose a currency pair and load its rate history.': 'Välj ett valutapar och hämta dess kurshistorik.',
        'Effects on': 'Effekter på',
        'Effects off': 'Effekter av',
        'Turn animations on or off. Your preference is saved.': 'Slå på eller av animationer. Inställningen sparas.',
        'Overview': 'Översikt',
        'Converter': 'Omvandlare',
        'Currencies': 'Valutor',
        'Fees': 'Avgifter',
        'History': 'Historik',
        'Snake': 'Snake',
        'Help': 'Hjälp',
        'Show optional percentage and fixed fees. Leave them at zero for no deductions.': 'Visa procentuella och fasta '
                                                                                          'avgifter. Lämna dem på noll '
                                                                                          'för inga avdrag.',
        'Offer': 'Erbjudande',
        'Fee %': 'Avgift %',
        'Fixed fee (source)': 'Fast avgift (från)',
        'Enter your own fees and compare offers.': 'Ange egna avgifter och jämför erbjudanden.',
        'Inputs or rates changed · compare offers again.': 'Inmatning eller kurser har ändrats · jämför igen.',
        'DEMO · Undated sample rates · Do not use for actual conversions': 'DEMO · Odaterade exempelkurser · Använd '
                                                                           'inte för verkliga omvandlingar',
        'Retrieved online': 'Hämtat online',
        'Offline / saved rates': 'Offline / sparade kurser',
        'Result copied.': 'Resultatet kopierat.',
        'This pair is not available in the current rate snapshot.': 'Valutaparet saknas i den aktuella '
                                                                    'kursinformationen.',
        'Export CSV': 'Exportera CSV',
        'Load a rate history first.': 'Hämta kurshistorik först.',
        'Close': 'Stäng',
        '★ Save pair': '★ Spara valutapar',
        'Export chart CSV': 'Exportera diagram som CSV',
        'Remove selected pair': 'Ta bort valt valutapar',
        'Hide fees': 'Dölj avgifter',
        'Window  Esc': 'Fönster  Esc',
        'Fullscreen  F11': 'Helskärm  F11',
        'Could not save display preferences.': 'Visningsinställningarna kunde inte sparas.',
        'Reset': 'Återställ',
        'Export rates as CSV': 'Exportera kurser som CSV',
        'Currency': 'Valuta',
        'Rate': 'Kurs',
        'Base': 'Bas',
        'Rate date / source': 'Kursdatum / källa',
        'Time': 'Tid',
        'Amount': 'Belopp',
        'Currency pair': 'Valutapar',
        'Result': 'Resultat',
        'Fee (source)': 'Avgift (från)',
        'Rate date': 'Kursdatum',
        'Source': 'Källa',
        'Compare offers': 'Jämför erbjudanden',
        'Fees (source)': 'Avgifter (från)',
        'Payout (target)': 'Utbetalning (till)',
        'Difference from best offer': 'Skillnad mot bästa erbjudandet',
        'Check your input': 'Kontrollera inmatningen',
        'Could not save favorites.': 'Favoriterna kunde inte sparas.',
        'Export': 'Exportera',
        'CSV file saved.': 'CSV-filen sparad.',
        'Selection changed · reload the chart.': 'Valet har ändrats · hämta diagrammet igen.',
        'Load rate history to see the trend': 'Hämta kurshistorik för att se utvecklingen',
        'Frankfurter / ECB · Daily reference rates · Fees are your own estimates.': 'Frankfurter / ECB · Dagliga '
                                                                                    'referenskurser · Avgifterna är '
                                                                                    'dina uppskattningar.',
        'Percent %': 'Procent %',
        'Fixed fee': 'Fast avgift',
        'Period (days)': 'Period (dagar)',
        'Fees active · edit': 'Avgifter aktiva · ändra',
        'Find currency': 'Sök valuta',
        'Conversion saved locally.': 'Omvandlingen sparad lokalt.',
        'Converted, but history could not be saved.': 'Omvandlat, men historiken kunde inte sparas.',
        'Export failed': 'Exporten misslyckades',
        'Deletion failed': 'Raderingen misslyckades',
        ' DEMO rates used.': ' DEMO-kurser användes.',
        'Cache': 'Cache',
        'Reference rates': 'Referenskurser',
        'Pause / Resume': 'Pausa / Fortsätt',
        'Normal': 'Normal',
        'Arrow keys or WASD · Space to pause · Enter to restart': 'Piltangenter eller WASD · Mellanslag pausar · Enter '
                                                                  'startar om',
        'YOU WIN!': 'DU VANN!',
        'New game': 'Nytt spel',
        'Relaxed': 'Lugnt',
        'Fast': 'Snabbt',
        'GAME OVER': 'SPELET SLUT',
        'New game / Space': 'Nytt spel / Mellanslag',
        'A little break. A longer snake.': 'En liten paus. En längre orm.',
        'High score is kept for this session; saving failed.': 'Rekordet behålls under denna session; det gick inte '
                                                               'att spara.',
        'PAUSE': 'PAUS',
        'SNAKE ARCADE': 'SNAKE ARCADE',
        'Your money. In any currency.': 'Dina pengar. I alla valutor.',
        'Enter an amount. Choose currencies. Get clarity.': 'Ange belopp. Välj valutor. Få klarhet.',
        'Your result · after fees': 'Ditt resultat · efter avgifter',
        'Enter a number without thousands separators, e.g. 1234.56 (up to 8 decimal places).': 'Ange ett tal utan '
                                                                                               'tusentalsavgränsare, '
                                                                                               't.ex. 1234,56 (högst 8 '
                                                                                               'decimaler).',
        'Amount must not exceed 1,000,000,000,000.': 'Beloppet får inte överstiga 1 000 000 000 000.',
        'No valid rate data.': 'Inga giltiga kursdata.',
        'Invalid cache.': 'Ogiltig cache.',
        'Invalid cache date.': 'Ogiltigt cachedatum.',
        'Invalid base currency.': 'Ogiltig basvaluta.',
        'Percentage fee must be between 0 and 100.': 'Procentavgiften måste vara mellan 0 och 100.',
        'Currency not available in this rate snapshot.': 'Valutan saknas i denna kursinformation.',
        'Fees exceed the source amount.': 'Avgifterna överstiger ursprungsbeloppet.',
        'Invalid number.': 'Ogiltigt tal.',
        'Invalid currency.': 'Ogiltig valuta.',
        'Invalid rate.': 'Ogiltig kurs.',
        'Response is too large.': 'Svaret är för stort.',
        'Rates loaded; the local cache could not be saved.': 'Kurserna har hämtats men kunde inte sparas lokalt.',
        'Invalid period or currency.': 'Ogiltig period eller valuta.',
        'Negative or invalid amounts are not allowed.': 'Negativa eller ogiltiga belopp är inte tillåtna.',
        'Incorrect base currency.': 'Fel basvaluta.',
        'Rate date is in the future.': 'Kursdatumet ligger i framtiden.',
        'Invalid time series.': 'Ogiltig tidsserie.',
        'No rates available for the selected period.': 'Inga kurser för den valda perioden.',
        'Rate history is unavailable. Check your internet connection and try again.': 'Kurshistoriken är inte '
                                                                                      'tillgänglig. Kontrollera '
                                                                                      'internetanslutningen och försök '
                                                                                      'igen.',
        'Request failed: {error}': 'Begäran misslyckades: {error}',
        'Offer {n}': 'Erbjudande {n}',
        '{amount} {base} → {target} · Rate date {date} · Sorted by payout. Individual exchange-rate markups are not included.': '{amount} '
                                                                                                                                '{base} '
                                                                                                                                '→ '
                                                                                                                                '{target} '
                                                                                                                                '· '
                                                                                                                                'Kursdatum '
                                                                                                                                '{date} '
                                                                                                                                '· '
                                                                                                                                'Sorterat '
                                                                                                                                'efter '
                                                                                                                                'utbetalning. '
                                                                                                                                'Individuella '
                                                                                                                                'valutapåslag '
                                                                                                                                'ingår '
                                                                                                                                'inte.',
        '{source} · Rate date {date} · {count} currencies · Frankfurter / ECB': '{source} · Kursdatum {date} · {count} '
                                                                                'valutor · Frankfurter / ECB',
        '1 {base} = {rate} {target}\nFees: {fee} {base}\nBefore fees: {gross} {target}': '1 {base} = {rate} {target}\n'
                                                                                         'Avgifter: {fee} {base}\n'
                                                                                         'Före avgifter: {gross} '
                                                                                         '{target}',
        '{pair} · {change} % over the available period · {count} data points · {source}': '{pair} · {change} % under '
                                                                                          'tillgänglig period · '
                                                                                          '{count} datapunkter · '
                                                                                          '{source}',
        'SCORE  {score}     /     BEST  {best}': 'POÄNG  {score}     /     REKORD  {best}',
        'help_body': 'SÅ FUNGERAR DET\n'
                     'Välj belopp och valutapar. Använd punkt eller komma för decimaler, utan tusentalsavgränsare. '
                     'Procentuella och fasta avgifter dras före omvandlingen. Endast visade belopp avrundas.\n'
                     '\n'
                     'KURSKÄLLOR\n'
                     'Online: dagliga ECB-referenskurser från Frankfurter. Datum kan vara äldre på helger och '
                     'helgdagar. Offline: sparade kurser med ursprungligt datum. DEMO: odaterade exempel, inte för '
                     'verkliga omvandlingar. Diagram använder endast hämtade eller sparade historiska data.\n'
                     '\n'
                     'KONTROLLER\n'
                     'Enter omvandlar och sparar. Ctrl+R uppdaterar kurser. Ctrl+S byter valutor. Ctrl+F öppnar '
                     'sökningen. F11 växlar helskärm. Escape lämnar helskärm och pausar Snake. Håll muspekaren över '
                     'diagrammet för att se värden. Hämta diagrammet igen efter byte av valutapar. Animationer kan '
                     'stängas av i sidofältet.\n'
                     '\n'
                     'INTEGRITET\n'
                     'Belopp, avgifter och historik stannar på datorn. Leverantören får valutapar, datumintervall och '
                     'normal anslutningsinformation. Inget konto eller telemetri. CSV-filer sparas bara där du '
                     'väljer.\n'
                     '\n'
                     'SPRÅK\n'
                     'Välj språk i sidofältet. Gränssnittet uppdateras direkt och inställningen sparas. Snake pausas '
                     'vid språkbyte. Systemets fildialoger kan följa Windows språk.\n'
                     '\n'
                     'LOKALA DATA\n'
                     '{folder}\n'
                     '\n'
                     'QuantumFX {version}\n'
                     'Originalprojekt: oneiric-hammer/QuantumFX-Currency-Intelligence-Platform. Originallicensen '
                     'medföljer.'}}

class LocalizedText(str):
    """Keep the English source for stable icon selection across languages."""
    def __new__(cls, value, source, language="en"):
        result = super().__new__(cls, value)
        result.language = language
        result.source = source
        return result


class Translator:
    def __init__(self, language="en"):
        self.language = language if isinstance(language, str) and language in LANGUAGES else "en"

    def __call__(self, message, **values):
        source = getattr(message, "source", str(message))
        translated = CATALOGS[self.language].get(source, source)
        if values:
            translated = translated.format(**values)
        return LocalizedText(translated, source, self.language)

    def error(self, error):
        message = str(error)
        if message.startswith("Request failed: "):
            return self("Request failed: {error}", error=self.error(message[len("Request failed: "):]))
        return self(message)

    def amount(self, formatted):
        if self.language == "de":
            return formatted.replace(",", "_").replace(".", ",").replace("_", ".")
        if self.language == "sv":
            return formatted.replace(",", " ").replace(".", ",")
        return formatted


def font_family(language):
    return "Malgun Gothic" if language == "ko" else "Segoe UI"
