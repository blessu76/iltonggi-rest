---
title: Drei Schwierigkeitsgrade, von Zahlen gehalten
description: Wie wir Tausende Schlachten simulieren, damit Leicht, Normal und Schwer in ihren Siegquoten-Bereichen bleiben, und warum der Bot Schwer schwerer aussehen lässt.
date: 2026-11-18
copy_review: iris 2026-11-14
slug: three-difficulties-in-numbers
lang: de
translation_of: ko
---

Wer Leicht wählt, erwartet meistens zu gewinnen. Wer Schwer wählt, erwartet bedrängt zu werden. Das klingt selbstverständlich, gerät aber unbemerkt aus dem Lot, sobald jemand eine Regel oder einen General ändert. Deshalb halten wir jeden Schwierigkeitsgrad mit Tests in einem Bereich. Das Spiel ist noch in Entwicklung, und diese Notiz beschreibt, wie das funktioniert.

## Was schon abgesichert war

Zuvor prüften unsere Tests, wie stark eine Karte oder ein berühmter General die Siegquote erhöht und ob Leicht jedem Königreich zwischen 60 und 95 Prozent gibt. Nichts deckte die absolute Siegquote von Normal und Schwer ab, und auch nicht die einfache Tatsache, dass Leicht leichter sein muss als Normal und Normal leichter als Schwer.

## Wie wir messen

Ein Bot spielt jedes Königreich 200-mal mit einer festen Menge von Zufallswerten und denselben Regeln wie beim Start der App. Die Ergebnisse sind jedes Mal gleich, und der gesamte Lauf dauert einige Sekunden. Die Durchschnitte über vier Königreiche, gemessen am 5. November:

| Karte | Leicht | Normal | Schwer |
|---|---|---|---|
| Akt 1 | 79,5 % | 23,8 % | 6,0 % |
| Historischer Akt 1 | 77,5 % | 30,5 % | 7,9 % |
| Han-Fluss | 72,3 % | 45,4 % | 4,4 % |

Jeder Test erlaubt etwa 10 Punkte Abstand nach beiden Seiten. Schiebt eine Änderung ein Ergebnis aus seinem Bereich, schlägt der Test fehl.

## Ein paar zusätzliche Regeln

- Zwischen den Schwierigkeitsgraden muss ein Abstand von mehr als 15 Punkten liegen.
- Bei Schwer darf kein Königreich über 25 Prozent liegen.
- Bei Leicht darf kein Königreich unter 55 Prozent fallen.
- Mit demselben Startwert müssen sich die Ergebnisse exakt wiederholen.

## Warum Schwer so niedrig wirkt

Der Bot nutzt weder Diplomatie noch Spione und spielt daher schlechter als ein Mensch. Die niedrigen Werte für Normal und Schwer sind die des Bots, kein Versprechen für menschliche Spieler. Dass die Prüfung wirklich greift, haben wir bestätigt, indem wir einen Bereich absichtlich verstellten und den Test scheitern sahen.

## Was sie nicht sagen kann

Eine Siegquote sagt nicht, ob sich ein Spiel fair oder unterhaltsam anfühlte. Diese Antworten kommen weiterhin vom Spielen von Hand. Verschieben wir einmal absichtlich einen Bereich, ändern wir die Tabelle am Anfang der Testdatei und die Notizen gemeinsam.

// Zahlen können einen Schwierigkeitsgrad ehrlich halten. Unterhaltsam machen sie ihn nicht.
