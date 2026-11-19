---
title: Um polegar, uma região: desenhando os controles de toque de um jogo de mapa
description: Um jogo de conquista de territórios precisa funcionar com um só polegar em uma tela pequena. Veja como pensamos em toques, arrastos e nos erros que queremos evitar.
slug: one-thumb-touch-controls
lang: pt
translation_of: en
date: 2026-11-22
copy_review: iris 2026-11-19
---

Iltonggi é um jogo de mapa, e um jogo de mapa no celular exige muito de um único polegar. É preciso escolher uma região, ver suas tropas, mover um exército e ler o resultado, sem cobrir a própria região que se quer tocar. Esta postagem descreve como pensamos a entrada por toque. O jogo ainda está em desenvolvimento, então leia estas regras como o que estamos testando, não como um manual pronto.

## Tocar e arrastar são coisas diferentes

O erro mais comum em um jogo de mapa é tratar cada toque como um clique. Um dedo que se move um pouco enquanto o mapa desliza por baixo não é uma seleção. Por isso separamos duas intenções: um toque curto, que seleciona, e um movimento mais longo, que desloca o mapa. Se o dedo percorrer uma distância pequena antes de soltar, o toque pertence ao mapa e nenhuma região é escolhida.

O princípio importa mais do que a distância exata. Um jogador nunca deveria selecionar uma região sem querer ao rolar por uma parte cheia do mapa.

## As regiões são pequenas em um celular

Algumas regiões são estreitas, e o polegar é largo. Quando não há outra região por perto, deixamos a área de toque de uma região ir um pouco além da borda desenhada. Nunca a deixamos tão grande a ponto de roubar um toque destinado a um vizinho. Quando duas regiões estão próximas, a escolha deve vir de onde o toque cai, e não de qual região foi desenhada por último.

## Confirmar os movimentos caros

Atacar ou mover tropas muda o estado do jogo, então deve ser mais difícil fazer isso por acidente do que olhar uma região. Um toque mostra o que aconteceria, e uma segunda ação deliberada confirma. Isso custa um pouco de velocidade, e quem conhece o mapa pode achar mais lento. Aceitamos essa troca, porque um exército enviado no lugar errado incomoda mais do que um toque a mais.

## Sessões curtas, interrupções frequentes

As pessoas jogam Iltonggi em sessões curtas: no ônibus, na fila, por alguns minutos antes de dormir. Uma interrupção pode acontecer a qualquer momento, como uma ligação ou a troca para outro aplicativo. Por isso os controles não podem depender de um gesto que fique em andamento por muito tempo. Um arrasto interrompido deve terminar sem resultado, e o mapa deve continuar onde o jogador o deixou.

## O que ainda precisamos verificar

O tamanho dos polegares varia, e o das telas também. Nossas suposições vêm sobretudo dos aparelhos que temos. Planejamos testar as áreas de toque em mais telas e observar onde os jogadores tocam por engano. Ainda não medimos isso em grande escala, então esta postagem não traz números.

// O toque mais seguro é aquele que você pode desfazer.
