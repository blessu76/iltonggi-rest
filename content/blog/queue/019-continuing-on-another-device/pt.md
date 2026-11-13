---
title: Continuar a partida em outro dispositivo
description: Como o Iltonggi permite continuar a partida entre dispositivos Apple, e a regra que definimos quando o conteúdo dos dois dispositivos é diferente.
date: 2026-11-16
slug: continuing-on-another-device
lang: pt
translation_of: ko
---

O pedido inicial era simples: poder continuar, em outro dispositivo da mesma conta, o jogo que se estava jogando em um dispositivo Apple. Parece pequeno, mas o difícil não é copiar o save. O difícil é decidir o que fazer quando os dois dispositivos têm versões diferentes. Este texto é uma nota sobre as regras que definimos. O jogo ainda está em desenvolvimento.

## A versão de referência fica no dispositivo

Cada dispositivo trata o próprio arquivo como o save verdadeiro. No iCloud há apenas uma cópia, não o original. Se o iCloud estiver desligado, se a sessão tiver sido encerrada ou se for Android, tudo funciona em silêncio, só dentro daquele dispositivo e sem erros. Participam o save principal, os três espaços de save e as configurações.

## Comparam-se três coisas

Para decidir o que fazer, cada dispositivo guarda a impressão digital da última versão em que coincidiu com a nuvem. Depois, compara.

- Só este dispositivo mudou: envia.
- Só a nuvem mudou: baixa.
- Os dois mudaram: uma regra escolhe um.

## Quando os dois mudaram

A ordem que definimos é esta.

1. Um save com conteúdo vence um save vazio.
2. Se o horário de gravação diferir em mais de 2 minutos, vence o mais recente.
3. Se diferir em menos de 2 minutos e for a mesma partida, vence o que tiver mais turnos.
4. Se mesmo assim não houver decisão, vale o deste dispositivo.

Essa parte dividiu opiniões. Dizer "vence quem mais avançou" teria sido mais fácil de explicar, mas achamos que "quem salvou por último" se aproxima mais do que o jogador espera. Quem perde não é apagado: fica guardado à parte como cópia de conflito.

## Mescla-se em vez de escolher

Há coisas que não podem ser perdidas no cara ou coroa. Os atos concluídos, as histórias dos atos vistos e os itens não são resolvidos escolhendo um lado, mas mesclados como a união dos dois conjuntos.

## Limite de tamanho

Se um texto passar de 200.000 caracteres, ele não é enviado e fica só no dispositivo. Esse limite é verificado por testes.

## Perceber durante a partida

No início, só relíamos a nuvem quando o jogador voltava ao aplicativo. Na versão de compilação 85, também são percebidas as mudanças feitas em outro dispositivo enquanto o aplicativo está em primeiro plano, e a tela de configurações mostra se a sincronização com o iCloud está ligada.

## O que ainda não confirmamos

Tudo isso são testes em um computador. Ainda não vimos com os nossos próprios olhos dois aparelhos reais da mesma conta trocando uma partida, então essa parte não está confirmada. As ilustrações dos generais e o progresso das missões ficam, de propósito, apenas em cada dispositivo.

// Sincronizar é fácil. O trabalho é decidir quem tem razão.
