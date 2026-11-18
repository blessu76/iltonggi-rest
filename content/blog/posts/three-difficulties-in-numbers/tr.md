---
title: Sayılarla Yerinde Tutulan Üç Zorluk Seviyesi
description: Kolay, Normal ve Zor seviyelerini kendi kazanma oranı aralıklarında tutmak için binlerce savaşı nasıl simüle ediyoruz ve bot neden Zor'u daha zor gösteriyor.
date: 2026-11-18
copy_review: iris 2026-11-14
slug: three-difficulties-in-numbers
lang: tr
---

Kolay'ı seçerseniz çoğu zaman kazanmayı beklersiniz. Zor'u seçerseniz zorlanmayı beklersiniz. Bu apaçık görünüyor, ama biri bir kuralı ya da bir generali değiştirdiğinde sessizce bozuluyor. Bu yüzden her zorluk seviyesini testlerle bir aralıkta tutuyoruz. Oyun hâlâ geliştirme aşamasında ve bu yazı, bunun nasıl işlediğinin notudur.

## Daha önce neyin güvencesi vardı

Bundan önce testlerimiz, bir kartın ya da ünlü bir generalin kazanma oranını ne kadar artırdığını ve Kolay'ın her krallığa yüzde 60 ile 95 arasında verip vermediğini kapsıyordu. Hiçbir şeyin kapsamadığı, Normal ve Zor'un mutlak kazanma oranı ya da Kolay'ın Normal'i, Normal'in de Zor'u geçmesi gerektiği basit gerçeğiydi.

## Nasıl ölçüyoruz

Bir bot, uygulamanın başlangıcıyla aynı kuralları kullanarak, sabit bir rastgele tohum kümesiyle her krallığı 200 kez oynuyor. Sonuçlar her seferinde aynı ve tüm çalışma birkaç saniye sürüyor. 5 Kasım'da ölçülen, dört krallık üzerindeki ortalamalar:

| Harita | Kolay | Normal | Zor |
|---|---|---|---|
| 1. Perde | %79,5 | %23,8 | %6,0 |
| Tarihî 1. Perde | %77,5 | %30,5 | %7,9 |
| Han Nehri | %72,3 | %45,4 | %4,4 |

Her test, ölçümün iki yanında yaklaşık 10 puanlık bir banda izin veriyor. Bir değişiklik sonucu bandın dışına iterse test başarısız olur.

## Birkaç ek kural

- Zorluk seviyeleri arasında 15 puandan büyük bir fark olmalı.
- Zor'da hiçbir krallık yüzde 25'i aşmamalı.
- Kolay'da hiçbir krallık yüzde 55'in altına düşmemeli.
- Aynı tohumla sonuçlar birebir tekrarlanmalı.

## Zor neden bu kadar düşük görünüyor

Bot diplomasi ya da casus kullanmıyor, bu yüzden bir insandan daha kötü oynuyor. Normal ve Zor'daki düşük rakamlar botun rakamlarıdır, insan oyuncular için verilmiş bir söz değildir. Korumanın gerçekten çalıştığını, bir aralığı bilerek bozup testin başarısız olmasını izleyerek kontrol ettik.

## Bize söyleyemedikleri

Bir kazanma oranı, oyunun adil ya da eğlenceli hissettirip hissettirmediğini söylemez. Bu cevaplar hâlâ elle oynayarak geliyor. Bir aralığı bir gün bilerek kaydırırsak, test dosyasının başındaki tabloyu ve notları birlikte değiştiririz.

// Sayılar bir zorluk seviyesini dürüst tutabilir. Onu eğlenceli yapamaz.
