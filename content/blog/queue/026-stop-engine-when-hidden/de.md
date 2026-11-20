---
title: Den Motor anhalten, wenn niemand hinsieht
description: Wenn der Bildschirm verdeckt ist oder die App in den Hintergrund geht, hält die Spiel-Engine an. Hier ist die Regel, die wir beim Umzug auf ein gemeinsames Engine-Kit festgelegt haben, und was wir noch nicht gemessen haben.
slug: stop-engine-when-hidden
lang: de
translation_of: en
date: 2026-11-23
---

Die Karten- und Schlachtszenen von Iltonggi sind bewegte Bilder. Soldaten marschieren, Banner wehen, und Gefechte laufen Bild für Bild ab. Doch wenn ein Spieler einen Anruf annimmt oder zu einer anderen App wechselt, gibt es keinen Grund, weiter Bilder zu zeichnen, die niemand sehen kann. Dieser Beitrag hält die Regel fest, die wir heute beim Umzug der Spiel-Engine auf ein gemeinsames Kit festgelegt haben. Das Spiel ist noch in Entwicklung.

## Anhalten, wenn nichts zu sehen ist

Wenn der Bildschirm verdeckt wird oder die App in den Hintergrund geht, hält die Engine an. Eine Szene zu zeichnen, die niemand sehen kann, verbraucht nur Akku. Kehrt der Spieler zurück, wird dort weitergezeichnet, wo es aufgehört hat. Die Karte, die ein Spieler verlassen hat, muss dieselbe bleiben, deshalb lassen wir die Spielzeit nicht heimlich weiterlaufen, während die App verborgen ist.

## Eine Stelle entscheidet, wann angehalten wird

Früher hatte jede Szene einen eigenen Code zum Anhalten. Karte, Schlachtbühne und Weltübersicht prüften jeweils selbst, ob sie verdeckt waren, und jede musste einzeln korrigiert werden. Diese Aufgabe liegt jetzt bei einer gemeinsamen Hülle. Die Szenen fragen nicht mehr, ob sie sichtbar sind. Sie folgen dem Zustand, den die Hülle setzt.

## Die Gefechtsanimation läuft weiter

Wenn zwei Heere auf der Karte aufeinandertreffen, bewegt sich die Animation nur, während die Engine läuft. Während eines Gefechts wird die angehaltene Engine deshalb für diesen Moment eingeschaltet und danach wieder angehalten. Tempo und Reihenfolge der Animation haben sich nicht geändert. Außerdem haben wir eine Lücke geschlossen: Endet ein Gefecht, während der Bildschirm verdeckt ist, startet die Engine beim Zurückkehren nicht mehr von selbst neu.

## Was wir noch nicht gemessen haben

Wie viel Akku das spart, haben wir noch nicht gemessen. Einiges lässt sich nur auf echten Geräten prüfen: die App in den Hintergrund schicken und zurückholen, zwischen Karte und Weltansicht wechseln, die Obergrenze von 30 Bildern pro Sekunde und wie lange das Zeichnen auf der GPU dauert. Bis dahin nennt dieser Beitrag keine Akkuwerte.

// Ein Bild, das niemand sieht, ist das billigste, das man auslassen kann.
