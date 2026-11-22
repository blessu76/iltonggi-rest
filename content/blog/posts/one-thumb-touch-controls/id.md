---
title: Satu jempol, satu wilayah: merancang kontrol sentuh untuk game peta
description: Game perebutan wilayah harus bisa dimainkan dengan satu jempol di layar kecil. Inilah cara kami memikirkan ketukan, geseran, dan kesalahan yang ingin kami cegah.
slug: one-thumb-touch-controls
lang: id
translation_of: en
copy_review: iris 2026-11-19
date: 2026-11-22
published: 2026-11-22T16:00:00+09:00
---

Iltonggi adalah game peta, dan game peta di ponsel membebani satu jempol dengan banyak tugas. Anda harus memilih sebuah wilayah, melihat pasukannya, menggerakkan pasukan, dan membaca hasilnya, tanpa menutupi wilayah yang ingin ditekan. Tulisan ini menjelaskan cara kami memikirkan masukan sentuh. Game ini masih dalam pengembangan, jadi bacalah aturan ini sebagai hal yang sedang kami uji, bukan panduan yang sudah final.

## Ketuk dan geser adalah dua hal berbeda

Kesalahan paling umum dalam game peta adalah memperlakukan setiap sentuhan sebagai klik. Jari yang sedikit bergerak sementara peta bergeser di bawahnya bukanlah pilihan. Karena itu kami memisahkan dua maksud: ketukan singkat, yang memilih, dan gerakan lebih panjang, yang menggeser peta. Jika jari bergerak melewati jarak kecil sebelum diangkat, sentuhan itu milik peta dan tidak ada wilayah yang dipilih.

Prinsipnya lebih penting daripada jarak yang tepat. Pemain tidak boleh memilih wilayah secara tidak sengaja ketika sedang menggulir melewati bagian peta yang padat.

## Wilayah terasa kecil di ponsel

Ada wilayah yang sempit, sementara jempol itu lebar. Ketika tidak ada wilayah lain di dekatnya, kami membiarkan area ketuk sebuah wilayah sedikit melampaui garis batasnya. Namun area itu tidak pernah dibuat sebesar itu hingga mencuri ketukan yang seharusnya untuk tetangganya. Jika dua wilayah berdekatan, pilihannya harus ditentukan oleh tempat sentuhan mendarat, bukan oleh wilayah mana yang digambar terakhir.

## Konfirmasi langkah yang mahal

Menyerang atau memindahkan pasukan mengubah keadaan permainan, jadi melakukannya tanpa sengaja harus lebih sulit daripada sekadar melihat sebuah wilayah. Satu ketukan menunjukkan apa yang akan terjadi, dan satu tindakan kedua yang disengaja akan mengeksekusinya. Ini membuat sedikit lebih lambat, dan pemain yang sudah hafal peta mungkin merasakannya. Kami menerima pertukaran ini, karena pasukan yang salah kirim lebih mengganggu daripada satu ketukan tambahan.

## Sesi pendek, sering terputus

Orang memainkan Iltonggi dalam sesi singkat: di bus, saat antre, beberapa menit sebelum tidur. Gangguan bisa datang kapan saja, misalnya telepon masuk atau pindah ke aplikasi lain. Maka kontrol tidak boleh bergantung pada gerakan yang lama berlangsung. Geseran yang belum selesai harus berakhir begitu saja tanpa hasil, dan peta tetap berada di tempat yang ditinggalkan pemain.

## Yang masih perlu kami periksa

Ukuran jempol berbeda-beda, dan layar ponsel juga. Asumsi kami sebagian besar berasal dari perangkat yang kami miliki. Kami berencana menguji area ketuk di lebih banyak layar dan memperhatikan di mana pemain salah menekan. Kami belum mengukurnya dalam skala besar, jadi tulisan ini tidak memuat angka.

// Ketukan paling aman adalah ketukan yang bisa dibatalkan.
