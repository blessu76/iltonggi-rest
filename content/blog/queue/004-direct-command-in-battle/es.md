---
title: Que el mando directo no sea una trampa: equilibrarlo con el ordenador
description: Cómo evitamos que el mando directo de Iltonggi sea una trampa equilibrándolo con batallas simuladas, por qué sus reglas son simples y qué falta por hacer.
date: 2026-11-02
slug: direct-command-in-battle
lang: es
translation_of: ko
---

Las batallas de Iltonggi son automáticas por defecto, así que en los días ocupados puedes limitarte a ver el resultado. Pero desde el principio también quisimos que se pudiera tomar el mando y dirigir el combate uno mismo, y por eso añadimos el mando directo a la ventana previa al ataque. Tomó su primera forma en la versión 33, el 29 de octubre. Por ahora solo funciona cuando atacas. El mando directo en defensa todavía no está hecho.

## Piedra, papel o tijera en tres tiempos

El mando directo te permite elegir una de tres posturas a lo largo de tres tiempos: formación, carga o flanco. La formación vence a la carga, la carga vence al flanco y el flanco vence a la formación. Si envías exploradores, puedes atisbar lo que jugará el enemigo, y los enemigos dentro de un castillo suelen elegir la formación. Si te están haciendo retroceder, puedes retirarte y salvar la mitad de tus tropas.

Mantuvimos las reglas tan simples como piedra, papel o tijera. En una partida de 5 a 10 minutos, tener que aprender reglas largas convertiría el mando directo en una carga. En cambio, añadimos pistas, como los exploradores y los hábitos de los defensores de un castillo, para darle el gusto de leer al rival. Igual que los espías te dejan asomarte a las tierras cubiertas por la niebla, los exploradores te dejan asomarte a la jugada del enemigo. La idea de que reunir información es poder se traslada también al combate. Añadimos la retirada por la misma razón. Aguantar hasta perderlo todo es peor que salvar la mitad para volver a intentarlo, y un comandante necesita esa opción para sentirse como tal.

## No puede ser una trampa

Si el mando directo es demasiado fuerte, todos acaban usándolo y se rompe el carácter ligero y rápido de la partida. Si es demasiado débil, nadie lo usa. Si puede dar la vuelta a un combate muy desigual, ya no es mando, sino trampa. Las habilidades de los generales, la fuerza de las tropas y el clima se calculan exactamente igual que en el combate automático, y decidimos mantener pequeña la ventaja que da el mando. Quien lea bien debe tener una ligera ventaja, pero un bando con muchas menos tropas nunca debe ganar solo por el mando.

## Comparar con todo lo demás igual

Para ver solo el efecto del mando, todas las demás condiciones tienen que ser idénticas. Así que enfrentamos a los mismos generales, con las mismas tropas y el mismo clima, cambiando solo la forma de mandar, y comparamos los porcentajes de victoria. El combate automático es la referencia, y miramos cuánto se aleja de ella el mando directo. Si la diferencia es demasiado grande o demasiado pequeña, retocamos las reglas.

## 6.000 combates con el ordenador

Según nuestros registros de desarrollo, para comprobarlo hicimos que el ordenador librara 6.000 batallas dirigidas de diversas maneras. Elegir al azar o repetir una sola orden mantenía el porcentaje de victorias a menos de 1 punto porcentual del combate automático. Leer el informe de los exploradores y responder subía las victorias en unos 3 puntos porcentuales, y los registros no muestran ningún caso de darle la vuelta a un combate muy desigual.

Una persona no puede jugar 6.000 batallas a mano, así que este tipo de comprobación se deja al ordenador. Esta vez también construimos primero las pruebas del motor y de la simulación y añadimos la pantalla después. Es un orden de equilibrar primero con números y vestirlo luego con algo que se pueda tocar. La pantalla y los textos en once idiomas vinieron después.

No es la primera vez que equilibramos con el ordenador. Según nuestros registros de desarrollo, en la versión 32, justo anterior, medimos del mismo modo cómo variaban mucho los porcentajes de victoria entre reinos en dificultad fácil, y los acercamos. La idea era que, elijas el reino que elijas, lo fácil debe ser igual de fácil.

## Lo que queda después de los números

Buenos números no garantizan buena sensación. Un ordenador puede medir porcentajes de victoria, pero no puede decirte si mandar es divertido. Por eso seguimos puliéndolo jugando a mano. El mando directo en defensa y una comprobación a lo largo de una partida entera siguen siendo tareas pendientes.

// Quien lee bien tiene una ligera ventaja. Las trampas no funcionan.
