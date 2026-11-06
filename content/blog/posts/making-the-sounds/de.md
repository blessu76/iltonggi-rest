---
title: Von Kriegstrommeln bis zur Gayageum – auch die Klänge haben wir selbst gemacht
description: Wie Iltonggis 15 Effekte und 4 Musikstücke ohne fremdes Audio per Skript synthetisiert wurden und warum wir einige neu gemacht haben.
slug: making-the-sounds
lang: de
translation_of: ko
date: 2026-11-06
published: 2026-11-06T12:00:00+09:00
---

Der Klang ist der Teil von Iltonggi, an dem wir am längsten weiterarbeiten. Ein Bild sieht man sofort, aber wenn ein Klang falsch ist, lässt sich schwer sagen, was an ihm falsch ist. Dieser Beitrag hält fest, wie die Klänge entstanden sind und warum wir einige einmal neu gemacht haben.

## Ohne fremdes Audio

Im Spiel stecken jetzt 19 Klänge: 15 Effekte und 4 Musikstücke. Alle sind per Skript von Grund auf synthetisiert. Wir haben weder heruntergeladene Samples noch gekauftes Audio verwendet. Lässt man dasselbe Skript noch einmal laufen, entsteht deshalb derselbe Klang noch einmal. Dass wir die Herkunft jedes Klangs erklären können, ist der wichtigste Grund für diesen Weg.

## Trommeln, Siegel, Flagge und Tusche

Für Kampf und Marsch gibt es vier Trommelklänge. Jeder beginnt als Sinuswelle, deren Tonhöhe absinkt, mit einem kurzen Rauschstoß darüber, der den Schlag aufs Fell andeutet. Die Tonhöhen liegen auseinander, ungefähr bei 55, 59, 65 und 85 Hz.

Der Siegelklang beim Einnehmen von Land ist ein tiefer Ton, der von 94 Hz auf 39 Hz fällt. Doch der kleine Lautsprecher eines Handys bringt so tiefe Töne kaum hervor. Deshalb haben wir einige Obertöne beigemischt, damit der Schlag auch dann noch zu spüren ist, wenn der tiefste Teil wegfällt.

Der Flaggenklang, der beim Sieg und beim Zugwechsel erklingt, lässt Rauschen nur durch ein schmales Band und lässt es schnell zittern, wie Stoff im Wind. Er dauert 1,4 Sekunden. Der Tuscheklang, der in der Diplomatie zu hören ist, breitet sich über 2,2 Sekunden langsam aus und ist bei etwa 1,3 Sekunden am dunkelsten. Der Tastenklang legt zwei kurze Töne von 620 und 1240 Hz übereinander und verklingt in 0,15 Sekunden, wie ein Holzknopf.

## Die Klänge, die wir neu gemacht haben

Acht der ersten Effekte hatten einige Probleme, deshalb haben wir sie neu gemacht.

- Manche Spitzen stießen an die Obergrenze. Jetzt liegen alle mindestens 1 dB darunter, sodass nichts mehr verzerren kann.
- Drei Trommeln wurden abgeschnitten, bevor der zweite Schlag zu Ende war. Jetzt blendet jeder Klang in den ersten und letzten 5 ms weich aus und ein, sodass es nicht knackt.
- Die Lautstärke schwankte von Klang zu Klang. Jetzt stimmt der mittlere Pegel der acht auf 0,1 dB genau überein.

Beim Neumachen haben wir versucht, den Charakter der Klänge nicht zu verändern. Die Tonhöhen der Trommeln, die absteigende Form des Siegels und der Zeitpunkt, an dem die Tusche am dunkelsten ist, blieben erhalten.

## Die Musik

Die Musik baut auf Nachbildungen einer Gayageum und einer Daegeum auf. Die Gayageum entsteht, indem man eine gezupfte Saite berechnet (die Karplus-Strong-Methode), die Daegeum, indem man Obertöne schichtet und Atemrauschen beimischt. Dazu kommen eine Trommel und ein tiefer Bordun, und die Töne stammen aus einer Fünftonleiter der traditionellen koreanischen Musik. Es gibt je ein Stück für Menü, Karte, Kampf und Sieg.

## So klingt es auf dem Bildschirm

- Wenn die Buchstaben des Titels mit einem Schlag herabfallen, begleitet eine Vibration den Klang.
- Die Videos zwischen den Akten enthalten Trommeln, Hufschläge, Wind, Donner und das Siegel.
- Der Ton erklingt auch bei eingeschaltetem Stummschalter des Handys, und die Musik spielt auf vier Bildschirmen.
- In den Einstellungen lassen sich die Effekte ausschalten oder leiser stellen.

## Was wir noch nicht geschafft haben

Ehrlich gesagt haben wir diese Klänge noch nicht lange genug mit menschlichen Ohren gehört. Lautstärke, Länge und Abschneidungen haben wir anhand von Zahlen geprüft, aber ob der Holzknopf und das Trommelfell gut klingen, muss auf echten Lautsprechern und Kopfhörern noch weiter angehört werden. Die Musik ist eine erste Version, und es bleibt Raum zum Feinschliff.

// Einen Klang kann man mit Zahlen einstellen, entschieden wird am Ende mit dem Ohr.
