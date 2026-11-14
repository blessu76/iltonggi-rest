---
title: From War Drums to Gayageum, We Made the Sounds Ourselves
description: How Iltonggi's 15 effects and 4 music tracks were synthesized by script with no outside audio, and why we remade some of them.
slug: making-the-sounds
lang: en
date: 2026-11-06
copy_review: iris 2026-11-14
published: 2026-11-06T12:00:00+09:00
---

Sound is the part of Iltonggi we keep touching the longest. A picture is seen at once, but when a sound is wrong it is hard to say what is wrong with it. This post is a record of how the sounds were made, and why we remade some of them once.

## No outside audio

The game now holds 19 sounds: 15 effects and 4 music tracks. Every one is synthesized from scratch by script. We used no downloaded samples and no purchased audio. That means running the same script again makes the same sound again. Being able to explain where each sound comes from is the main reason we chose this way.

## Drums, seal, flag, ink

There are four drum sounds for battle and marching. Each starts as a sine wave whose pitch sinks, with a short burst of noise on top to suggest a stick on hide. The pitches are set apart, at roughly 55, 59, 65 and 85 Hz.

The seal sound for taking land is a low note that falls from 94 Hz to 39 Hz. But a small phone speaker can barely produce notes that low. So we mixed in a few overtones, so that the thud is still felt when the lowest part drops out.

The flag sound, used for victory and for passing a turn, lets noise through only a narrow band and makes it flutter quickly, like cloth in the wind. It lasts 1.4 seconds. The ink sound used for diplomacy spreads slowly over 2.2 seconds and is darkest at about 1.3 seconds. The button sound layers two short tones at 620 and 1240 Hz and fades in 0.15 seconds, like a wooden button.

## The sounds we remade

Eight of the first effects had a few problems, so we made them again.

- Some peaks touched the ceiling. Every one is now at least 1 dB below it, leaving no room to distort.
- Three drums were cut off before their second hit finished. Now every sound fades softly over its first and last 5 ms, so there is no clicking.
- Loudness varied from sound to sound. The average level of the eight now matches within 0.1 dB.

When remaking them we tried not to change their character. The drum pitches, the falling shape of the seal and the moment the ink is darkest were all kept.

## The music

The music is built around imitations of a gayageum and a daegeum. The gayageum is made by calculating a plucked string (the Karplus-Strong method), and the daegeum by stacking overtones and mixing in breath noise. A drum and a low drone are added, and the notes come from a five-note scale used in Korean traditional music. There is one track each for the menu, the map, battle and victory.

## How it sounds on screen

- When the title letters land with a thud, a vibration goes with the sound.
- The videos between acts contain drums, hoofbeats, wind, thunder and the seal.
- Sound plays even with the phone's silent switch on, and music plays on four screens.
- In settings you can turn the effects off or lower them.

## What we have not done yet

To be honest, we have not yet listened to these sounds with human ears for long enough. We checked loudness, length and cut-offs by numbers, but whether the wooden button and the drum hide sound good needs more listening on real speakers and earphones. The music is a first version, and there is room left to polish it.

// You can tune a sound by numbers, but in the end you decide by ear.
