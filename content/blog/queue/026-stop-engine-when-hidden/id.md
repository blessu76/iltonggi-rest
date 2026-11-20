---
title: Hentikan mesin saat tidak ada yang melihat
description: Saat layar tertutup atau aplikasi berpindah ke latar belakang, mesin permainan berhenti. Ini aturan yang kami tetapkan saat memindahkan permainan ke kit mesin bersama, dan hal yang belum kami ukur.
slug: stop-engine-when-hidden
lang: id
translation_of: en
date: 2026-11-23
---

Adegan peta dan pertempuran di Iltonggi adalah gambar yang bergerak. Prajurit berjalan, panji berkibar, dan pertempuran berlangsung bingkai demi bingkai. Namun ketika pemain menerima telepon atau berpindah ke aplikasi lain, tidak ada alasan untuk terus menggambar sesuatu yang tidak bisa dilihat siapa pun. Tulisan ini mencatat aturan yang kami tetapkan hari ini, saat memindahkan mesin permainan ke kit bersama. Permainan ini masih dalam pengembangan.

## Berhenti saat tidak ada yang bisa dilihat

Ketika layar tertutup, atau aplikasi masuk ke latar belakang, mesin berhenti. Menggambar adegan yang tidak bisa dilihat siapa pun hanya menghabiskan baterai. Saat pemain kembali, penggambaran dilanjutkan dari tempat tadi berhenti. Peta yang ditinggalkan pemain harus tetap sama, jadi kami tidak membiarkan waktu permainan berjalan diam-diam saat aplikasi tersembunyi.

## Satu tempat yang memutuskan kapan berhenti

Dulu, setiap adegan punya kode berhenti sendiri. Peta, panggung pertempuran, dan tampilan dunia masing-masing memeriksa apakah mereka tersembunyi, dan masing-masing harus diperbaiki sendiri. Sekarang tugas itu dipegang oleh satu cangkang bersama. Adegan tidak lagi bertanya apakah mereka terlihat. Mereka mengikuti keadaan yang ditetapkan cangkang.

## Animasi pertempuran tetap berjalan

Saat dua pasukan bertemu di peta, animasinya hanya bergerak selama mesin berjalan. Jadi selama bentrokan, mesin yang berhenti dinyalakan untuk saat itu dan dimatikan lagi ketika bentrokan selesai. Kecepatan dan urutan animasi tidak berubah. Kami juga menutup satu celah: jika bentrokan selesai saat layar tertutup, mesin tidak lagi mulai sendiri ketika layar kembali.

## Yang belum kami ukur

Kami belum mengukur seberapa banyak baterai yang dihemat. Beberapa hal hanya bisa diperiksa di perangkat sungguhan: membawa aplikasi ke latar belakang lalu membukanya lagi, berpindah antara peta dan tampilan dunia, batas 30 bingkai per detik, dan berapa lama penggambaran memakan waktu di GPU. Sampai kami mengukurnya, tulisan ini tidak memuat angka baterai.

// Gambar yang tidak dilihat siapa pun adalah yang paling murah untuk dilewati.
