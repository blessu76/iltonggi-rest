---
title: Une sauvegarde qui survit à la casse
description: Comment Iltonggi protège votre progression si un fichier est coupé en pleine écriture, et comment nous l'avons testé sans abîmer un vrai téléphone.
date: 2026-11-15
slug: a-save-that-survives
lang: fr
translation_of: ko
---

Rien ne gâche plus vite une longue partie que d'ouvrir le jeu et de voir sa progression disparue. La batterie d'un téléphone peut se vider, ou l'application se fermer au milieu de l'écriture d'un fichier, et il reste alors la moitié d'un fichier. Nous voulions qu'Iltonggi y survive. Le jeu est encore en développement, et cette note dit jusqu'où va la protection aujourd'hui.

## Nous en avions déjà l'essentiel

En nous asseyant pour ajouter un filet de sécurité, nous avons découvert que la sauvegarde principale en avait déjà un. Nous l'avions oublié. Il fonctionne en quatre étapes.

1. La nouvelle sauvegarde est d'abord écrite dans un fichier temporaire, puis échangée. Si l'écriture est coupée, l'ancienne sauvegarde reste intacte.
2. Une génération de copie de secours de la sauvegarde précédente est conservée.
3. Au chargement, on vérifie que le fichier se lit correctement.
4. S'il est abîmé, on restaure la copie de secours. Si celle-ci est abîmée aussi, on démarre une nouvelle partie au lieu de planter.

Le défaut, c'est que seule la sauvegarde principale en bénéficiait. Les trois emplacements de sauvegarde, les réglages, les actes terminés, les quêtes, la boutique, les objets possédés, le pseudo et les records étaient écrits sans précaution.

## L'élargir, mais pas à tout

Nous avons activé la copie de secours pour tout fichier dont la perte ferait mal. Nous l'avons laissée désactivée pour les journaux, les conseils, la météo et l'historique, dont la perte ne coûte rien d'important. Une liste courte, c'est moins de fichiers sur le téléphone et moins de cas à raisonner. Les noms et le contenu des fichiers n'ont pas changé, donc les sauvegardes existantes continuent de fonctionner. Seule la copie de secours s'ajoute.

## Tester sans casser un téléphone

On ne peut pas demander à un joueur de couper le courant en pleine écriture. Nous avons donc reproduit quatre situations dans des tests, pour chaque fichier qui a désormais une copie de secours :

- Texte abîmé dans la sauvegarde : la copie de secours est restaurée.
- Fichier vide : la copie de secours est restaurée.
- Abîmé et sans copie : le jeu démarre à neuf sans planter.
- Seul un fichier temporaire à moitié écrit : la sauvegarde précédente est toujours là.

## Ce que nous n'avons pas vérifié

Ce sont des tests sur ordinateur. Nous n'avons pas encore abîmé volontairement un fichier sur un vrai appareil pour voir la récupération, donc cette partie n'est pas vérifiée. De plus, quand autre chose que la sauvegarde principale est restauré, le joueur ne voit aucun message : tout revient discrètement. Nous pensons que c'est juste pour les réglages, mais nous pourrons y revenir.

// Une bonne sauvegarde, on ne la remarque que le jour où elle nous sauve.
