---
title: Quanto é grande demais para um jogo de celular
description: Como colocamos um orçamento de tamanho nas imagens, no som e nas fontes do Iltonggi, e um mecanismo que interrompe a compilação quando ele é ultrapassado.
date: 2026-11-17
copy_review: iris 2026-11-14
slug: how-big-is-too-big
lang: pt
translation_of: ko
---

Um jogo que demora para baixar ou cuja primeira tela aparece tarde perde as pessoas antes de elas o experimentarem. O Iltonggi carrega muita coisa: uma fonte de ar antigo, ilustrações, música e efeitos sonoros, e textos em vários idiomas. Se ninguém vigiar, ele só cresce. Por isso definimos um orçamento e fazemos o computador cobrá-lo. O jogo ainda está em desenvolvimento.

## O que se mede

Não contamos tudo o que existe no projeto, mas apenas os arquivos que o aplicativo realmente empacota. Os valores em 5 de novembro são estes.

| Item | Medido | Limite |
|---|---|---|
| Total de recursos empacotados (74 arquivos) | 9,83 MiB | 12.000.000 bytes |
| O maior arquivo (fonte Myeongjo, comprimida) | 1,29 MB | 1.5 MB |
| Som | 4,27 MB | 5 MB |
| Fotos (23) | 3,55 MB | 4.2 MB |
| O que é lido antes da primeira tela | 1,48 MB | 1.7 MB |

Em cada limite deixamos uma folga de 13 a 16 por cento. Também são bloqueados formatos que não devem entrar, como som sem compressão ou arquivos de imagem com camadas.

## Um mecanismo, não uma promessa

Regras que existem apenas em um documento são esquecidas. Por isso a verificação de tamanho roda na mesma porta que a formatação, a análise e os testes. Se um limite for ultrapassado, a compilação falha. Aumentar um limite é possível, mas só quando feito de propósito: é preciso corrigir juntos o número do script e a tabela.

## A fonte fica de fora

A fonte Myeongjo original tem 3,18 MB, grande demais para um celular. Nós a incluímos comprimida para 1,29 MB, e o original fica apenas no repositório. Se alguém o colocar no aplicativo por engano, a regra de formatos proibidos e o limite total o pegam ao mesmo tempo.

## Tempo de inicialização

Descompactar a fonte em um Mac leva cerca de 6 milissegundos, e ler a ilustração de abertura leva cerca de 14 milissegundos. Não definimos um limite de tempo, porque um valor medido em um Mac diz pouco sobre a primeira execução em um celular de verdade.

## O que ainda não sabemos

Ainda não sabemos o tamanho final do pacote de instalação, porque a compressão, o código e o motor só são somados na hora da compilação. Quando soubermos o valor, pretendemos anotá-lo ao lado desta tabela.

// Um orçamento tem força porque pode dizer não.
