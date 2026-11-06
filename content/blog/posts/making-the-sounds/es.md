---
title: De los tambores al gayageum, también hicimos los sonidos nosotros
description: Cómo se sintetizaron con scripts los 15 efectos y las 4 músicas de Iltonggi sin audio externo, y por qué rehicimos algunos.
slug: making-the-sounds
lang: es
translation_of: ko
date: 2026-11-06
published: 2026-11-06T12:00:00+09:00
---

El sonido es la parte de Iltonggi a la que seguimos dando forma hasta más tarde. Una imagen se ve de inmediato, pero cuando un sonido está mal, es difícil decir qué le pasa. Este texto es un registro de cómo se hicieron los sonidos y por qué rehicimos algunos una vez.

## Sin audio externo

El juego tiene ahora 19 sonidos: 15 efectos y 4 músicas. Todos están sintetizados desde cero por script. No usamos muestras descargadas ni audio comprado. Por eso, si se vuelve a ejecutar el mismo script, se vuelve a obtener el mismo sonido. Poder explicar de dónde viene cada sonido es la razón principal por la que elegimos este camino.

## Tambores, sello, bandera y tinta

Hay cuatro sonidos de tambor para el combate y la marcha. Cada uno parte de una onda sinusoidal cuyo tono desciende, con una breve ráfaga de ruido encima para sugerir el golpe sobre el cuero. Los tonos se separan, aproximadamente en 55, 59, 65 y 85 Hz.

El sonido del sello al tomar tierra es una nota grave que baja de 94 Hz a 39 Hz. Pero el altavoz pequeño de un móvil apenas puede producir notas tan bajas. Por eso mezclamos algunos armónicos, de modo que el golpe se siga notando aunque falte la parte más grave.

El sonido de la bandera, que se usa en la victoria y al pasar de turno, deja pasar el ruido solo por una banda estrecha y lo hace temblar rápidamente, como una tela al viento. Dura 1,4 segundos. La tinta que se usa en la diplomacia se extiende despacio durante 2,2 segundos y es más oscura hacia los 1,3 segundos. El sonido del botón superpone dos tonos cortos de 620 y 1240 Hz y se apaga en 0,15 segundos, como un botón de madera.

## Los sonidos que rehicimos

Ocho de los primeros efectos tenían algunos problemas, así que los hicimos de nuevo.

- Algunos picos tocaban el techo. Ahora todos quedan al menos 1 dB por debajo, sin margen para distorsionar.
- Tres tambores se cortaban antes de terminar el segundo golpe. Ahora cada sonido se atenúa suavemente en sus primeros y últimos 5 ms, sin chasquidos.
- El volumen variaba de un sonido a otro. Ahora el nivel medio de los ocho coincide dentro de 0,1 dB.

Al rehacerlos intentamos no cambiar su carácter. Se mantuvieron los tonos de los tambores, la forma descendente del sello y el momento en que la tinta es más oscura.

## La música

La música gira en torno a imitaciones de un gayageum y un daegeum. El gayageum se hace calculando una cuerda pulsada (el método de Karplus-Strong) y el daegeum, apilando armónicos y mezclando ruido de aliento. Se añaden un tambor y un bordón grave, y las notas salen de una escala de cinco notas de la música tradicional coreana. Hay una pieza para el menú, otra para el mapa, otra para el combate y otra para la victoria.

## Cómo suena en pantalla

- Cuando las letras del título caen con un golpe, una vibración acompaña al sonido.
- Los vídeos entre actos llevan tambores, cascos de caballo, viento, trueno y el sello.
- El sonido se oye incluso con el interruptor de silencio del móvil activado, y la música suena en cuatro pantallas.
- En los ajustes se pueden apagar o bajar los efectos.

## Lo que aún no hemos hecho

Para ser sinceros, todavía no hemos escuchado estos sonidos con oídos humanos el tiempo suficiente. Comprobamos con números el volumen, la duración y los cortes, pero si el botón de madera y el cuero del tambor suenan bien exige escuchar más en altavoces y auriculares reales. La música es una primera versión y aún queda margen para pulirla.

// Un sonido se puede ajustar con números, pero al final se decide con el oído.
