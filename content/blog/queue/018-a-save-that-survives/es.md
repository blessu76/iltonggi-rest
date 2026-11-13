---
title: Una partida guardada que sobrevive aunque se rompa
description: Cómo Iltonggi protege tu progreso cuando la escritura de un archivo se interrumpe, y cómo lo probamos sin romper un teléfono real.
date: 2026-11-15
slug: a-save-that-survives
lang: es
translation_of: ko
---

Pocas cosas desaniman tanto como abrir un juego al que has dedicado mucho tiempo y encontrar que el progreso ha desaparecido. Si al teléfono se le acaba la batería o la aplicación se cierra mientras escribe un archivo, puede quedar un archivo a medio escribir. Queríamos que Iltonggi sobreviviera a eso. El juego sigue en desarrollo, y esta entrada es una nota sobre hasta dónde llega hoy la protección.

## Ya existía casi todo

Cuando nos sentamos a añadir una salvaguarda, resultó que el guardado principal ya la tenía. Simplemente lo habíamos olvidado. Funciona en cuatro pasos.

1. La nueva partida se escribe primero en un archivo temporal y luego se intercambia. Si se interrumpe a mitad de escritura, el guardado anterior queda intacto.
2. El guardado inmediatamente anterior se conserva como copia de seguridad de una generación.
3. Al cargar, se comprueba que el archivo se lea correctamente.
4. Si está dañado, se vuelve a la copia de seguridad. Si la copia también está dañada, no se detiene: empieza una partida nueva.

El hueco era que esto solo existía para el guardado principal. Las tres ranuras de guardado, los ajustes, los actos superados, las misiones, el mercado, los objetos, el apodo y los registros se escribían sin más.

## Ampliar, pero no a todo

Activamos la copia de seguridad en todos los archivos cuya pérdida duele. No la activamos en los que se pueden perder sin consecuencias, como registros, avisos, el clima y los historiales. Con una lista corta quedan menos archivos en el teléfono y menos cosas que revisar. Los nombres y el contenido de los archivos no cambian, así que los guardados existentes siguen valiendo. Lo único que se añade es la copia de seguridad.

## Probar sin romper el teléfono

No podemos pedirle a un jugador que desconecte la corriente a mitad de una escritura, así que ahora, para cada archivo con copia de seguridad, reproducimos cuatro situaciones en pruebas.

- Texto del guardado dañado: se vuelve a la copia de seguridad.
- Archivo vacío: se vuelve a la copia de seguridad.
- Dañado y sin copia de seguridad: no se detiene; empieza una partida nueva.
- Solo queda un archivo temporal escrito a medias: el guardado anterior sigue ahí.

## Lo que no hemos podido confirmar

Estas pruebas se hacen en un ordenador. Todavía no hemos visto cómo se recupera un archivo que rompemos a propósito en un dispositivo real, así que esa parte no está confirmada. Además, cuando se recupera un archivo que no es el guardado principal, no aparece ningún aviso al jugador: vuelve en silencio. Para los ajustes creemos que es lo correcto, pero podríamos replantearlo.

// Un buen guardado es el que no se nota, salvo cuando te salva.
