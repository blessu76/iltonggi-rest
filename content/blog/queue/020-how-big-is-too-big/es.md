---
title: Cuánto es demasiado grande para un juego de móvil
description: Cómo pusimos un presupuesto de tamaño a las imágenes, el sonido y las fuentes de Iltonggi, y un mecanismo que detiene la compilación si se supera.
date: 2026-11-17
copy_review: iris 2026-11-14
slug: how-big-is-too-big
lang: es
translation_of: ko
---

Un juego que tarda en descargarse o cuya primera pantalla aparece tarde pierde a la gente antes de que lo pruebe. Iltonggi lleva mucho dentro: una fuente de aire antiguo, ilustraciones, música y efectos de sonido, y textos en varios idiomas. Si nadie lo vigila, solo crece. Por eso fijamos un presupuesto y hacemos que lo haga cumplir el ordenador. El juego sigue en desarrollo.

## Qué se mide

No contamos todo lo que hay en el proyecto, sino solo los archivos que la aplicación empaqueta de verdad. Los valores al 5 de noviembre son estos.

| Concepto | Medido | Límite |
|---|---|---|
| Total de recursos empaquetados (74 archivos) | 9,83 MiB | 12.000.000 bytes |
| El archivo más grande (fuente Myeongjo, comprimida) | 1,29 MB | 1.5 MB |
| Sonido | 4,27 MB | 5 MB |
| Fotos (23) | 3,55 MB | 4.2 MB |
| Lo que se lee antes de la primera pantalla | 1,48 MB | 1.7 MB |

En cada límite dejamos un margen de entre el 13 y el 16 por ciento. También se bloquean formatos que no deben incluirse, como el sonido sin comprimir o los archivos de imagen con capas.

## Un mecanismo, no una promesa

Las reglas que solo están en un documento se olvidan. Por eso la comprobación de tamaño se ejecuta en la misma puerta que el formato, el análisis y las pruebas. Si se supera un límite, la compilación falla. Subir un límite es posible, pero solo si se hace a propósito: hay que corregir juntos el número del script y la tabla.

## La fuente se queda fuera

La fuente Myeongjo original pesa 3,18 MB, demasiado para un teléfono. La incluimos comprimida a 1,29 MB y el original queda solo en el repositorio. Si alguien lo sube a la aplicación por error, la regla de formatos prohibidos y el límite total lo detectan a la vez.

## Tiempo de arranque

Descomprimir la fuente en un Mac lleva unos 6 milisegundos, y leer la ilustración de apertura unos 14 milisegundos. No hemos puesto un límite de tiempo, porque un valor medido en un Mac dice poco sobre el primer arranque en un teléfono real.

## Lo que aún no sabemos

Todavía no conocemos el tamaño final del paquete de instalación, porque la compresión, el código y el motor solo se suman en el momento de compilar. Cuando sepamos el valor, pensamos anotarlo junto a esta tabla.

// Un presupuesto tiene fuerza porque puede decir que no.
