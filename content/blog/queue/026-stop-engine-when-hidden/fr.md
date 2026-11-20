---
title: Arrêter le moteur quand personne ne regarde
description: Lorsque l'écran est masqué ou que l'application passe en arrière-plan, le moteur du jeu s'arrête. Voici la règle fixée lors du passage à un kit de moteur partagé, et ce que nous n'avons pas encore mesuré.
slug: stop-engine-when-hidden
lang: fr
translation_of: en
date: 2026-11-23
---

Les scènes de carte et de bataille d'Iltonggi sont des images animées. Les soldats marchent, les bannières flottent et les combats se déroulent image par image. Mais lorsqu'un joueur répond à un appel ou passe à une autre application, rien ne justifie de continuer à dessiner des images que personne ne peut voir. Ce texte consigne la règle que nous avons fixée aujourd'hui, pendant le passage du moteur du jeu vers un kit partagé. Le jeu est encore en développement.

## S'arrêter quand rien ne peut être vu

Lorsque l'écran est masqué, ou que l'application passe en arrière-plan, le moteur s'arrête. Dessiner une scène que personne ne peut voir ne fait que consommer la batterie. Quand le joueur revient, le dessin reprend là où il s'était arrêté. La carte que le joueur a quittée doit rester la même, et nous ne laissons donc pas le temps du jeu s'écouler en silence pendant que l'application est cachée.

## Un seul endroit décide quand s'arrêter

Auparavant, chaque scène avait son propre code d'arrêt. La carte, la scène de bataille et la vue du monde vérifiaient chacune si elles étaient masquées, et chacune devait être corrigée séparément. Cette tâche revient désormais à une seule coque commune. Les scènes ne demandent plus si elles sont visibles. Elles suivent l'état que fixe la coque.

## L'animation des combats continue

Lorsque deux armées s'affrontent sur la carte, l'animation ne progresse que lorsque le moteur tourne. Pendant un affrontement, le moteur arrêté est donc relancé pour ce moment, puis arrêté de nouveau à la fin. La vitesse et l'ordre de l'animation n'ont pas changé. Nous avons aussi comblé une faille : si un affrontement se termine pendant que l'écran est masqué, le moteur ne redémarre plus tout seul au retour de l'écran.

## Ce que nous n'avons pas encore mesuré

Nous n'avons pas encore mesuré l'économie de batterie réelle. Certains points ne peuvent être vérifiés que sur de vrais appareils : envoyer l'application en arrière-plan puis la rouvrir, passer de la carte à la vue du monde, la limite de 30 images par seconde et le temps de dessin sur le GPU. Tant que nous ne les aurons pas mesurés, ce texte ne donne aucun chiffre de batterie.

// L'image que personne ne voit est la moins chère à sauter.
