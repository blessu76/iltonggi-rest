---
title: Dari genderang hingga gayageum, kami membuat suaranya sendiri
description: Bagaimana 15 efek suara dan 4 musik Iltonggi disintesis dengan skrip tanpa audio luar, dan mengapa sebagian kami buat ulang.
date: 2026-11-07
slug: making-the-sounds
lang: id
translation_of: ko
---

Suara adalah bagian Iltonggi yang paling lama kami utak-atik. Gambar langsung terlihat, tetapi saat suara keliru, sulit mengatakan bagian mana yang keliru. Tulisan ini adalah catatan tentang cara suara dibuat dan mengapa sebagian kami buat ulang sekali.

## Tanpa audio luar

Gim ini kini memuat 19 suara: 15 efek dan 4 musik. Semuanya disintesis dari nol dengan skrip. Kami tidak memakai sampel unduhan maupun audio yang dibeli. Karena itu, menjalankan skrip yang sama lagi akan menghasilkan suara yang sama lagi. Bisa menjelaskan asal tiap suara adalah alasan utama kami memilih cara ini.

## Genderang, segel, bendera, dan tinta

Ada empat suara genderang untuk pertempuran dan pawai. Masing-masing berawal dari gelombang sinus yang nadanya menurun, dengan semburan derau singkat di atasnya untuk memberi kesan pukulan pada kulit. Nadanya dibedakan, kira-kira 55, 59, 65, dan 85 Hz.

Suara segel saat merebut tanah adalah nada rendah yang turun dari 94 Hz ke 39 Hz. Namun pengeras suara ponsel yang kecil nyaris tidak bisa menghasilkan nada serendah itu. Karena itu kami mencampurkan beberapa harmonik, supaya hentakannya masih terasa meski bagian terendahnya hilang.

Suara bendera, yang dipakai saat menang dan saat berganti giliran, hanya melewatkan derau pada satu pita sempit dan membuatnya bergetar cepat, seperti kain tertiup angin. Panjangnya 1,4 detik. Suara tinta yang dipakai dalam diplomasi menyebar pelan selama 2,2 detik dan paling pekat sekitar detik ke-1,3. Suara tombol menumpuk dua nada pendek 620 dan 1240 Hz dan lenyap dalam 0,15 detik, seperti tombol kayu.

## Suara yang kami buat ulang

Delapan dari efek pertama punya beberapa masalah, jadi kami membuatnya lagi.

- Ada puncak suara yang menyentuh batas atas. Sekarang semuanya berada setidaknya 1 dB di bawahnya, sehingga tidak ada ruang untuk pecah.
- Tiga genderang terpotong sebelum pukulan keduanya selesai. Sekarang setiap suara diredam dengan halus pada 5 ms pertama dan terakhirnya, sehingga tidak ada bunyi klik.
- Kerasnya suara berbeda-beda. Sekarang tingkat rata-rata kedelapannya sama dalam selisih 0,1 dB.

Saat membuat ulang, kami berusaha tidak mengubah watak suaranya. Nada genderang, bentuk turunnya segel, dan saat tinta paling pekat tetap dipertahankan.

## Musik

Musik dibangun di sekitar tiruan gayageum dan daegeum. Gayageum dibuat dengan menghitung senar yang dipetik (metode Karplus-Strong), dan daegeum dengan menumpuk harmonik serta mencampurkan derau napas. Ditambahkan sebuah genderang dan dengung rendah, dan nadanya berasal dari tangga nada lima nada dalam musik tradisional Korea. Ada satu lagu untuk menu, peta, pertempuran, dan kemenangan.

## Begini bunyinya di layar

- Saat huruf judul jatuh dengan hentakan, getaran menyertai suaranya.
- Video antarbabak berisi genderang, derap kuda, angin, guntur, dan segel.
- Suara tetap berbunyi meski sakelar senyap ponsel menyala, dan musik diputar di empat layar.
- Di pengaturan, efek dapat dimatikan atau dikecilkan.

## Yang belum kami lakukan

Jujur saja, kami belum mendengarkan suara-suara ini dengan telinga manusia cukup lama. Kami memeriksa kerasnya, panjangnya, dan terpotong tidaknya lewat angka, tetapi apakah tombol kayu dan kulit genderang terdengar enak masih perlu didengar lebih banyak lewat pengeras suara dan earphone sungguhan. Musiknya adalah versi pertama, dan masih ada ruang untuk disempurnakan.

// Suara bisa disetel dengan angka, tetapi akhirnya diputuskan dengan telinga.
