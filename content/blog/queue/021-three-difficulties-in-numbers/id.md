---
title: Tiga Tingkat Kesulitan yang Dijaga Angka
description: Cara kami mensimulasikan ribuan pertempuran agar Mudah, Normal, dan Sulit tetap di rentang kemenangan masing-masing, dan mengapa bot membuat Sulit tampak lebih berat.
date: 2026-11-18
copy_review: iris 2026-11-14
slug: three-difficulties-in-numbers
lang: id
translation_of: ko
---

Jika memilih Mudah, Anda berharap menang hampir selalu. Jika memilih Sulit, Anda berharap terdesak. Kedengarannya jelas, tetapi diam-diam bergeser setiap kali ada yang mengubah aturan atau seorang jenderal. Karena itu kami menjaga tiap tingkat kesulitan dalam sebuah rentang dengan pengujian. Gim ini masih dalam pengembangan, dan catatan ini menjelaskan cara kerjanya.

## Yang sudah dijaga

Sebelumnya, pengujian kami mencakup seberapa besar sebuah kartu atau jenderal ternama menaikkan angka kemenangan, dan apakah Mudah memberi setiap kerajaan antara 60 dan 95 persen. Yang tak tercakup adalah angka kemenangan mutlak Normal dan Sulit, serta fakta sederhana bahwa Mudah harus lebih mudah daripada Normal, dan Normal lebih mudah daripada Sulit.

## Cara mengukur

Sebuah bot memainkan setiap kerajaan 200 kali dengan kumpulan bibit acak yang tetap, memakai aturan yang sama dengan awal aplikasi. Hasilnya sama setiap kali, dan seluruh proses selesai dalam beberapa detik. Rata-rata empat kerajaan, diukur pada 5 November:

| Peta | Mudah | Normal | Sulit |
|---|---|---|---|
| Babak 1 | 79,5% | 23,8% | 6,0% |
| Babak 1 sejarah | 77,5% | 30,5% | 7,9% |
| Sungai Han | 72,3% | 45,4% | 4,4% |

Setiap pengujian mengizinkan sekitar 10 poin di kedua sisi dari hasil pengukuran. Jika sebuah perubahan mendorong hasil keluar dari rentangnya, pengujian gagal.

## Beberapa aturan tambahan

- Antar tingkat kesulitan harus ada selisih lebih dari 15 poin.
- Pada Sulit, tak ada kerajaan yang boleh melebihi 25 persen.
- Pada Mudah, tak ada kerajaan yang boleh turun di bawah 55 persen.
- Dengan bibit yang sama, hasil harus berulang persis.

## Mengapa Sulit tampak begitu rendah

Bot tidak memakai diplomasi atau mata-mata, sehingga bermain lebih lemah daripada manusia. Angka rendah untuk Normal dan Sulit adalah angka bot, bukan janji bagi pemain manusia. Kami memastikan penjaga ini bekerja dengan sengaja menggeser sebuah rentang dan melihat pengujian gagal.

## Yang tak bisa dikatakannya

Angka kemenangan tidak menunjukkan apakah sebuah permainan terasa adil atau seru. Jawaban itu tetap datang dari bermain dengan tangan sendiri. Jika suatu saat kami menggeser rentang dengan sengaja, kami mengubah tabel di awal berkas pengujian dan catatannya bersama-sama.

// Angka bisa menjaga kejujuran tingkat kesulitan. Angka tidak bisa membuatnya seru.
