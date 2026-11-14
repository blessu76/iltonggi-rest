---
title: Bir Mobil Oyun İçin Ne Kadar Büyük Çok Büyüktür?
description: Iltonggi'nin görsellerine, sesine ve yazı tiplerine neden bir boyut bütçesi koyduk ve sınırı aştığımızda derlemeyi başarısız kılan koruma.
date: 2026-11-17
slug: how-big-is-too-big
lang: tr
---

İndirmesi uzun süren ya da ilk ekranı geç gösteren bir oyun, oynanmadan insanları kaybeder. Iltonggi'de çok şey var: eski usul yazı tipleri, resimler, müzik ve ses efektleri ve on bir dilde metin. Kimse bakmazsa yalnızca büyür. Bu yüzden bir bütçe koyduk ve bilgisayarın bunu uygulatmasını sağladık. Oyun hâlâ geliştirme aşamasında.

## Neyi ölçüyoruz

Projedeki her şeyi değil, yalnızca uygulamanın gerçekten pakete kattığı dosyaları sayıyoruz. 5 Kasım'daki rakamlar şöyleydi:

| Kalem | Ölçülen | Sınır |
|---|---|---|
| Pakete giren tüm varlıklar (74 dosya) | 9,83 MiB | 12.000.000 bayt |
| En büyük tek dosya (serif yazı tipi, sıkıştırılmış) | 1,29 MB | 1,5 MB |
| Ses | 4,27 MB | 5 MB |
| Fotoğraflar (23) | 3,55 MB | 4,2 MB |
| İlk kareden önce okunan | 1,48 MB | 1,7 MB |

Her sınır kabaca yüzde 15 ila 18 pay bırakıyor. Sıkıştırılmamış ses ve katmanlı görsel dosyaları gibi asla pakete girmemesi gereken biçimleri de yasaklıyoruz.

## Bir söz değil, bir koruma

Yalnızca bir belgede duran kural unutulur. Bu yüzden boyut denetimi, biçimlendirme, analiz ve testlerle aynı kapının içinde çalışıyor. Bir sınır aşılırsa derleme başarısız olur. Sınırı yükseltmek serbest, ama yalnızca bilerek: sayıyı betikte ve tabloda birlikte değiştirmeniz gerekir.

## Dışarıda kalan yazı tipi

Serif yazı tipi özgün dosya olarak 3,18 MB; bu, bir telefon için çok. Biz onu 1,29 MB'a sıkıştırılmış hâliyle gönderiyoruz, özgün dosya yalnızca depoda duruyor. Biri onu yanlışlıkla uygulamaya eklerse, yasaklı biçim kuralı ve toplam sınır bunu yakalar.

## Açılış süresi

Bir Mac'te yazı tipini açmak yaklaşık 6 milisaniye, açılış resmini yüklemek yaklaşık 14 milisaniye sürüyor. Süre sınırı koymadık, çünkü bir Mac'ten gelen rakamlar, soğuk başlangıçtaki gerçek bir telefon hakkında pek bir şey söylemez.

## Henüz bilmediğimiz

Kurulabilir paketin son boyutunu henüz bilmiyoruz; çünkü sıkıştırma, kod ve motor yalnızca derleme sırasında ekleniyor. Elimize geçince bu rakamı bu tablonun yanına kaydetmeyi planlıyoruz.

// Bütçe, hayır diyebildiği için işe yarar.
