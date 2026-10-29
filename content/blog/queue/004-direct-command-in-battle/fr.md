---
title: Que le commandement direct ne devienne pas de la triche : l'équilibrer par ordinateur
description: Comment nous évitons que le commandement direct d'Iltonggi tourne à la triche grâce à des batailles simulées, pourquoi ses règles restent simples, et la suite.
date: 2026-11-02
slug: direct-command-in-battle
lang: fr
translation_of: ko
---

Les batailles d'Iltonggi sont automatiques par défaut : les jours chargés, on peut se contenter du résultat. Mais dès le départ, nous voulions aussi qu'on puisse prendre la main et diriger le combat soi-même, et nous avons donc ajouté le commandement direct à la fenêtre qui précède l'attaque. Il a pris sa première forme dans la version 33, le 29 octobre. Pour l'instant, il ne fonctionne que lorsque vous attaquez. Le commandement direct en défense n'est pas encore fait.

## Pierre-feuille-ciseaux en trois temps

Le commandement direct vous permet de choisir l'une de trois postures sur trois temps : formation, charge ou flanc. La formation bat la charge, la charge bat le flanc, et le flanc bat la formation. Si vous envoyez des éclaireurs, vous pouvez entrevoir ce que jouera l'ennemi, et les ennemis retranchés dans un château choisissent souvent la formation. Si l'on vous repousse, vous pouvez battre en retraite et sauver la moitié de vos troupes.

Nous avons gardé des règles aussi simples que pierre-feuille-ciseaux. Dans une partie de 5 à 10 minutes, devoir apprendre de longues règles ferait du commandement direct un fardeau. En échange, nous avons ajouté des indices, comme les éclaireurs et les habitudes des défenseurs d'un château, pour offrir le plaisir de lire son adversaire. De même que les espions vous laissent entrevoir les terres dans le brouillard, les éclaireurs vous laissent entrevoir le coup de l'ennemi. L'idée que s'informer, c'est avoir du pouvoir se prolonge aussi dans le combat. Nous avons ajouté la retraite pour la même raison. Tenir jusqu'à tout perdre vaut moins que sauver la moitié pour retenter sa chance, et un chef a besoin de cette option pour se sentir chef.

## Il ne doit pas devenir de la triche

Si le commandement direct est trop fort, tout le monde finit par l'utiliser, et le caractère léger et rapide d'une partie se brise. S'il est trop faible, personne ne s'en sert. S'il peut renverser un combat très déséquilibré, ce n'est plus du commandement, c'est de la triche. Les capacités des généraux, la force des troupes et la météo se calculent exactement comme dans le combat automatique, et nous avons décidé de garder faible le gain que procure le commandement. Celui qui lit bien doit avoir un léger avantage, mais un camp très court en troupes ne doit jamais gagner par le seul commandement.

## Comparer en gardant tout le reste égal

Pour ne voir que l'effet du commandement, toutes les autres conditions doivent être identiques. Nous avons donc opposé les mêmes généraux, les mêmes troupes et la même météo, en ne changeant que la manière de commander, et comparé les taux de victoire. Le combat automatique sert de référence, et nous regardons de combien le commandement direct s'en écarte. Si l'écart est trop grand ou trop petit, nous retouchons les règles.

## 6 000 combats par ordinateur

D'après nos notes de développement, pour vérifier cela, nous avons fait livrer à l'ordinateur 6 000 batailles commandées de diverses façons. Choisir au hasard, ou répéter un seul ordre, laissait le taux de victoire à moins de 1 point de pourcentage du combat automatique. Lire le rapport des éclaireurs et réagir faisait gagner environ 3 points de pourcentage de plus, et les notes ne montrent aucun cas de renversement d'un combat très déséquilibré.

Une personne ne peut pas jouer 6 000 batailles à la main, et ce genre de vérification est donc confié à l'ordinateur. Cette fois encore, nous avons d'abord construit les tests du moteur et de la simulation, puis ajouté l'écran ensuite. C'est un ordre qui consiste à équilibrer d'abord avec des chiffres, puis à l'habiller de quelque chose qu'on peut toucher. L'écran et les textes en onze langues sont venus après.

Ce n'est pas la première fois que nous équilibrons par ordinateur. D'après nos notes de développement, dans la version 32, juste avant, nous avons mesuré de la même façon les taux de victoire très inégaux entre les royaumes en difficulté facile, et nous les avons resserrés. L'idée était que, quel que soit le royaume choisi, le niveau facile soit tout aussi facile.

## Ce qui reste après les chiffres

De bons chiffres ne garantissent pas de bonnes sensations. Un ordinateur peut mesurer des taux de victoire, mais il ne peut pas dire si commander est amusant. Nous continuons donc à le peaufiner en jouant à la main. Le commandement direct en défense et une vérification sur toute une partie restent devant nous.

// Qui lit bien a un léger avantage. La triche ne marche pas ici.
