---
title: Two Name Tags on the Map: Ink for Ours, Paper for the Rest
description: We cut the village name tags on the map from four looks to two. Our villages get ink-dark tags with gold troop numbers, and the others get paper tags with ink lettering.
slug: two-name-tags-on-the-map
lang: en
date: 2026-11-24
published: 2026-11-24T12:15:00+09:00
---

Each village on the Iltonggi map carries a name tag. The name tells a player where they are, and the troop number tells them what the board says. For a while, the tags came in too many styles, and the map felt noisy. This post records how we reduced them to two looks and the principles behind the change.

## Four looks were too many

The tags used four styles: a purple-edged pill, a white pill, white outlined lettering, and a round question mark for fog. Each looked acceptable alone. On a map with dozens of villages, though, none of them clearly mattered more than the others, because every tag claimed its own color.

## Our villages: ink tags with gold numbers

A village the player rules gets a dark ink tag. Its name is in cream and its troop count is in gold. Our own land is the first thing a player should find on the map, so it gets the strongest contrast. Gold appears only on the number, nowhere else on the tag.

## Other villages: paper tags with ink lettering

Villages held by other kingdoms get a hanji-colored tag with ink-colored lettering. The kingdom is no longer shown by the tag's color. A small dot at the left edge of the tag carries the kingdom color instead, so a map with many kingdoms does not become a clash of colors.

## Fog: softer, and without white outlines

Villages the player cannot see yet get a faded paper tag with faded ink. The fog mark is now a hanji-colored circle with an ink question mark. We also removed all white-outlined lettering. A test checks that the lettering keeps a contrast ratio of at least 4.5 to 1 against its background.

## Attack and move ranges

The colors for attack and move ranges were treated the same way. We removed loose color values that had been written into individual screens, and they now come from the shared design tokens. The attack color became slightly deeper.

## What is still open

We have not yet confirmed the new tags on recent device captures. Whether they stay comfortable to read in a long session needs real play on real devices, and we have not done that yet.

// A name tag should be easy to read, and it should never try to be the first thing you see.
