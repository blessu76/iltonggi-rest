---
title: Um save que sobrevive mesmo quando quebra
description: Como o Iltonggi protege o seu progresso quando a gravação de um arquivo é interrompida, e como testamos isso sem estragar um celular de verdade.
date: 2026-11-15
slug: a-save-that-survives
lang: pt
translation_of: ko
---

Poucas coisas desanimam tanto quanto abrir um jogo em que você investiu muito tempo e descobrir que o progresso sumiu. Se a bateria do celular acaba ou o aplicativo fecha no meio da gravação de um arquivo, pode sobrar um arquivo escrito pela metade. Queríamos que o Iltonggi sobrevivesse a isso. O jogo ainda está em desenvolvimento, e este texto é uma nota sobre até onde vai a proteção hoje.

## Quase tudo já existia

Quando nos sentamos para acrescentar uma proteção, descobrimos que o save principal já a tinha. Nós é que tínhamos esquecido. Ela funciona em quatro etapas.

1. O novo save é gravado primeiro em um arquivo temporário e só depois trocado pelo antigo. Se a gravação for interrompida, o save antigo continua intacto.
2. O save imediatamente anterior é mantido como backup de uma geração.
3. Ao carregar, verifica-se se o arquivo é lido corretamente.
4. Se estiver corrompido, volta-se ao backup. Se o backup também estiver corrompido, o jogo não trava: começa uma partida nova.

A lacuna era que isso só existia para o save principal. Os três espaços de save, as configurações, os atos concluídos, as missões, o mercado, os itens, o apelido e os registros eram gravados direto, sem essa proteção.

## Ampliar, mas não tudo

Ativamos o backup em todos os arquivos cuja perda dói. Não o ativamos nos que podem se perder sem problema, como logs, avisos, clima e históricos. Com uma lista curta, ficam menos arquivos no celular e menos coisas a examinar. Os nomes e o conteúdo dos arquivos não mudam, então os saves existentes continuam valendo. O que se acrescenta é apenas a cópia de backup.

## Testar sem estragar o celular

Não dá para pedir a um jogador que desligue a energia no meio de uma gravação, então agora, para cada arquivo com backup, reproduzimos quatro situações em testes.

- Texto do save corrompido: volta-se ao backup.
- Arquivo vazio: volta-se ao backup.
- Corrompido e sem backup: o jogo não trava; começa uma partida nova.
- Sobrou apenas um arquivo temporário escrito pela metade: o save anterior continua lá.

## O que não conseguimos confirmar

Esses testes são feitos em um computador. Ainda não vimos a recuperação de um arquivo que quebramos de propósito em um aparelho real, então essa parte não está confirmada. Além disso, quando um arquivo que não é o save principal é recuperado, nenhum aviso aparece para o jogador: ele volta em silêncio. Para as configurações, achamos que isso é o certo, mas podemos repensar.

// Um bom save é aquele que não se nota, a não ser quando te salva.
