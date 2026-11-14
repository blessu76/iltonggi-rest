---
title: Ein Spielstand, der Beschädigung übersteht
description: Wie Iltonggi Ihren Fortschritt schützt, wenn eine Datei mitten im Schreiben abbricht, und wie wir das testeten, ohne ein echtes Handy zu beschädigen.
date: 2026-11-15
copy_review: iris 2026-11-14
slug: a-save-that-survives
lang: de
translation_of: ko
---

Nichts verdirbt ein langes Spiel schneller, als es zu öffnen und den Fortschritt verschwunden zu finden. Der Akku eines Handys kann leer werden, oder die App wird mitten im Schreiben einer Datei geschlossen, und dann bleibt eine halbe Datei zurück. Iltonggi sollte das überstehen. Das Spiel ist noch in Entwicklung, und diese Notiz beschreibt, wie weit der Schutz heute reicht.

## Das meiste gab es schon

Als wir uns daransetzten, ein Sicherheitsnetz einzubauen, stellten wir fest, dass der Hauptspielstand schon eines hatte. Wir hatten es vergessen. Es arbeitet in vier Schritten.

1. Der neue Spielstand wird zuerst in eine temporäre Datei geschrieben und dann ausgetauscht. Bricht das Schreiben ab, bleibt der alte Spielstand unberührt.
2. Von dem vorherigen Spielstand wird eine Sicherungsgeneration aufbewahrt.
3. Beim Laden wird geprüft, ob sich die Datei fehlerfrei lesen lässt.
4. Ist sie beschädigt, wird die Sicherung wiederhergestellt. Ist auch die Sicherung beschädigt, beginnt ein neues Spiel, statt abzustürzen.

Die Lücke war, dass nur der Hauptspielstand das hatte. Die drei Speicherplätze, die Einstellungen, die abgeschlossenen Akte, Aufträge, der Laden, besessene Gegenstände sowie Spitzname und Rekorde wurden einfach so geschrieben.

## Ausweiten, aber nicht auf alles

Wir haben die Sicherung für jede Datei eingeschaltet, deren Verlust wehtäte. Für Protokolle, Tipps, Wetter und Verlauf blieb sie aus, weil ein Verlust dort nichts Wichtiges kostet. Eine kurze Liste bedeutet weniger zusätzliche Dateien auf dem Handy und weniger, worüber man nachdenken muss. Dateinamen und Inhalte blieben gleich, bestehende Spielstände funktionieren also weiter. Neu ist nur die Sicherungskopie.

## Testen, ohne ein Handy zu zerstören

Man kann Spieler nicht bitten, mitten im Schreiben den Strom zu kappen. Deshalb haben wir vier Situationen in Tests nachgestellt, für jede Datei, die jetzt eine Sicherung hat:

- Beschädigter Text im Spielstand: Die Sicherung wird wiederhergestellt.
- Leere Datei: Die Sicherung wird wiederhergestellt.
- Beschädigt und ohne Sicherung: Das Spiel startet neu, ohne abzustürzen.
- Nur eine halb geschriebene temporäre Datei: Der vorherige Spielstand ist noch da.

## Was wir nicht überprüft haben

Das sind Tests auf einem Computer. Wir haben noch nicht auf einem echten Gerät absichtlich eine Datei beschädigt und die Wiederherstellung beobachtet, dieser Teil ist also unbestätigt. Wird etwas anderes als der Hauptspielstand wiederhergestellt, sieht der Spieler außerdem keine Meldung. Es kommt leise zurück. Für Einstellungen halten wir das für richtig, aber wir können es noch einmal überdenken.

// Ein guter Spielstand fällt nur dann auf, wenn er uns rettet.
