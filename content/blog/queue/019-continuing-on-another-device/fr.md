---
title: Reprendre la partie sur un autre appareil
description: Comment Iltonggi permet de continuer une partie d'un appareil Apple à l'autre, et les règles choisies quand deux appareils ne sont pas d'accord.
date: 2026-11-16
slug: continuing-on-another-device
lang: fr
translation_of: ko
---

La demande de départ était simple : si l'on joue sur un appareil Apple, on doit pouvoir continuer sur un autre avec le même compte. Cela paraît mineur, mais le plus dur n'est pas de copier une sauvegarde. C'est de décider ce qui se passe quand deux appareils en ont des versions différentes. Cette note décrit les règles que nous avons retenues. Le jeu est encore en développement.

## Le téléphone fait foi

Chaque appareil garde son propre fichier comme vraie sauvegarde. iCloud n'en détient qu'une copie, pas l'original. Si iCloud est désactivé, si vous êtes déconnecté ou si vous êtes sur Android, le jeu reste simplement sur cet appareil, sans erreur. La sauvegarde principale, les trois emplacements et les réglages participent.

## Une comparaison à trois

Pour décider quoi faire, chaque appareil retient l'empreinte de la dernière version qui correspondait au cloud. Puis il compare :

- Seul cet appareil a changé : on envoie.
- Seul le cloud a changé : on reçoit.
- Les deux ont changé : on choisit selon une règle.

## Quand les deux ont changé

Voici l'ordre que nous avons choisi.

1. Une sauvegarde non vide l'emporte sur une vide.
2. Si les heures de sauvegarde diffèrent de plus de deux minutes, la plus tardive l'emporte.
3. Si elles sont à moins de deux minutes et que c'est la même partie, celle qui compte le plus de tours l'emporte.
4. Sinon, celle de cet appareil.

Nous en avons débattu. Dire simplement « la progression la plus avancée gagne » aurait été plus facile à expliquer, mais nous avons jugé que « la dernière sauvegarde » correspond mieux à ce que veut le joueur. La copie perdante n'est pas supprimée : elle est mise de côté comme copie de conflit.

## Fusionner plutôt que choisir

Certaines choses ne doivent jamais se perdre à pile ou face. Les actes terminés, les récits d'actes déjà vus et ce que vous possédez sont fusionnés en union au lieu d'être pris d'un seul côté.

## Une limite de taille

Un seul texte de plus de 200 000 caractères n'est pas envoyé et reste sur l'appareil. Des tests couvrent cette limite.

## Remarquer un changement pendant que l'on joue

Au début, le jeu ne relisait le cloud qu'au retour dans l'application. Avec la version 85, il remarque aussi un changement fait sur un autre appareil pendant qu'il est au premier plan, et l'écran des réglages indique si la synchronisation iCloud est activée.

## Pas encore vérifié

Tout cela est testé sur ordinateur. Nous n'avons pas encore vu deux vrais appareils d'un même compte se passer une partie, donc cette partie n'est pas vérifiée. Les portraits des généraux et l'avancement des quêtes restent sur chaque appareil, par choix.

// Synchroniser est facile. Décider qui a raison, c'est le vrai travail.
