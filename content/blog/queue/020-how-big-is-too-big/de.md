---
title: Wie groß ist zu groß für ein Handyspiel?
description: Warum wir für Bilder, Klänge und Schriften von Iltonggi ein Größenbudget festgelegt haben und welche Prüfung den Build bei Überschreitung scheitern lässt.
date: 2026-11-17
slug: how-big-is-too-big
lang: de
translation_of: ko
---

Ein Spiel, dessen Download lange dauert oder das seinen ersten Bildschirm spät zeigt, verliert Menschen, bevor sie spielen. Iltonggi enthält viel: Schriften im alten Stil, Gemälde, Musik und Soundeffekte sowie Texte in elf Sprachen. Wenn niemand aufpasst, wächst es nur. Also haben wir ein Budget festgelegt und den Computer darüber wachen lassen. Das Spiel ist noch in Entwicklung.

## Was wir messen

Wir zählen nur die Dateien, die die App tatsächlich mitliefert, nicht alles im Projekt. Am 5. November lauteten die Zahlen:

| Posten | Gemessen | Grenze |
|---|---|---|
| Alle mitgelieferten Dateien (74) | 9,83 MiB | 12.000.000 Byte |
| Größte Einzeldatei (die Serifenschrift, komprimiert) | 1,29 MB | 1,5 MB |
| Audio | 4,27 MB | 5 MB |
| Fotos (23) | 3,55 MB | 4,2 MB |
| Vor dem ersten Bild gelesen | 1,48 MB | 1,7 MB |

Jede Grenze lässt etwa 15 bis 18 Prozent Spielraum. Außerdem verbieten wir Formate, die nie ausgeliefert werden sollten, etwa unkomprimiertes Audio und Bilddateien mit Ebenen.

## Eine Prüfung, kein Versprechen

Eine Regel, die nur in einem Dokument steht, gerät in Vergessenheit. Deshalb läuft die Größenprüfung im selben Tor wie Formatierung, Analyse und Tests. Wird eine Grenze überschritten, schlägt der Build fehl. Eine Grenze anzuheben ist erlaubt, aber nur absichtlich: Die Zahl im Skript und in der Tabelle müssen zusammen geändert werden.

## Die Schrift, die draußen blieb

Die Serifenschrift ist als Originaldatei 3,18 MB groß, was für ein Handy viel ist. Wir liefern sie komprimiert mit 1,29 MB aus, und das Original bleibt nur im Repository. Fügt es jemand versehentlich der App hinzu, fangen die Regel für verbotene Formate und die Gesamtgrenze es ab.

## Startzeit

Auf einem Mac dauert das Entpacken der Schrift etwa 6 Millisekunden und das Laden des Eröffnungsbilds etwa 14. Ein Zeitlimit haben wir nicht gesetzt, denn Zahlen von einem Mac sagen wenig über ein echtes Handy beim Kaltstart.

## Noch unbekannt

Die endgültige Größe des installierbaren Pakets kennen wir noch nicht, weil Kompression, Code und Engine erst beim Build hinzukommen. Wir wollen diese Zahl neben dieser Tabelle festhalten, sobald wir sie haben.

// Ein Budget wirkt, weil es Nein sagen kann.
