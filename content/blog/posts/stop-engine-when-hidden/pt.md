---
title: Parar o motor quando ninguém está olhando
description: Quando a tela fica coberta ou o app vai para o segundo plano, o motor do jogo para. Esta é a regra que definimos ao migrar para um kit de motor compartilhado, e o que ainda não medimos.
slug: stop-engine-when-hidden
lang: pt
translation_of: en
date: 2026-11-23
published: 2026-11-23T14:00:00+09:00
---

As cenas de mapa e de batalha de Iltonggi são imagens em movimento. Os soldados andam, as bandeiras balançam e os combates se desenrolam quadro a quadro. Mas quando o jogador atende uma ligação ou troca de app, não há motivo para continuar desenhando imagens que ninguém consegue ver. Este texto registra a regra que definimos hoje, enquanto passávamos o motor do jogo para um kit compartilhado. O jogo ainda está em desenvolvimento.

## Parar quando nada pode ser visto

Quando a tela é coberta, ou o app vai para o segundo plano, o motor para. Desenhar uma cena que ninguém pode ver só gasta bateria. Quando o jogador volta, o desenho continua de onde parou. O mapa que o jogador deixou precisa continuar igual, então não deixamos o tempo do jogo correr em silêncio enquanto o app está oculto.

## Um único lugar decide quando parar

Antes, cada cena tinha seu próprio código para parar. O mapa, o palco de batalha e a tela do menu inicial verificavam cada um se estavam ocultos, e cada um precisava ser corrigido separadamente. Agora essa tarefa fica com uma única carcaça compartilhada. As cenas não perguntam mais se estão visíveis. Elas seguem o estado que a carcaça define.

## A animação do combate continua

Quando dois exércitos se chocam no mapa, a animação só avança enquanto o motor está rodando. Então, durante um choque, o motor parado é ligado naquele momento e desligado de novo quando o choque termina. A velocidade e a ordem da animação não mudaram. Também fechamos uma brecha: se um choque terminar com a tela coberta, o motor não se reinicia sozinho quando a tela voltar.

## O que ainda não medimos

Ainda não medimos quanta bateria isso economiza. Algumas coisas só podem ser verificadas em aparelhos reais: mandar o app para o segundo plano e trazê-lo de volta, alternar entre o mapa e outras telas, o limite de 30 quadros por segundo e quanto tempo o desenho leva na GPU. Até medirmos, este texto não traz números de bateria.

// A imagem que ninguém vê é a mais barata de pular.
