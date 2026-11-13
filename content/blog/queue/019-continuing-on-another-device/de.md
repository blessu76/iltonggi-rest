---
title: Auf einem anderen Gerät weiterspielen
description: Wie Iltonggi das Weiterspielen zwischen Apple-Geräten ermöglicht und welche Regeln wir wählten, wenn zwei Geräte uneins sind.
date: 2026-11-16
slug: continuing-on-another-device
lang: de
translation_of: ko
---

Die ursprüngliche Bitte war einfach: Wer auf einem Apple-Gerät spielt, soll mit demselben Konto auf einem anderen weitermachen können. Das klingt klein, aber das Schwierige ist nicht, einen Spielstand zu kopieren. Es ist zu entscheiden, was passiert, wenn zwei Geräte verschiedene Versionen haben. Diese Notiz beschreibt die Regeln, auf die wir uns geeinigt haben. Das Spiel ist noch in Entwicklung.

## Die Wahrheit liegt auf dem Gerät

Jedes Gerät behält seine eigene Datei als den eigentlichen Spielstand. iCloud hält nur eine Kopie, nicht das Original. Ist iCloud ausgeschaltet, sind Sie abgemeldet oder nutzen Sie Android, bleibt das Spiel einfach auf diesem einen Gerät, ohne Fehlermeldung. Der Hauptspielstand, die drei Speicherplätze und die Einstellungen nehmen teil.

## Ein Dreiervergleich

Um zu entscheiden, was zu tun ist, merkt sich jedes Gerät einen Fingerabdruck der letzten Version, die mit der Cloud übereinstimmte. Dann vergleicht es:

- Nur dieses Gerät hat sich geändert: hochladen.
- Nur die Cloud hat sich geändert: herunterladen.
- Beide haben sich geändert: nach Regel auswählen.

## Wenn beide sich geändert haben

Die Reihenfolge, die wir gewählt haben:

1. Ein nicht leerer Spielstand schlägt einen leeren.
2. Unterscheiden sich die Speicherzeiten um mehr als zwei Minuten, gewinnt der spätere.
3. Liegen sie innerhalb von zwei Minuten und ist es dasselbe Spiel, gewinnt der mit mehr Zügen.
4. Andernfalls der von diesem Gerät.

Darüber haben wir gestritten. „Der weiteste Fortschritt gewinnt“ wäre leichter zu erklären gewesen, aber wir hielten „der zuletzt gespeicherte“ für näher an dem, was Spieler meinen. Die unterlegene Kopie wird nicht gelöscht, sondern als Konfliktkopie beiseitegelegt.

## Zusammenführen statt wählen

Manches darf nie einem Münzwurf zum Opfer fallen. Welche Akte Sie abgeschlossen, welche Aktgeschichten Sie gesehen haben und was Sie besitzen, wird als Vereinigung zusammengeführt, statt von einer Seite übernommen zu werden.

## Ein Größenlimit

Ein einzelner Text mit mehr als 200.000 Zeichen wird nicht hochgeladen und bleibt auf dem Gerät. Tests decken diese Grenze ab.

## Änderungen beim Spielen bemerken

Anfangs las das Spiel die Cloud nur neu, wenn Sie zur App zurückkehrten. Mit Build 85 bemerkt es auch eine Änderung von einem anderen Gerät, während es vor Ihnen im Vordergrund ist, und die Einstellungen zeigen, ob die iCloud-Synchronisierung an ist.

## Noch nicht überprüft

All das ist auf einem Computer getestet. Wir haben noch nicht gesehen, wie zwei echte Geräte mit einem Konto ein Spiel hin und her reichen, dieser Teil ist also unbestätigt. Bilder der Generäle und Ihr Auftragsfortschritt bleiben absichtlich auf jedem Gerät.

// Synchronisieren ist leicht. Zu entscheiden, wer recht hat, ist die Arbeit.
