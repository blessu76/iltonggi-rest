---
title: Para o comando direto não virar trapaça — testado pelo computador
description: Como o comando direto no Iltonggi evita virar trapaça: pedra-papel-tesoura em três lances, condições iguais de comparação, simulações no computador.
date: 2026-11-02
slug: direct-command-in-battle
lang: pt
translation_of: ko
---

As batalhas do Iltonggi são automáticas por padrão: num dia corrido, basta ver o resultado. Mas desde o início também queríamos poder acompanhar e comandar o combate, e por isso abrimos o “comando direto” na janela anterior ao ataque. O recurso ganhou forma no build 33, em 29 de outubro. Por enquanto só funciona no ataque; o comando direto na defesa ainda não foi feito.

## Pedra, papel e tesoura em três lances

O comando direto consiste em escolher, ao longo de três lances, formação, investida ou flanco. A formação vence a investida, a investida vence o flanco e o flanco vence a formação. Se você manda um batedor, pode espiar o que o inimigo vai jogar, e quem está dentro de um castelo costuma apostar na formação. Se as coisas pioram, é possível recuar e salvar metade das tropas.

Mantivemos as regras simples como pedra-papel-tesoura. Numa partida de 5 a 10 minutos, o comando direto viraria um peso se exigisse aprender regras longas. Em troca, pistas como o batedor e os hábitos dentro do castelo dão gosto a ler o adversário. Assim como o espião deixa ver o território sob a névoa, o batedor deixa ver a jogada do inimigo. A ideia de que informação é poder, no Iltonggi, continua no combate. A retirada existe pelo mesmo motivo: em vez de resistir até perder tudo, é preciso poder salvar metade e planejar o próximo passo; só assim comandar tem graça.

## Não pode virar trapaça

Se o comando direto for forte demais, todos vão usá-lo e a leveza da partida se perde. Se for fraco demais, ninguém usa. Se ele revertesse uma luta muito desfavorável, deixaria de ser comando e seria trapaça. Habilidade dos generais, tropas e clima são calculados exatamente como no combate automático, e o ganho do comando é mantido pequeno. Quem lê bem leva uma pequena vantagem, mas quem tem muito menos tropas não deve vencer só com o comando.

## Comparar em condições iguais

Para ver só o efeito do comando, todas as outras condições precisam ser iguais. Por isso comparamos taxas de vitória em combates com os mesmos generais, as mesmas tropas e o mesmo clima, mudando só a forma de comandar. O combate automático é a linha de base, e vemos o quanto o comando direto se afasta dela. Se o desvio for grande ou pequeno demais, ajustamos as regras de novo.

## 6.000 combates no computador

Segundo os registros de desenvolvimento, para conferir isso fizemos o computador comandar de vários jeitos e jogar 6.000 combates. Escolhendo ao acaso ou repetindo um só comando, a taxa de vitória ficou a menos de 1 ponto percentual do combate automático. Lendo os relatórios do batedor e respondendo a eles, o computador venceu cerca de 3 pontos percentuais a mais, e não houve nos registros nenhum combate muito desfavorável revertido.

Ninguém consegue jogar 6.000 combates à mão, então essa verificação fica com o computador. Desta vez também montamos primeiro os testes do motor e da simulação, e só depois a tela. Primeiro o equilíbrio em números, depois a forma que se toca. A tela e os textos em onze idiomas vieram em seguida.

Equilibrar com o computador não é novidade. Segundo os registros de desenvolvimento, no build 32, logo antes, já tínhamos medido do mesmo jeito e reduzido a grande diferença de taxa de vitória entre reinos no nível fácil. A ideia era que, qualquer reino escolhido, o “fácil” fosse igualmente fácil.

## O que sobra depois dos números

Bons números não garantem boa sensação nas mãos. O computador mede a taxa de vitória, mas não diz se comandar é divertido. Por isso seguimos lapidando jogando de verdade. O comando direto na defesa e uma conferência da partida inteira também continuam por fazer.

// Quem lê bem leva uma pequena vantagem; trapaça não funciona.
