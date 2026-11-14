---
title: Des tambours au gayageum, nous avons aussi fait les sons nous-mêmes
description: Comment les 15 effets et les 4 musiques d'Iltonggi ont été synthétisés par script sans audio extérieur, et pourquoi nous en avons refait certains.
slug: making-the-sounds
lang: fr
translation_of: ko
date: 2026-11-06
copy_review: iris 2026-11-14
published: 2026-11-06T12:00:00+09:00
---

Le son est la partie d'Iltonggi sur laquelle nous avons gardé la main le plus longtemps. Une image se voit tout de suite, mais quand un son est faux, il est difficile de dire ce qui cloche. Cet article raconte comment les sons ont été faits et pourquoi nous en avons refait certains une fois.

## Sans audio extérieur

Le jeu contient maintenant 19 sons : 15 effets et 4 musiques. Tous sont synthétisés de zéro par script. Nous n'avons utilisé ni échantillons téléchargés ni audio acheté. Relancer le même script redonne donc le même son. Pouvoir expliquer l'origine de chaque son est la principale raison pour laquelle nous avons choisi cette voie.

## Tambours, sceau, drapeau et encre

Il y a quatre sons de tambour pour le combat et la marche. Chacun part d'une onde sinusoïdale dont la hauteur descend, avec une brève rafale de bruit par-dessus pour évoquer la baguette sur la peau. Les hauteurs sont distinctes, à peu près 55, 59, 65 et 85 Hz.

Le son du sceau lorsqu'on prend une terre est une note grave qui descend de 94 Hz à 39 Hz. Mais le petit haut-parleur d'un téléphone sait à peine produire des notes aussi basses. Nous y avons donc mêlé quelques harmoniques, pour que le choc se sente encore quand la partie la plus grave disparaît.

Le son du drapeau, utilisé pour la victoire et le passage de tour, ne laisse passer le bruit que dans une bande étroite et le fait frémir rapidement, comme une étoffe au vent. Il dure 1,4 seconde. L'encre utilisée en diplomatie se répand lentement pendant 2,2 secondes et est la plus foncée vers 1,3 seconde. Le son du bouton superpose deux tons courts de 620 et 1240 Hz et s'éteint en 0,15 seconde, comme un bouton en bois.

## Les sons que nous avons refaits

Huit des premiers effets avaient quelques défauts, nous les avons donc refaits.

- Certains pics touchaient le plafond. Tous sont maintenant au moins 1 dB en dessous, sans risque de distorsion.
- Trois tambours étaient coupés avant la fin du second coup. Désormais, chaque son s'atténue en douceur sur ses 5 premières et ses 5 dernières millisecondes, sans claquement.
- Le volume variait d'un son à l'autre. Le niveau moyen des huit est maintenant aligné à 0,1 dB près.

En les refaisant, nous avons essayé de ne pas changer leur caractère. Les hauteurs des tambours, la forme descendante du sceau et le moment où l'encre est la plus foncée ont été conservés.

## La musique

La musique s'organise autour d'imitations d'un gayageum et d'un daegeum. Le gayageum est fait en calculant une corde pincée (la méthode de Karplus-Strong), et le daegeum en empilant des harmoniques et en y mêlant un bruit de souffle. On y ajoute un tambour et un bourdon grave, et les notes viennent d'une gamme de cinq notes de la musique traditionnelle coréenne. Il y a un morceau pour le menu, un pour la carte, un pour le combat et un pour la victoire.

## Ce que cela donne à l'écran

- Quand les lettres du titre s'abattent avec un choc, une vibration accompagne le son.
- Les vidéos entre les actes comportent des tambours, des sabots de cheval, du vent, du tonnerre et le sceau.
- Le son se fait entendre même quand le commutateur silencieux du téléphone est activé, et la musique joue sur quatre écrans.
- Dans les réglages, on peut couper les effets ou les baisser.

## Ce que nous n'avons pas encore fait

Pour être honnêtes, nous n'avons pas encore écouté ces sons avec des oreilles humaines assez longtemps. Nous avons vérifié par des chiffres le volume, la durée et les coupures, mais savoir si le bouton en bois et la peau du tambour sonnent bien demande d'écouter davantage sur de vrais haut-parleurs et de vrais écouteurs. La musique est une première version, et il reste de la place pour la peaufiner.

// On peut régler un son avec des chiffres, mais on tranche finalement à l'oreille.
