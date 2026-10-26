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

#### Bug: Naive Fehlerfortpflanzung

Entsteht, weil alle Fehleranteile als unabhängig betrachtet werden. **Beispiel**:

- $f(x) = x - x$ ist offensichtlich $0\pm 0$. Die naive implementation ergibt: $0 \pm \Delta f$ mit $\Delta f = \sqrt{(1\Delta x)^2 + (-1\Delta x)^2} = \sqrt 2 \Delta x$.
- $f(x) = x + x$ ergibt $\Delta f = \sqrt 2 \Delta x$ anstatt dem richtigen Fehler $\Delta f = 2\Delta x$.

#### Fix

- Jede **Messung** kennt die ihre _atomaren_ Abhängigkeiten $x_i$. (Solche, die nicht aus einer Formel aus Anderen entstehen.)
- Pro $x_i$ kennt die **Messung** die partiellen Ableitungen ihrer _direkten_ Abhängigkeiten $g_k$ nach allen _atomaren_ Abhängigkeiten, ausgewertet an den Werten der _atomaren_ Abhängigkeiten $a_{ik}$. ($a_{ik} = \frac{\partial g_k}{\partial x_i} |_{x_1,\dots,x_N}$)
- Je nach Verknüpfung, werden dann diese Beiträge addiert **bevor** sie quadriert und weiter verrechnet werden.
- Für die geplanten Verknüpfungen ist $k\in\{1,2\}$, das macht die berechnung leichter.

# LaTeX Helper

## Idee

- Automatische Generation von LaTeX/ Typst Boilerplate und persönlicher Templates.
- Direkte Einbindung von Formatierten Auswertungen, aus 1.
- Soll als Bibliothek in Notebooks verwendet werden können.
- In Code Blöcken wird Skripting und Inhalt.

## Umsetzung

To do.
