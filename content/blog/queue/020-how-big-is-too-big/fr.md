---
title: À partir de quelle taille un jeu mobile est-il trop gros ?
description: Pourquoi nous avons fixé un budget de taille pour les images, les sons et les polices d'Iltonggi, et la garde qui fait échouer la compilation en cas de dépassement.
date: 2026-11-17
slug: how-big-is-too-big
lang: fr
translation_of: ko
---

Un jeu long à télécharger, ou long à afficher son premier écran, perd des gens avant qu'ils jouent. Iltonggi contient beaucoup de choses : des polices d'allure ancienne, des peintures, de la musique et des effets sonores, et des textes en onze langues. Si personne n'y veille, il ne fait que grossir. Nous avons donc fixé un budget et chargé l'ordinateur de le faire respecter. Le jeu est encore en développement.

## Ce que nous mesurons

Nous ne comptons que les fichiers réellement intégrés à l'application, pas tout le contenu du projet. Au 5 novembre, les chiffres étaient les suivants :

| Élément | Mesure | Limite |
|---|---|---|
| Tous les fichiers intégrés (74) | 9,83 MiB | 12 000 000 octets |
| Plus gros fichier (la police à empattements, compressée) | 1,29 Mo | 1,5 Mo |
| Audio | 4,27 Mo | 5 Mo |
| Photos (23) | 3,55 Mo | 4,2 Mo |
| Lu avant la première image | 1,48 Mo | 1,7 Mo |

Chaque limite laisse environ 15 à 18 % de marge. Nous interdisons aussi les formats qui ne doivent jamais être livrés, comme l'audio non compressé et les images à calques.

## Une garde, pas une promesse

Une règle qui ne vit que dans un document finit oubliée. La vérification de taille s'exécute donc dans la même barrière que la mise en forme, l'analyse et les tests. Si une limite est dépassée, la compilation échoue. Relever une limite est permis, mais seulement volontairement : il faut modifier ensemble le chiffre dans le script et celui du tableau.

## La police laissée dehors

La police à empattements pèse 3,18 Mo en fichier d'origine, ce qui est beaucoup pour un téléphone. Nous la livrons compressée à 1,29 Mo, et l'original ne reste que dans le dépôt. Si quelqu'un l'ajoute à l'application par erreur, la règle des formats interdits et le total la détectent.

## Temps de démarrage

Sur un Mac, décompresser la police prend environ 6 millisecondes, et charger l'image d'ouverture environ 14. Nous n'avons pas fixé de limite de temps, car des mesures faites sur Mac disent peu de choses d'un vrai téléphone en démarrage à froid.

## Pas encore connu

Nous ne connaissons pas encore la taille finale du paquet installable, puisque la compression, le code et le moteur ne s'ajoutent qu'à la compilation. Nous comptons noter ce chiffre à côté de ce tableau dès que nous l'aurons.

// Un budget a de la force parce qu'il sait dire non.
