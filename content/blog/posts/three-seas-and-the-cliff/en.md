---
title: Three Seas, and the Cliff We Found by Simulation
description: Acts 4 to 6 in Iltonggi, and what two hundred simulated games per difficulty taught us about balance.
slug: three-seas-and-the-cliff
lang: en
date: 2026-11-09
published: 2026-11-09T12:00:00+09:00
---

Acts 4, 5 and 6 take the land grab out to sea and across the old trade roads. This post tours the three, and then tells a story from the balancing work that surprised us. The numbers are from development and may change, and they are shared as a look behind the screen rather than as a promise about how any game will go.

## 1. Act 4, the Treasure Fleet of the Southern Seas

Act 4 follows a sea road that runs south from the Chinese coast through port after port, and its map grew from 25 to 38 regions. The sea route matters more than any single town. A handful of harbors along that road decide who can move quickly and who cannot, and the neutral towns around them are worth reading before you commit.

## 2. Act 5, the Stargazer of the Silk Road

Act 5 has five nations and 24 regions, and its goal is to hold the western end of the map, Constantinople, through a round. Your kingdom is placed as if it had risen in the Fergana valley and set off westward. That is an adaptation of ours, not history, and we try to say so wherever it applies. The road west passes through the lands of Timur and the Black Sheep, so even on the easy setting it was designed to be roughly an even contest.

## 3. Act 6, the Sea of the Renaissance

Act 6 has five powers, among them the Habsburgs, Castile, France and Venice, on a map of 24 regions. Its goal is Florence, which is a neutral town: you can raise a flag there, or finish first in territory, or unify. A few of the people in this act are placed into the story as our own adaptation, and our notes mark them as such.

## 4. How we balance: simulate, then look for cliffs

Before an act is shown, we play it by machine. For each difficulty we run two hundred games with different random seeds and watch how often the United Kingdom wins. We also let the computer kingdoms fight each other for a hundred games to see that no single one runs away with every game, and that unification does not happen too often.

## 5. The cliff

This is the part that surprised us. In Act 5 we adjusted the defense bonus of the strong kingdom guarding the road west, a little at a time. Win rates drifted down smoothly, until one more small step made the player's win rate fall to nearly zero. In Act 4 it was a single soldier: take one troop away from a key harbor on the sea road and the normal-difficulty win rate jumped from under ten percent to more than fifty. In Act 6 it was the same shape again.

A balance that swings that hard on one number is not a good game, so we stopped short of those edges and picked values on the safe side of them. It also taught us not to trust a single playtest.

## Finally

Simulation cannot tell you whether a game is fun, only whether it is broken. The fun part still needs people, and that is where your play and your impressions will count most.

// A good game leans without tipping over.
