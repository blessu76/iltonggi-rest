---
title: Damit der Direktbefehl kein Trick wird – vom Computer gegengeprüft
description: Wie der Direktbefehl in Iltonggi kein Trick wird: Schere-Stein-Papier über drei Runden, gleiche Bedingungen, Computersimulationen und offene Aufgaben.
date: 2026-11-02
slug: direct-command-in-battle
lang: de
translation_of: ko
---

Die Kämpfe in Iltonggi laufen standardmäßig automatisch – an einem vollen Tag reicht es, sich das Ergebnis anzusehen. Von Anfang an gab es aber auch den Wunsch, einen Kampf selbst zu führen und dabei zuzusehen, und deshalb haben wir im Fenster vor dem Angriff den „Direktbefehl“ geöffnet. Die Funktion erhielt ihre erste Gestalt im Build Nr. 33 am 29. Oktober. Derzeit lässt sie sich nur beim Angreifen nutzen; den Direktbefehl bei der Verteidigung haben wir noch nicht gebaut.

## Schere, Stein, Papier über drei Runden

Beim Direktbefehl wählt man über drei Gefechtsrunden hinweg jeweils Formation, Sturmangriff oder Flanke. Die Formation schlägt den Sturmangriff, der Sturmangriff die Flanke und die Flanke die Formation. Schickt man einen Späher aus, kann man erahnen, was der Gegner wählt, und Feinde in einer Burg setzen oft auf die Formation. Wenn es schlecht läuft, kann man sich zurückziehen und die Hälfte der Truppen retten.

Die Regeln haben wir bewusst schlicht wie Schere, Stein, Papier gehalten. Bei einer Partie von 5 bis 10 Minuten würde der Direktbefehl eher zur Last, wenn man lange Regeln lernen müsste. Dafür gibt es Hinweise wie den Späher und die Gewohnheiten in der Burg, damit das Lesen des Gegners Spaß macht. So wie ein Spion den Blick in den Nebel öffnet, lässt der Späher ahnen, was der Gegner spielt. Der Gedanke, dass Information Macht ist, setzt sich in Iltonggi auch im Kampf fort. Aus demselben Grund gibt es den Rückzug: Statt bis zum Ende durchzuhalten und alles zu verlieren, soll man die Hälfte retten und das Nächste planen können; erst dann macht das Führen Freude.

## Es darf kein Trick werden

Ist der Direktbefehl zu stark, macht ihn jeder, und der Charakter einer leichten Partie geht verloren. Ist er zu schwach, benutzt ihn niemand. Wenn er einen stark benachteiligten Kampf umdreht, ist es keine Führung mehr, sondern ein Trick. Fähigkeiten der Feldherren, Truppenstärke und Wetter werden genauso berechnet wie beim automatischen Kampf, und den Gewinn durch den Befehl halten wir klein. Wer gut liest, hat einen kleinen Vorteil; wer weit weniger Truppen hat, soll allein durch Befehle nicht gewinnen können.

## Verglichen wird unter gleichen Bedingungen

Um nur die Wirkung des Befehls zu sehen, müssen alle übrigen Bedingungen gleich sein. Deshalb haben wir Kämpfe mit denselben Feldherren, denselben Truppen und demselben Wetter verglichen und nur die Art der Führung verändert. Der automatische Kampf ist die Grundlinie; wir schauen, wie weit der Direktbefehl davon abweicht. Ist die Abweichung zu groß oder zu klein, überarbeiten wir die Regeln.

## 6.000 Kämpfe am Computer

Nach unseren Entwicklungsaufzeichnungen ließen wir zur Überprüfung den Computer auf verschiedene Arten führen und spielten 6.000 Kämpfe durch. Bei zufälligen Befehlen oder einem einzigen, ständig wiederholten Befehl lag die Siegquote weniger als 1 Prozentpunkt vom automatischen Kampf entfernt. Wer die Späherberichte las und darauf reagierte, gewann etwa 3 Prozentpunkte mehr, und einen stark benachteiligten Kampf zu drehen, kam in den Aufzeichnungen nicht vor.

6.000 Kämpfe kann kein Mensch von Hand spielen, also übernimmt das der Computer. Auch diesmal haben wir zuerst die Tests für Engine und Simulation gebaut und die Oberfläche danach angefügt. Erst die Balance in Zahlen, dann die Form zum Anfassen. Bildschirm und die Texte in elf Sprachen kamen danach.

Das Ausbalancieren per Computer ist nicht neu. Nach unseren Entwicklungsaufzeichnungen haben wir schon im Build Nr. 32 davor auf dieselbe Weise gemessen und verringert, dass die Siegquote im leichten Schwierigkeitsgrad je nach Reich stark auseinanderging. Der Gedanke war: Egal, welches Reich man wählt, „leicht“ soll gleich leicht sein.

## Was nach den Zahlen bleibt

Gute Zahlen garantieren kein gutes Gefühl in der Hand. Der Computer misst die Siegquote, sagt aber nicht, ob das Führen Spaß macht. Deshalb feilen wir weiter, indem wir es selbst spielen. Der Direktbefehl bei der Verteidigung und ein Blick auf die Partie als Ganzes sind ebenfalls noch offen.

// Wer gut liest, hat einen kleinen Vorteil – Tricks funktionieren nicht.
