---
title: Tres dificultades sujetas con números
description: Cómo simulamos miles de partidas para que fácil, normal y difícil se mantengan en su propio rango de victorias, y por qué los bots hacen que difícil parezca todavía más difícil.
date: 2026-11-18
slug: three-difficulties-in-numbers
lang: es
translation_of: ko
---

Quien elige fácil espera ganar casi siempre, y quien elige difícil espera perder terreno. Parece obvio, pero cada vez que alguien cambia una regla o un general, esto se desajusta sin que nadie lo note. Por eso sujetamos el rango de cada dificultad con pruebas. El juego sigue en desarrollo, y esta entrada es una nota sobre ese método.

## Lo que ya vigilábamos

Antes también había pruebas. Miraban cuánto sube la tasa de victorias una carta o un general famoso, y si en fácil todas las naciones quedaban entre el 60 y el 95 por ciento. Lo que no cubría nada era la tasa de victorias absoluta en normal y en difícil, ni el hecho sencillo de que fácil debe ser más fácil que normal, y normal más fácil que difícil.

## Cómo se mide

Los bots juegan 200 partidas por nación, con un conjunto fijo de semillas y las mismas reglas con las que arranca la aplicación. El resultado es siempre el mismo y todo el conjunto tarda unos segundos en ejecutarse. Los promedios de las cuatro naciones medidos el 5 de noviembre son estos.

| Partida | Fácil | Normal | Difícil |
|---|---|---|---|
| Acto 1 | 79.5% | 23.8% | 6.0% |
| Acto 1 histórico | 77.5% | 30.5% | 7.9% |
| Río Han | 72.3% | 45.4% | 4.4% |

Cada prueba admite unos 10 puntos porcentuales por encima y por debajo del valor medido. Si un cambio empuja el resultado fuera del rango, la prueba falla.

## Reglas añadidas

- Entre dificultades debe haber una diferencia de más de 15 puntos porcentuales.
- En difícil, ninguna nación debe superar el 25 por ciento.
- En fácil, ninguna nación debe bajar del 55 por ciento.
- Con la misma semilla, el resultado debe repetirse exactamente igual.

## Por qué difícil es tan bajo

Los bots no usan diplomacia ni espías, así que juegan peor que una persona. Los valores bajos de normal y difícil son los del bot, no una promesa para un jugador humano. Desajustamos el rango a propósito y comprobamos que la prueba fallaba de verdad, lo que confirma que el mecanismo funciona.

## Lo que no puede decirnos

La tasa de victorias no dice si una partida fue justa ni si fue divertida. Esas respuestas se siguen obteniendo jugando a mano. Si alguna vez tenemos que mover un rango a propósito, corregiremos a la vez la tabla y la nota que hay al principio del archivo de pruebas.

// Los números mantienen la dificultad honesta. No la hacen divertida.
