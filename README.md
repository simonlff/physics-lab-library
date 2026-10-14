# Auswertung

## Idee

- Bibliothek, die große Teile der Datenauswertung von Laborversuchen (halb)-automatisiert.
- Stark vereinfachte Datendarstellung, sowohl als Tabelle als auch als Plot.

## Architektur

### Datenklassen

- **Messung:** Messreihen, die den "gleichen" Wert `n`-Mal messen `(n,)`.
- **Variation:** Reihen, die `m` verschiedenen Werte, z.B. in Abhängigkeit einer anderen Größe, messen `(n,m)`.
- **Versuchsblock:** `k` zusammengehöreige Variationen `(n,m,k)`.

<!-- - Falls benötigt, könnten auch mehrdiemnsionale Messungen und Kontrollvariablen nützlich sein. -->

### Funktionen

- Mittelwert, Standardabweichung, SEM berechen.
- Elementweise anwendung von Funktionen auf Datenobjekte. Automatische Fehlerfortpflanzung.
- Kombination von _mehreren_ Datenobjekten durch Funktionen zu einem neuen Datenobjekt (insbesondere von einer `Messung` auf ihren Mittelwert). Automatische Fehlerfortpflanzung.
- Zusätzliche definition von weiteren Fehlern an beliebigen Stellen der Rechnung.
- Darstellung als Plot und Ausgabe von ausgefülltem LaTeX Snippets.

# LaTeX Helper

## Idee

- Automatische Generation von LaTeX/ Typst Boilerplate und persönlicher Templates.
- Direkte Einbindung von Formatierten Auswertungen, aus 1.
- Soll als Bibliothek in Notebooks verwendet werden können.
- In Code Blöcken wird Skripting und Inhalt.

## Umsetzung

To do.
