---
title: Seguir jugando en otro dispositivo
description: Cómo Iltonggi permite continuar una partida entre dispositivos Apple, y la regla que fijamos cuando el contenido de los dos dispositivos es distinto.
date: 2026-11-16
copy_review: iris 2026-11-14
slug: continuing-on-another-device
lang: es
translation_of: ko
---

La petición inicial era sencilla: poder seguir en otro dispositivo de la misma cuenta la partida que se jugaba en un dispositivo Apple. Parece pequeño, pero lo difícil no es copiar el guardado. Lo difícil es decidir qué hacer cuando los dos dispositivos tienen versiones distintas. Esta entrada es una nota sobre las reglas que fijamos. El juego sigue en desarrollo.

## La versión de referencia está en el dispositivo

Cada dispositivo trata su propio archivo como el guardado verdadero. En iCloud solo hay una copia, no el original. Si iCloud está desactivado, si se cerró la sesión o si se trata de Android, todo funciona en silencio, solo dentro de ese dispositivo y sin errores. Participan el guardado principal, las tres ranuras de guardado y los ajustes.

## Se comparan tres cosas

Para decidir qué hacer, cada dispositivo recuerda la huella de la última versión en la que coincidió con la nube. Después compara.

- Solo cambió este dispositivo: se sube.
- Solo cambió la nube: se descarga.
- Cambiaron los dos: una regla elige uno.

## Cuando cambiaron los dos

El orden que fijamos es este.

1. Un guardado con contenido gana a uno vacío.
2. Si la hora de guardado difiere en más de 2 minutos, gana el más reciente.
3. Si difiere en menos de 2 minutos y es la misma partida, gana el que tenga más turnos.
4. Si aun así no se decide, gana el de este dispositivo.

Esta parte generó desacuerdo. Decir "gana el que más avanzó" habría sido más fácil de explicar, pero pensamos que "el último que guardó" se acerca más a lo que el jugador espera. El que pierde no se borra: se conserva aparte como copia de conflicto.

## Se fusiona en lugar de elegir

Hay cosas que no deben perderse a cara o cruz. Los actos superados, las historias de los actos vistos y los objetos no se resuelven eligiendo un lado, sino fusionándolos como una unión de ambos conjuntos.

## Límite de tamaño

Si un texto supera los 200.000 caracteres, no se sube y se queda solo en el dispositivo. Este límite se comprueba con pruebas.

## Enterarse durante la partida

Al principio solo volvíamos a leer la nube cuando se regresaba a la aplicación. En una compilación posterior también se detectan los cambios hechos en otro dispositivo mientras la aplicación está en primer plano, y la pantalla de ajustes muestra si la sincronización con iCloud está activada.

## Lo que aún no hemos confirmado

Todo esto son pruebas en un ordenador. Todavía no hemos visto con nuestros propios ojos cómo dos dispositivos reales de la misma cuenta se pasan una partida, así que esa parte no está confirmada. Las ilustraciones de los generales y el avance de las misiones se quedan solo en cada dispositivo, a propósito.

// Sincronizar es fácil. El trabajo es decidir quién tiene razón.
