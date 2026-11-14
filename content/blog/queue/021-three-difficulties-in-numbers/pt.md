---
title: Três dificuldades presas por números
description: Como simulamos milhares de partidas para que fácil, normal e difícil fiquem cada uma em sua faixa de vitórias, e por que os bots fazem o difícil parecer ainda mais difícil.
date: 2026-11-18
copy_review: iris 2026-11-14
slug: three-difficulties-in-numbers
lang: pt
translation_of: ko
---

Quem escolhe fácil espera vencer quase sempre, e quem escolhe difícil espera ser pressionado. Parece óbvio, mas toda vez que alguém muda uma regra ou um general, isso se desajusta sem que ninguém perceba. Por isso prendemos a faixa de cada dificuldade com testes. O jogo ainda está em desenvolvimento, e este texto é uma nota sobre esse método.

## O que já vigiávamos

Antes também havia testes. Eles olhavam quanto uma carta ou um general famoso aumenta a taxa de vitórias, e se no fácil todas as nações ficavam entre 60 e 95 por cento. O que nada cobria era a taxa de vitórias absoluta no normal e no difícil, nem o fato simples de que o fácil deve ser mais fácil que o normal, e o normal mais fácil que o difícil.

## Como se mede

Os bots jogam 200 partidas por nação, com um conjunto fixo de sementes e as mesmas regras com que o aplicativo começa. O resultado é sempre o mesmo e o conjunto inteiro leva alguns segundos para rodar. As médias das quatro nações medidas em 5 de novembro são estas.

| Partida | Fácil | Normal | Difícil |
|---|---|---|---|
| Ato 1 | 79,5 % | 23,8 % | 6,0 % |
| Ato 1 histórico | 77,5 % | 30,5 % | 7,9 % |
| Rio Han | 72,3 % | 45,4 % | 4,4 % |

Cada teste admite cerca de 10 pontos percentuais para cima e para baixo do valor medido. Se uma mudança empurrar o resultado para fora da faixa, o teste falha.

## Regras acrescentadas

- Entre as dificuldades deve haver uma diferença de mais de 15 pontos percentuais.
- No difícil, nenhuma nação deve passar de 25 por cento.
- No fácil, nenhuma nação deve cair abaixo de 55 por cento.
- Com a mesma semente, o resultado deve se repetir exatamente igual.

## Por que o difícil é tão baixo

Os bots não usam diplomacia nem espiões, então jogam pior que uma pessoa. Os valores baixos do normal e do difícil são os do bot, não uma promessa para um jogador humano. Desajustamos a faixa de propósito e vimos o teste falhar de verdade, o que confirma que o mecanismo funciona.

## O que ele não consegue dizer

A taxa de vitórias não diz se uma partida foi justa nem se foi divertida. Essas respostas continuam vindo de jogar à mão. Se um dia precisarmos mover uma faixa de propósito, corrigiremos juntos a tabela e a nota no início do arquivo de testes.

// Os números mantêm a dificuldade honesta. Não a tornam divertida.
