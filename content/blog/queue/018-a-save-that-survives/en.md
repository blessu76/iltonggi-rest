---
title: A Save File That Survives Being Broken
description: How Iltonggi protects your progress if a save file is cut off mid-write, and how we tested it without breaking a real phone.
date: 2026-11-15
slug: a-save-that-survives
lang: en
---

Nothing ruins a long game faster than opening it and finding your progress gone. A phone can run out of battery, or the app can be closed in the middle of writing a file, and then half a file is left on disk. We wanted Iltonggi to survive that. The game is still in development, and this is a note on how far the protection goes today.

## We already had most of it

When we sat down to add a safety net, we found that the main save already had one. We had forgotten. It works in four steps.

1. Write the new save to a temporary file first, then swap it in. A cut-off write leaves the old save untouched.
2. Keep one backup generation of the previous save.
3. When loading, check that the file reads correctly.
4. If it is broken, restore the backup. If the backup is broken too, start a fresh game instead of crashing.

The gap was that only the main save had it. Everything else, such as the three save slots, settings, the acts you have cleared, quests, the shop, owned items, and your nickname and records, was written plainly.

## Widening it, but not to everything

We turned the backup on for every file that would hurt to lose. We left it off for logs, tips, weather and history, because losing those costs you nothing that matters. Keeping the list short means fewer extra files on the phone and fewer things to reason about. File names and contents stayed the same, so existing saves keep working. The only addition is the backup copy.

## Testing without breaking a phone

You cannot ask a player to cut power in the middle of a write, so we reproduced four situations in tests, for each file that now has a backup:

- Broken text in the save: the backup is restored.
- An empty file: the backup is restored.
- Broken and no backup: the game starts fresh without crashing.
- Only a half-written temporary file: the previous save is still there.

## What we have not verified

These are tests on a computer. We have not yet deliberately corrupted a file on a real device and watched it recover, so that part is unverified. Also, when something other than the main save is restored, the player sees no message. It simply comes back quietly. We think that is right for settings, but we may revisit it.

// A good save system is one you only notice when it saves you.
