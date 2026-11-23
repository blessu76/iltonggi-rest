---
title: Detener el motor cuando nadie mira
description: Cuando la pantalla queda tapada o la app pasa al segundo plano, el motor del juego se detiene. Esta es la regla que fijamos al pasar a un kit de motor compartido, y lo que todavía no hemos medido.
slug: stop-engine-when-hidden
lang: es
translation_of: en
date: 2026-11-23
published: 2026-11-23T14:00:00+09:00
---

Las escenas de mapa y batalla de Iltonggi son imágenes en movimiento. Los soldados caminan, las banderas ondean y los combates se desarrollan cuadro a cuadro. Pero cuando el jugador atiende una llamada o cambia a otra app, no hay motivo para seguir dibujando imágenes que nadie puede ver. Este texto recoge la regla que fijamos hoy, mientras pasábamos el motor del juego a un kit compartido. El juego sigue en desarrollo.

## Parar cuando no se puede ver nada

Cuando la pantalla queda tapada, o la app pasa al segundo plano, el motor se detiene. Dibujar una escena que nadie puede ver solo gasta batería. Cuando el jugador vuelve, el dibujo continúa donde se quedó. El mapa que dejó el jugador debe seguir siendo el mismo, así que no dejamos que el tiempo del juego avance en silencio mientras la app está oculta.

## Un solo lugar decide cuándo parar

Antes, cada escena tenía su propio código para detenerse. El mapa, el escenario de batalla y la pantalla del menú inicial comprobaban cada uno si estaban ocultos, y cada uno había que corregirlo por separado. Ahora esa tarea la asume una sola carcasa compartida. Las escenas ya no preguntan si son visibles. Siguen el estado que fija la carcasa.

## La animación de combate sigue

Cuando dos ejércitos chocan en el mapa, la animación solo avanza mientras el motor funciona. Así que, durante un choque, el motor detenido se enciende en ese momento y se apaga de nuevo al terminar. La velocidad y el orden de la animación no han cambiado. También cerramos un hueco: si un choque termina mientras la pantalla está tapada, el motor ya no se vuelve a iniciar solo cuando la pantalla regresa.

## Lo que todavía no hemos medido

Todavía no hemos medido cuánta batería ahorra esto. Algunas cosas solo se pueden comprobar en dispositivos reales: enviar la app al segundo plano y volver, cambiar entre el mapa y otras pantallas, el límite de 30 cuadros por segundo y cuánto tarda el dibujo en la GPU. Hasta medirlo, este texto no da cifras de batería.

// La imagen que nadie ve es la más barata de saltarse.
