---
title: Un pulgar, una región: diseñar los controles táctiles de un juego de mapa
description: Un juego de conquista de territorios debe funcionar con un solo pulgar en una pantalla pequeña. Así pensamos los toques, los arrastres y los errores que queremos evitar.
slug: one-thumb-touch-controls
lang: es
translation_of: en
copy_review: iris 2026-11-19
date: 2026-11-22
published: 2026-11-22T16:00:00+09:00
---

Iltonggi es un juego de mapa, y un juego de mapa en el teléfono exige mucho a un solo pulgar. Hay que elegir una región, ver sus tropas, mover un ejército y leer el resultado, sin tapar la región que se quiere pulsar. Esta entrada describe cómo pensamos la entrada táctil. El juego sigue en desarrollo, así que estas reglas deben leerse como lo que estamos probando, no como un manual terminado.

## Tocar y arrastrar son cosas distintas

El error más habitual en un juego de mapa es tratar cada toque como un clic. Un dedo que se mueve un poco mientras el mapa se desliza debajo no es una selección. Por eso separamos dos intenciones: un toque breve, que selecciona, y un movimiento más largo, que desplaza el mapa. Si el dedo recorre una distancia pequeña antes de levantarse, el toque pertenece al mapa y no se elige ninguna región.

Lo importante es el principio más que la distancia exacta. Un jugador nunca debería seleccionar una región por accidente al desplazarse por una zona llena del mapa.

## Las regiones son pequeñas en un teléfono

Algunas regiones son estrechas y el pulgar es ancho. Cuando no hay otra región cerca, dejamos que el área de toque de una región llegue un poco más allá de su borde dibujado. Nunca la hacemos tan grande que robe un toque destinado a un vecino. Cuando dos regiones están cerca, la elección debe depender de dónde cae el toque, no de cuál se dibujó al final.

## Confirmar los movimientos costosos

Atacar o mover tropas cambia el estado del juego, así que debe ser más difícil hacerlo por accidente que mirar una región. Un toque muestra lo que pasaría, y una segunda acción deliberada lo confirma. Esto cuesta un poco de velocidad, y quien conozca el mapa quizá lo note más lento. Aceptamos ese cambio, porque un ejército mal enviado molesta más que un toque extra.

## Sesiones cortas, interrupciones frecuentes

La gente juega a Iltonggi en sesiones breves: en el autobús, en una cola, unos minutos antes de dormir. Una interrupción puede llegar en cualquier momento, como una llamada o un cambio a otra aplicación. Por eso los controles no deben depender de un gesto que dure mucho. Un arrastre a medias debe terminar sin resultado, y el mapa debe quedarse donde lo dejó el jugador.

## Lo que aún debemos comprobar

El tamaño de los pulgares varía, y también el de las pantallas. Nuestras suposiciones vienen sobre todo de los dispositivos que tenemos. Planeamos probar las áreas de toque en más pantallas y observar dónde los jugadores tocan por error. Todavía no lo hemos medido a gran escala, así que esta entrada no incluye cifras.

// El toque más seguro es el que puedes deshacer.
