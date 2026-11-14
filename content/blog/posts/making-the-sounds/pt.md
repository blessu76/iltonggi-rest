---
title: Dos tambores ao gayageum, também fizemos os sons nós mesmos
description: Como os 15 efeitos e as 4 músicas de Iltonggi foram sintetizados por script, sem áudio externo, e por que refizemos alguns.
slug: making-the-sounds
lang: pt
translation_of: ko
date: 2026-11-06
copy_review: iris 2026-11-14
published: 2026-11-06T12:00:00+09:00
---

O som é a parte de Iltonggi em que mexemos por mais tempo. Uma imagem vê-se de imediato, mas, quando um som está errado, é difícil dizer o que há de errado nele. Este texto é um registro de como os sons foram feitos e de por que refizemos alguns deles uma vez.

## Sem áudio externo

O jogo tem agora 19 sons: 15 efeitos e 4 músicas. Todos foram sintetizados do zero por script. Não usamos amostras baixadas nem áudio comprado. Por isso, rodar o mesmo script de novo produz o mesmo som de novo. Poder explicar a origem de cada som é o principal motivo de termos escolhido este caminho.

## Tambores, selo, bandeira e tinta

Há quatro sons de tambor para o combate e a marcha. Cada um parte de uma onda senoidal cuja altura desce, com uma breve rajada de ruído por cima para sugerir a baqueta no couro. As alturas são distintas, aproximadamente 55, 59, 65 e 85 Hz.

O som do selo ao tomar terra é uma nota grave que desce de 94 Hz a 39 Hz. Mas o alto-falante pequeno de um celular quase não consegue produzir notas tão baixas. Por isso misturamos alguns harmônicos, para que a pancada ainda se sinta quando a parte mais grave some.

O som da bandeira, usado na vitória e na passagem de turno, deixa o ruído passar só por uma faixa estreita e o faz tremular depressa, como um pano ao vento. Dura 1,4 segundo. A tinta usada na diplomacia espalha-se devagar durante 2,2 segundos e fica mais escura perto de 1,3 segundo. O som do botão sobrepõe dois tons curtos de 620 e 1240 Hz e se apaga em 0,15 segundo, como um botão de madeira.

## Os sons que refizemos

Oito dos primeiros efeitos tinham alguns problemas, então os fizemos de novo.

- Alguns picos tocavam o teto. Agora todos ficam pelo menos 1 dB abaixo, sem margem para distorcer.
- Três tambores eram cortados antes de o segundo golpe terminar. Agora cada som diminui suavemente nos primeiros e últimos 5 ms, sem estalos.
- O volume variava de um som para outro. Agora o nível médio dos oito coincide dentro de 0,1 dB.

Ao refazê-los, tentamos não mudar o caráter dos sons. As alturas dos tambores, a forma descendente do selo e o momento em que a tinta é mais escura foram mantidos.

## A música

A música gira em torno de imitações de um gayageum e de um daegeum. O gayageum é feito calculando uma corda dedilhada (o método de Karplus-Strong) e o daegeum, empilhando harmônicos e misturando ruído de respiração. Acrescentam-se um tambor e um bordão grave, e as notas vêm de uma escala de cinco notas da música tradicional coreana. Há uma faixa para o menu, uma para o mapa, uma para o combate e uma para a vitória.

## Como soa na tela

- Quando as letras do título caem com uma pancada, uma vibração acompanha o som.
- Os vídeos entre os atos têm tambores, cascos de cavalo, vento, trovão e o selo.
- O som toca mesmo com o interruptor de silêncio do celular ligado, e a música toca em quatro telas.
- Nas configurações é possível desligar ou baixar os efeitos.

## O que ainda não fizemos

Para ser sincero, ainda não ouvimos estes sons com ouvidos humanos por tempo suficiente. Conferimos por números o volume, a duração e os cortes, mas saber se o botão de madeira e o couro do tambor soam bem exige ouvir mais em alto-falantes e fones reais. A música é uma primeira versão e ainda há espaço para melhorá-la.

// Um som se ajusta com números, mas no fim decide-se pelo ouvido.
