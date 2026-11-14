---
title: Sebesar Apa yang Terlalu Besar untuk Gim Ponsel?
description: Mengapa kami menetapkan anggaran ukuran untuk gambar, suara, dan huruf Iltonggi, serta penjaga yang menggagalkan build jika terlampaui.
date: 2026-11-17
copy_review: iris 2026-11-14
slug: how-big-is-too-big
lang: id
translation_of: ko
---

Gim yang lama diunduh, atau lama menampilkan layar pertamanya, kehilangan orang sebelum mereka bermain. Iltonggi memuat banyak hal: huruf bergaya kuno, lukisan, musik dan efek suara, serta teks dalam banyak bahasa. Jika tak ada yang mengawasi, ia hanya akan membesar. Maka kami menetapkan anggaran dan menyerahkan penegakannya kepada komputer. Gim ini masih dalam pengembangan.

## Apa yang kami ukur

Kami hanya menghitung berkas yang benar-benar dikemas dalam aplikasi, bukan semua isi proyek. Per 5 November, angkanya sebagai berikut:

| Butir | Terukur | Batas |
|---|---|---|
| Semua berkas yang dikemas (74) | 9,83 MiB | 12.000.000 bita |
| Berkas terbesar (huruf serif, terkompresi) | 1,29 MB | 1,5 MB |
| Audio | 4,27 MB | 5 MB |
| Foto (23) | 3,55 MB | 4,2 MB |
| Dibaca sebelum bingkai pertama | 1,48 MB | 1,7 MB |

Setiap batas menyisakan ruang sekitar 13 sampai 16 persen. Kami juga melarang format yang tak boleh dikirim, seperti audio tanpa kompresi dan berkas gambar berlapis.

## Penjaga, bukan janji

Aturan yang hanya hidup di dokumen akan terlupakan. Karena itu pemeriksaan ukuran berjalan di gerbang yang sama dengan pemformatan, analisis, dan pengujian. Jika batas terlampaui, build gagal. Menaikkan batas boleh, tetapi hanya dengan sengaja: angka di skrip dan di tabel harus diubah bersama.

## Huruf yang dibiarkan di luar

Huruf serif berukuran 3,18 MB sebagai berkas asli, yang besar untuk ponsel. Kami mengemasnya terkompresi 1,29 MB, dan aslinya hanya ada di repositori. Jika seseorang tak sengaja menambahkannya ke aplikasi, aturan format terlarang dan batas total akan menangkapnya.

## Waktu mulai

Di Mac, membuka kompresi huruf butuh sekitar 6 milidetik, dan memuat gambar pembuka sekitar 14. Kami tidak menetapkan batas waktu, karena angka dari Mac sedikit bicara tentang ponsel sungguhan saat dijalankan dingin.

## Belum diketahui

Kami belum tahu ukuran akhir paket yang dipasang, karena kompresi, kode, dan mesin baru ditambahkan saat build. Kami berencana mencatat angka itu di samping tabel ini setelah kami memilikinya.

// Anggaran berdaya karena ia bisa berkata tidak.
