---
title: Melanjutkan Permainan di Perangkat Lain
description: Cara Iltonggi memungkinkan permainan dilanjutkan di antara perangkat Apple, dan aturan yang kami pilih saat dua perangkat berbeda isinya.
date: 2026-11-16
copy_review: iris 2026-11-14
slug: continuing-on-another-device
lang: id
translation_of: ko
---

Permintaan awalnya sederhana: jika bermain di satu perangkat Apple, kita harus bisa melanjutkan di perangkat lain dengan akun yang sama. Kedengarannya kecil, tetapi yang sulit bukan menyalin simpanan. Yang sulit adalah menentukan apa yang terjadi saat dua perangkat memiliki versi berbeda. Catatan ini tentang aturan yang kami tetapkan. Gim ini masih dalam pengembangan.

## Perangkat adalah sumber kebenaran

Setiap perangkat menyimpan berkasnya sendiri sebagai simpanan yang sebenarnya. iCloud hanya menyimpan salinan, bukan aslinya. Jika iCloud mati, Anda keluar akun, atau memakai Android, gim tetap berjalan di perangkat itu saja tanpa pesan galat. Simpanan utama, tiga slot simpanan, dan pengaturan ikut serta.

## Perbandingan tiga arah

Untuk memutuskan tindakan, setiap perangkat mengingat sidik jari dari versi terakhir yang cocok dengan awan. Lalu ia membandingkan:

- Hanya perangkat ini yang berubah: unggah.
- Hanya awan yang berubah: unduh.
- Keduanya berubah: pilih menurut aturan.

## Saat keduanya berubah

Urutan yang kami pilih:

1. Simpanan yang berisi mengalahkan yang kosong.
2. Jika waktu simpan berbeda lebih dari dua menit, yang lebih baru menang.
3. Jika selisihnya dalam dua menit dan permainannya sama, yang gilirannya lebih banyak menang.
4. Selain itu, yang ada di perangkat ini.

Kami sempat berdebat. "Kemajuan terjauh menang" lebih mudah dijelaskan, tetapi kami merasa "yang terakhir disimpan" lebih sesuai dengan maksud pemain. Salinan yang kalah tidak dihapus, melainkan disimpan terpisah sebagai salinan konflik.

## Digabung, bukan dipilih

Ada hal yang tidak boleh hilang karena lempar koin. Babak yang sudah tamat, kisah babak yang sudah dilihat, dan barang yang Anda miliki digabung sebagai gabungan, bukan diambil dari satu sisi.

## Batas ukuran

Satu teks yang lebih dari 200.000 karakter tidak diunggah dan tetap di perangkat. Pengujian mencakup batas ini.

## Menyadari perubahan saat bermain

Awalnya gim hanya membaca ulang awan ketika Anda kembali ke aplikasi. Pada build berikutnya, gim juga menyadari perubahan dari perangkat lain saat sedang tampil di depan, dan layar pengaturan kini menunjukkan apakah sinkronisasi iCloud aktif.

## Belum terverifikasi

Semua ini diuji di komputer. Kami belum melihat dua perangkat sungguhan dengan satu akun saling mengoper permainan, jadi bagian itu belum terverifikasi. Gambar para jenderal dan kemajuan misi sengaja tetap di tiap perangkat.

// Sinkronisasi itu mudah. Menentukan siapa yang benar, itulah pekerjaannya.
