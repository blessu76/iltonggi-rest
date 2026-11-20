---
title: Six New Towns and a Harder Normal Game
description: Six neutral towns in Act 3 pushed Normal win rates down to 14 percent. We changed only their troops, and this is how we picked the numbers.
slug: six-new-towns-and-normal-odds
lang: en
copy_review: iris 2026-11-16
date: 2026-11-20
published: 2026-11-20T12:45:00+09:00
---

When we add a place to the map, we also add a fight there. In Act 3 we added six neutral towns, and the Normal difficulty dropped sharply. Before the change, a unified kingdom won about 36 percent of simulated games on Normal. After it, the number fell to 14. This post is about how we brought it back into the target range, and what the numbers can and cannot tell us. The game is still in development.

## The problem

Neutral towns start with a few troops and can be taken by any side. Six more of them meant six more targets, and the simulated AI could grow faster too. The win rates moved away from the bands we had set for Easy, Normal and Hard.

## How we tested it

We ran 200 simulated games per difficulty with fixed random seeds, so the same run gives the same result. We also ran games where only the AI plays, to check that no single side takes over the map. The gate tests keep Easy high, Normal in the middle, Hard low, and the AI-only games balanced. We then repeated the check on a second set of seeds, so one lucky set would not decide the outcome.

## What we tried

First we set all six new towns to four or five troops. That raised the Normal win rate a little, but in AI-only games one side won 78 out of 100, which broke the limit of 75. We also tried lowering the five older neutral towns. It did not help, because the rivals grew just as easily. In the end we changed only the six new towns, and only by one troop each.

## What we chose

Two towns got five troops, and four got four. On the first seed set, Normal settled at 19.5 percent. On the second, it was 20.5 percent. Easy eased from 94.5 to 91.5 percent, which moves it away from the 98 ceiling and leaves room for a player who makes a mistake. Hard stayed near the bottom of its band.

## Read the numbers as a trend

One troop changed the result more than we expected. In one comparison, swapping the troop counts of two towns moved Normal from 13.5 to 19.5 percent. So we read these figures as the direction of a change, not as exact facts. Simulated players are not people, and no human has yet played this map to test how it feels [unverified].

## Finally

Adding a place to a map is a small act, but it changes what the player has to do. These numbers are a guide. The test that matters is whether the game is fun to play at Normal.
