---
title: One Thumb, One Region: Designing Touch Controls for a Map Game
description: A land-grab map has to work with one thumb on a small screen. Here is how we think about taps, drags and the mistakes we are guarding against.
slug: one-thumb-touch-controls
lang: en
copy_review: iris 2026-11-19
date: 2026-11-22
published: 2026-11-22T16:00:00+09:00
---

Iltonggi is a map game, and a map game on a phone asks a lot of one thumb. You need to pick a region, see its troops, move an army and read the result, all without covering the very region you are trying to press. This post describes how we think about touch input. The game is still in development, so read these as the rules we are testing, not a finished manual.

## Tap and drag are different things

The most common mistake in a map game is to treat every touch as a click. A finger that moves a little while the map slides under it is not a selection. So we separate two intents: a short tap, which selects, and a longer movement, which pans the map. If the finger travels beyond a small distance before it lifts, the touch belongs to the map, and no region is chosen.

The exact distance matters less than the principle. A player should never select a region by accident while scrolling across a crowded part of the map.

## Regions are small on a phone

Some regions are narrow, and a thumb is wide. When nothing else is nearby, we let a region's tap area reach a little beyond its drawn border. We never let that area grow so far that it steals a tap meant for a neighbor. When two regions are close, the choice should come from where the touch lands, not from which region happens to be drawn last.

## Confirm the costly moves

Attacking or moving troops changes the state of the game, so it should be harder to do by accident than looking at a region. A tap shows what would happen, and a second, deliberate action commits it. This costs a little speed, and a player who knows the map may find it slower. We accept that trade, because a misplaced army is more annoying than one extra tap.

## Short sessions, interrupted often

People play Iltonggi in short sessions: on a bus, in a queue, for a few minutes before bed. An interruption can come at any moment, such as a phone call or a switch to another app. So the controls must not depend on a gesture that stays in progress for long. A half-finished drag should simply end without a result, and the map should stay where the player left it.

## What we still need to check

Thumb sizes vary, and so do phone screens. Our assumptions come mostly from the devices we own. We plan to test the tap areas on more screens and to watch where players tap by mistake. We have not yet measured this at scale, so this post gives no numbers.

// The safest tap is the one you can take back.
