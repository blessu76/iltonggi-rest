---
title: Stop the Engine When No One Is Looking
description: When the screen is covered or the app goes to the background, the game engine stops. Here is the rule we set while moving to a shared engine kit, and what we have not measured yet.
slug: stop-engine-when-hidden
lang: en
date: 2026-11-23
published: 2026-11-23T14:00:00+09:00
---

Iltonggi's map and battle scenes are moving pictures. Soldiers walk, banners sway, and clashes play out one frame at a time. But when a player takes a phone call or switches to another app, there is no reason to keep drawing pictures no one can see. This post records the rule we set today, while moving the game engine onto a shared kit. The game is still in development.

## Stop when nothing can be seen

When the screen is covered, or the app goes to the background, the engine stops. Drawing a scene nobody can see only spends the battery. When the player returns, drawing resumes where it stopped. The map a player left must still be the same map, so we do not let game time run quietly while the app is hidden.

## One place decides when to stop

Earlier, each scene had its own code for stopping. The map, the battle stage and the first menu screen each checked whether they were hidden, and each one had to be fixed on its own. We moved that job into one shared shell. The scenes no longer ask whether they are visible. They follow the state the shell sets.

## The clash animation keeps going

When two armies clash on the map, the animation moves only while the engine is running. So during a clash, the stopped engine is switched on for that moment and switched off again when it ends. The speed and order of the animation have not changed. We also closed one gap: if a clash ends while the screen is covered, the engine no longer starts again by itself when the screen comes back.

## What we have not measured

We have not yet measured how much battery this saves. Some things can only be checked on real devices: sending the app to the background and back, moving between the map and other screens, the cap of 30 frames per second, and how long drawing takes on the GPU. Until we measure those, this post gives no battery numbers.

// The picture nobody sees is the cheapest one to skip.
