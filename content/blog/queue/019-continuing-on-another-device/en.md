---
title: Picking Up Where You Left Off on Another Device
description: How Iltonggi lets you continue a game across Apple devices, and the rules we chose for when two devices disagree.
date: 2026-11-16
slug: continuing-on-another-device
lang: en
---

Early on, the request was simple: if you play on one Apple device, you should be able to continue on another with the same account. It sounds small, but the hard part is not copying a save. It is deciding what happens when two devices have different versions of it. This is a note on the rules we settled on. The game is still in development.

## The phone is the source of truth

Each device keeps its own file as the real save. iCloud holds a copy, not the master. If iCloud is off, you are signed out, or you are on Android, the game simply stays on that one device without any error. The main save, the three save slots and the settings all take part.

## Three-way comparison

To decide what to do, each device remembers a fingerprint of the last version that matched the cloud. Then it compares:

- Only this device changed: send it up.
- Only the cloud changed: take it down.
- Both changed: pick one by rule.

## When both changed

The order we chose is below.

1. A non-empty save beats an empty one.
2. If the save times differ by more than two minutes, the later one wins.
3. If they are within two minutes and it is the same game, the one with more turns wins.
4. Otherwise, the one on this device.

We argued about this. A simple "furthest progress wins" would have been easier to explain, but we felt that "the one you saved last" matches what a player means. Whichever copy loses is kept aside as a conflict copy instead of being deleted.

## Merge, don't choose

Some things should never be lost to a coin flip. Which acts you have cleared, which act stories you have seen, and what you own are merged as a union rather than picked from one side.

## A size limit

A single piece of text over 200,000 characters is not sent up and stays on the device. Test cases cover this limit.

## Noticing a change while you play

At first the game only re-read the cloud when you came back to the app. In build 85 it also notices a change made on another device while it is in front of you, and the settings screen now shows whether iCloud sync is on.

## Not yet verified

All of this is tested on a computer. We have not yet watched two real devices on one account hand a game back and forth, so that part is unverified. Pictures of generals and your quest progress stay on each device by design.

// Syncing is easy. Deciding who is right is the work.
