---
title: Three Difficulties, Held in Place by Numbers
description: How we simulate thousands of battles to keep Easy, Normal and Hard in their own win-rate ranges, and why the bot makes Hard look harder.
date: 2026-11-18
slug: three-difficulties-in-numbers
lang: en
---

Choose Easy and you expect to win most of the time. Choose Hard and you expect to be pushed. That sounds obvious, but it quietly breaks whenever someone changes a rule or a general. So we hold each difficulty in a range with tests. The game is still in development, and this is a note on how that works.

## What was already guarded

Before this, our tests covered how much a card or a famed general raises the win rate, and whether Easy gives every kingdom between 60 and 95 percent. What nothing covered was the absolute win rate of Normal and Hard, or the simple fact that Easy should beat Normal and Normal should beat Hard.

## How we measure

A bot plays each kingdom 200 times with a fixed set of random seeds, using the same rules as the app's start. The results are the same every time, and the whole run takes a few seconds. The averages over four kingdoms, measured on November 5:

| Map | Easy | Normal | Hard |
|---|---|---|---|
| Act 1 | 79.5% | 23.8% | 6.0% |
| Historical Act 1 | 77.5% | 30.5% | 7.9% |
| Han River | 72.3% | 45.4% | 4.4% |

Each test allows a band of about 10 points either side of the measurement. If a change pushes a result out of its band, the test fails.

## A few extra rules

- Between difficulties there must be a gap of more than 15 points.
- On Hard, no kingdom may exceed 25 percent.
- On Easy, no kingdom may drop below 55 percent.
- With the same seed, results must repeat exactly.

## Why Hard looks so low

The bot does not use diplomacy or spies, so it plays worse than a person. The low numbers for Normal and Hard are the bot's numbers, not a promise about human players. We checked that the guard actually works by deliberately breaking a range and watching the test fail.

## What it cannot tell us

A win rate does not say whether a game felt fair or fun. Those answers still come from playing by hand. If we ever move a range on purpose, we change the table at the top of the test file and the notes together.

// Numbers can keep a difficulty honest. They cannot make it fun.
