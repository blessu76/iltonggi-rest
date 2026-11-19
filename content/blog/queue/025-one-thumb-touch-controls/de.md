---
title: Ein Daumen, ein Gebiet: Touch-Steuerung für ein Landkartenspiel entwerfen
description: Ein Spiel um Gebietseroberung muss auf einem kleinen Bildschirm mit einem einzigen Daumen funktionieren. So denken wir über Tippen, Ziehen und die Fehler nach, die wir vermeiden wollen.
slug: one-thumb-touch-controls
lang: de
translation_of: en
date: 2026-11-22
copy_review: iris 2026-11-19
---

Iltonggi ist ein Landkartenspiel, und ein Landkartenspiel auf dem Handy verlangt viel von einem einzigen Daumen. Man muss ein Gebiet auswählen, seine Truppen sehen, ein Heer bewegen und das Ergebnis lesen, ohne genau das Gebiet zu verdecken, das man antippen will. Dieser Beitrag beschreibt, wie wir über Touch-Eingaben nachdenken. Das Spiel ist noch in Entwicklung. Lesen Sie diese Regeln daher als das, was wir gerade testen, nicht als fertige Anleitung.

## Tippen und Ziehen sind verschiedene Dinge

Der häufigste Fehler bei einem Landkartenspiel besteht darin, jede Berührung wie einen Klick zu behandeln. Ein Finger, der sich ein wenig bewegt, während die Karte darunter gleitet, ist keine Auswahl. Deshalb trennen wir zwei Absichten: ein kurzes Tippen, das auswählt, und eine längere Bewegung, die die Karte verschiebt. Bewegt sich der Finger vor dem Loslassen über eine kleine Strecke, gehört die Berührung zur Karte, und es wird kein Gebiet gewählt.

Das Prinzip ist wichtiger als der genaue Abstand. Ein Spieler sollte beim Scrollen über einen dicht besetzten Teil der Karte nie versehentlich ein Gebiet auswählen.

## Gebiete sind auf dem Handy klein

Manche Gebiete sind schmal, und ein Daumen ist breit. Wenn in der Nähe kein anderes Gebiet liegt, lassen wir den Tippbereich eines Gebiets etwas über den gezeichneten Rand hinausreichen. Wir lassen ihn nie so groß werden, dass er einen Tipp stiehlt, der für einen Nachbarn bestimmt war. Liegen zwei Gebiete nah beieinander, soll die Wahl davon abhängen, wo die Berührung landet, und nicht davon, welches Gebiet zuletzt gezeichnet wurde.

## Teure Züge bestätigen

Angriffe und Truppenbewegungen verändern den Spielzustand. Deshalb sollen sie leichter aus Versehen zu vermeiden sein als das bloße Ansehen eines Gebiets. Ein Tipp zeigt, was passieren würde, und eine zweite, bewusste Handlung führt es aus. Das kostet etwas Tempo, und wer die Karte gut kennt, empfindet es vielleicht als langsamer. Wir nehmen diesen Tausch in Kauf, denn ein falsch geschicktes Heer ärgert mehr als ein zusätzlicher Tipp.

## Kurze Sitzungen, oft unterbrochen

Menschen spielen Iltonggi in kurzen Sitzungen: im Bus, in der Schlange, ein paar Minuten vor dem Schlafen. Eine Unterbrechung kann jederzeit kommen, etwa durch einen Anruf oder einen Wechsel zu einer anderen App. Die Steuerung darf deshalb nicht von einer Geste abhängen, die lange andauert. Ein halb ausgeführtes Ziehen soll ohne Ergebnis enden, und die Karte soll dort bleiben, wo der Spieler sie verlassen hat.

## Was wir noch prüfen müssen

Daumengrößen unterscheiden sich, Bildschirme ebenso. Unsere Annahmen stammen vor allem von den Geräten, die wir selbst besitzen. Wir planen, die Tippbereiche auf mehr Bildschirmen zu testen und zu beobachten, wo Spieler sich vertippen. Das haben wir noch nicht im großen Maßstab gemessen, deshalb nennt dieser Beitrag keine Zahlen.

// Der sicherste Tipp ist der, den man zurücknehmen kann.
