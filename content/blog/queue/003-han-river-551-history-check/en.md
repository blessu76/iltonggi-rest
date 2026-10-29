---
title: The 551 Han River Contest: Unnamed Generals Become "General ○○"
description: Building Iltonggi's 551 Han River scenario: dropping out-of-era generals, placing Kim Mu-ryeok and the Daegaya king, and why unknown names stay "General ○○."
date: 2026-11-01
slug: han-river-551-history-check
lang: en
---

A new scenario set in the year 551 is in the works for Iltonggi. It is the year Baekje and Silla joined hands to go after the Han River basin held by Goguryeo. The scenario took shape over three builds on October 29. In the first build, you could pick a new scenario starting in 551. In the next, a victory condition was added, and in the last, historical checks on its people arrived. One of the biggest jobs in making the scenario was fitting people to the era.

## The skeleton of the scenario

In the new scenario, towns in the Han River basin, such as Hanseong, Michuhol and Gukwonseong, become the battleground. Seize these three towns and hold them for three rounds in a row to win. Goguryeo, which holds the land at the start, wins by holding on to the end. It uses the same mechanism as the original scenarios, with the goal changed to suit the story. We also gave the computer-run kingdoms weights so they move toward this goal, and according to our development records, when we ran simulations, more games ended with the goal being contested.

The scenario-select screen also has a slot that shows, in one line, the people who appear in it. Knowing in advance who shows up in an unfamiliar year makes a strange era feel less daunting. To fill that line, each person's era and allegiance had to be settled, and that is how historical checking moved to the heart of scenario-making.

## Why spend time on accuracy

It's a game, so some things inevitably change for the sake of fun. But if we use names from real history and mix them up carelessly, we end up teaching something wrong to someone meeting those names for the first time. So we decided to keep what we changed and what we don't know clearly separate. What follows is a record of drawing those lines one by one.

## People who weren't there that year

At first we brought over the generals from the original scenario unchanged. But Eulji Mundeok belongs to 612, Gyebaek to 660, and Sadaham's name appears in the 562 campaign against Daegaya. They don't fit a 551 scenario, so we removed every general who doesn't belong to the era. Removing them in words alone wasn't enough, so we also added an automated test that checks whether every person in a scenario lies within its era. If someone carelessly slips in a general from another time later on, it will be caught before the build is made.

## Which side was Kim Mu-ryeok on?

Kim Mu-ryeok was a son of King Guhyeong, the last king of Geumgwan Gaya. But after Geumgwan Gaya surrendered to Silla in 532, he served as a Silla general, and after the Sinju province was established, his name appears as its governor. Going by bloodline alone, you'd want to put him on the Gaya side, but in 551 the place where he stood was Silla. So we placed him with Silla, not Gaya.

## The Gaya king we left unnamed

Whether Doseolji, known as the last king of Daegaya, was king in 551 is uncertain. A recent theory holds that he was the same person as a Silla nobleman of that name, in which case he may have been in Silla at the time. Where views are divided, we didn't want to assert anything, so we wrote only the title "Daegaya king." Writing a name would look more plausible, but we felt plausible and accurate are different things.

## "General ○○"

Some people have names that survive in the sources, but not every post is like that. For some Baekje generals we couldn't confirm a name in the sources, and instead of forcing one in, we left them as "General ○○." Where records disagree, we write "according to one theory." We attached short biographies to the people who appear in a scenario, and wrote those under the same principle.

We haven't yet cross-checked everything against the original text of the Samguk Sagi, and we plan to fix any mistakes we find.

// Writing "we don't know" when you don't know is also historical accuracy.
