---
title: Keeping Direct Command From Becoming a Cheat: Balancing It by Computer
description: How we keep Direct Command in Iltonggi from becoming a cheat by balancing it with simulated battles, why its rules stay simple, and what is still left to do.
date: 2026-11-02
slug: direct-command-in-battle
lang: en
---

Battles in Iltonggi are automatic by default, so on busy days you can just look at the result. But from the start we also wanted a way to take charge and direct the fight yourself, so we added Direct Command to the window before an attack. It took its first shape in build 33 on October 29. For now it works only when you attack. Direct Command for defense isn't built yet.

## Rock-paper-scissors in three beats

Direct Command lets you pick one of three stances over three beats: formation, charge, or flank. Formation beats charge, charge beats flank, and flank beats formation. If you send out scouts, you can catch a glimpse of what the enemy will play, and enemies inside a castle often choose formation. If you're being pushed back, you can retreat and save half your troops.

We kept the rules as simple as rock-paper-scissors. In a round of 5 to 10 minutes, having to learn long rules would turn Direct Command into a burden. Instead we added clues, such as scouts and the habits of defenders in a castle, to give it the pleasure of reading your opponent. Just as spies let you peek at land in the fog, scouts let you peek at the enemy's move. The idea that gathering information is power carries over into battle too. We added retreat for the same reason. Holding out until you lose everything is worse than saving half to try again, and a commander needs that option to feel like one.

## It must not become a cheat

If Direct Command is too strong, everyone ends up using it, and the light, quick nature of a round breaks down. If it's too weak, nobody uses it. If it can turn a heavily lopsided fight around, it's not command but a cheat. Generals' abilities, troop strength and weather are calculated exactly as in automatic battles, and we decided to keep the gain from command small. Someone who reads well should have a slight edge, but a side badly short on troops must never win on command alone.

## Compare with everything else held equal

To see only the effect of command, every other condition has to be identical. So we pitted the same generals, the same troops and the same weather against each other, changing only the way of command, and compared win rates. Automatic battle is the baseline, and we look at how far Direct Command strays from it. If the gap is too large or too small, we rework the rules.

## 6,000 fights by computer

According to our development records, to check this we had the computer fight 6,000 battles commanded in various ways. Choosing at random, or repeating a single order, kept the win rate within 1 percentage point of automatic battle. Reading the scout report and responding raised wins by about 3 percentage points, and the records show no case of turning a badly lopsided fight around.

A person can't play 6,000 battles by hand, so this kind of checking is left to the computer. This time too, we built the engine and simulation tests first and attached the screen afterward. It's a sequence of balancing with numbers first, then dressing it in something you can touch. The screen and the text in eleven languages came after that.

This isn't the first time we've balanced by computer. According to our development records, in the preceding build 32 we measured the same way how win rates varied widely between kingdoms on Easy difficulty, and narrowed them. The thinking was that whichever kingdom you pick, Easy should be equally Easy.

## What remains after the numbers

Good numbers don't guarantee good feel. A computer can measure win rates, but it can't tell you whether command is fun. So we keep refining it by playing by hand. Direct Command on defense, and a check across a whole playthrough, are still ahead of us.

// Read well and you get a slight edge. Cheats don't work here.
