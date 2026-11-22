---
title: Un pouce, une région : concevoir les commandes tactiles d'un jeu sur carte
description: Un jeu de conquête territoriale doit fonctionner avec un seul pouce sur un petit écran. Voici comment nous pensons les appuis, les glissements et les erreurs que nous voulons éviter.
slug: one-thumb-touch-controls
lang: fr
translation_of: en
copy_review: iris 2026-11-19
date: 2026-11-22
published: 2026-11-22T16:00:00+09:00
---

Iltonggi est un jeu sur carte, et ce type de jeu sur téléphone demande beaucoup à un seul pouce. Il faut choisir une région, voir ses troupes, déplacer une armée et lire le résultat, sans masquer la région même que l'on veut toucher. Cet article décrit notre façon de penser la saisie tactile. Le jeu est encore en développement : lisez donc ces règles comme ce que nous sommes en train de tester, et non comme un manuel terminé.

## Appuyer et glisser sont deux gestes différents

L'erreur la plus courante dans un jeu sur carte consiste à traiter chaque contact comme un clic. Un doigt qui bouge un peu pendant que la carte glisse dessous n'est pas une sélection. Nous séparons donc deux intentions : un appui bref, qui sélectionne, et un mouvement plus long, qui déplace la carte. Si le doigt parcourt une petite distance avant de se lever, le contact appartient à la carte et aucune région n'est choisie.

Le principe compte davantage que la distance exacte. Un joueur ne devrait jamais sélectionner une région par accident en faisant défiler une partie encombrée de la carte.

## Les régions sont petites sur un téléphone

Certaines régions sont étroites, et un pouce est large. Quand aucune autre région n'est proche, nous laissons la zone d'appui d'une région dépasser un peu sa bordure dessinée. Nous ne la rendons jamais assez grande pour voler un appui destiné à un voisin. Lorsque deux régions sont proches, le choix doit dépendre de l'endroit où le doigt se pose, et non de la région dessinée en dernier.

## Confirmer les gestes coûteux

Attaquer ou déplacer des troupes modifie l'état du jeu. Il doit donc être plus difficile de le faire par erreur que de regarder une région. Un appui montre ce qui se passerait, et une seconde action délibérée la valide. Cela coûte un peu de vitesse, et un joueur qui connaît la carte peut le trouver plus lent. Nous acceptons ce compromis, car une armée envoyée au mauvais endroit agace davantage qu'un appui de plus.

## Des sessions courtes, souvent interrompues

Les gens jouent à Iltonggi en sessions brèves : dans le bus, dans une file d'attente, quelques minutes avant de dormir. Une interruption peut survenir à tout moment, par un appel ou un passage à une autre application. Les commandes ne doivent donc pas dépendre d'un geste qui reste en cours longtemps. Un glissement inachevé doit simplement se terminer sans résultat, et la carte doit rester là où le joueur l'a laissée.

## Ce qu'il nous reste à vérifier

La taille des pouces varie, tout comme celle des écrans. Nos hypothèses viennent surtout des appareils que nous possédons. Nous prévoyons de tester les zones d'appui sur davantage d'écrans et d'observer où les joueurs appuient par erreur. Nous ne l'avons pas encore mesuré à grande échelle, donc cet article ne donne aucun chiffre.

// Le geste le plus sûr est celui que l'on peut annuler.
