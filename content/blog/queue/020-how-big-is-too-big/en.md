---
title: How Big Is Too Big for a Phone Game?
description: Why we put a size budget on Iltonggi's art, sound and fonts, and the guard that fails the build when we go over.
date: 2026-11-17
slug: how-big-is-too-big
lang: en
---

A game that takes a long time to download, or a long time to show its first screen, loses people before they play. Iltonggi carries a lot: old-style fonts, paintings, music and sound effects, and text in eleven languages. If nobody watches, it only ever grows. So we set a budget, and made the computer enforce it. The game is still in development.

## What we measure

We count only the files the app actually bundles, not everything in the project. On November 5 the numbers were:

| Item | Measured | Limit |
|---|---|---|
| All bundled assets (74 files) | 9.83 MiB | 12,000,000 bytes |
| Largest single file (the serif font, compressed) | 1.29 MB | 1.5 MB |
| Audio | 4.27 MB | 5 MB |
| Photos (23) | 3.55 MB | 4.2 MB |
| Read before the first frame | 1.48 MB | 1.7 MB |

Every limit leaves roughly 15 to 18 percent of room. We also ban formats that should never ship, such as uncompressed audio and layered image files.

## A guard, not a promise

A rule that only lives in a document gets forgotten. So the size check runs inside the same gate as formatting, analysis and tests. If a limit is crossed, the build fails. Raising a limit is allowed, but only on purpose: you must change the number in the script and in the table together.

## The font that stayed out

The serif font is 3.18 MB as an original file, which is a lot for a phone. We ship it compressed at 1.29 MB, and the original stays in the repository only. If someone adds it to the app by mistake, the banned-format rule and the total both catch it.

## Start-up time

On a Mac, unpacking the font takes about 6 milliseconds, and loading the opening picture about 14. We did not set a time limit, because numbers from a Mac say little about a real phone on a cold start.

## Not yet known

We do not yet know the final size of the installable package, since compression, code and the engine are added only when you build. We plan to record that number next to this table once we have it.

// A budget works because it can say no.
