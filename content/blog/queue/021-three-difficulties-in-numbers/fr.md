---
title: Trois niveaux de difficulté tenus par les chiffres
description: Comment nous simulons des milliers de batailles pour garder Facile, Normal et Difficile dans leurs plages de victoires, et pourquoi le robot fait paraître Difficile plus dur.
date: 2026-11-18
slug: three-difficulties-in-numbers
lang: fr
translation_of: ko
---

Si vous choisissez Facile, vous vous attendez à gagner la plupart du temps. Si vous choisissez Difficile, vous vous attendez à être poussé. C'est évident en apparence, mais cela se dérègle discrètement dès que quelqu'un modifie une règle ou un général. Nous maintenons donc chaque difficulté dans une plage grâce à des tests. Le jeu est encore en développement, et cette note explique la méthode.

## Ce qui était déjà gardé

Auparavant, nos tests vérifiaient de combien une carte ou un général célèbre augmente le taux de victoire, et si Facile donne à chaque royaume entre 60 et 95 pour cent. Rien ne couvrait le taux de victoire absolu de Normal et Difficile, ni le simple fait que Facile doit être plus aisé que Normal, et Normal plus aisé que Difficile.

## Comment nous mesurons

Un robot joue 200 parties par royaume, avec un jeu fixe de graines aléatoires, selon les mêmes règles que le démarrage de l'application. Les résultats sont identiques à chaque fois, et l'ensemble prend quelques secondes. Les moyennes sur quatre royaumes, mesurées le 5 novembre :

| Carte | Facile | Normal | Difficile |
|---|---|---|---|
| Acte 1 | 79,5 % | 23,8 % | 6,0 % |
| Acte 1 historique | 77,5 % | 30,5 % | 7,9 % |
| Han | 72,3 % | 45,4 % | 4,4 % |

Chaque test admet une marge d'environ 10 points de part et d'autre de la mesure. Si un changement pousse un résultat hors de sa plage, le test échoue.

## Quelques règles en plus

- Entre deux difficultés, l'écart doit dépasser 15 points.
- En Difficile, aucun royaume ne doit dépasser 25 pour cent.
- En Facile, aucun royaume ne doit tomber sous 55 pour cent.
- Avec la même graine, les résultats doivent se répéter à l'identique.

## Pourquoi Difficile paraît si bas

Le robot n'utilise ni diplomatie ni espions, il joue donc moins bien qu'une personne. Les faibles valeurs de Normal et Difficile sont celles du robot, pas une promesse pour les joueurs humains. Nous avons vérifié que la garde fonctionne en déréglant volontairement une plage et en voyant le test échouer.

## Ce que cela ne dit pas

Un taux de victoire ne dit pas si une partie a semblé équitable ou amusante. Ces réponses viennent toujours du jeu à la main. Si nous déplaçons un jour une plage volontairement, nous modifions ensemble le tableau en tête du fichier de test et les notes.

// Les chiffres peuvent garder une difficulté honnête. Ils ne la rendent pas amusante.
