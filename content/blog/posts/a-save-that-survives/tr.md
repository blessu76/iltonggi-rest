---
title: Bozulsa Bile Hayatta Kalan Bir Kayıt Dosyası
description: Iltonggi, kayıt dosyası yazılırken yarıda kesilirse ilerlemenizi nasıl korur ve bunu gerçek bir telefonu bozmadan nasıl test ettik.
date: 2026-11-15
copy_review: iris 2026-11-14
slug: a-save-that-survives
lang: tr
---

Uzun bir oyunu açıp ilerlemenizin yok olduğunu görmek kadar can sıkıcı bir şey yok. Telefonun şarjı bitebilir ya da uygulama bir dosya yazılırken kapatılabilir; o zaman diskte yarım bir dosya kalır. Iltonggi'nin buna dayanmasını istedik. Oyun hâlâ geliştirme aşamasında ve bu yazı, korumanın bugün nereye kadar gittiğinin notudur.

## Zaten büyük kısmı vardı

Bir güvenlik ağı eklemek için oturduğumuzda, ana kayıtta zaten bir tane olduğunu gördük. Unutmuşuz. Dört adımda çalışıyor.

1. Yeni kaydı önce geçici bir dosyaya yaz, sonra yerine koy. Yarıda kesilen bir yazma eski kayda dokunmaz.
2. Önceki kaydın bir yedek nesli tut.
3. Yüklerken dosyanın doğru okunduğunu kontrol et.
4. Bozuksa yedeği geri yükle. Yedek de bozuksa çökmek yerine yeni bir oyun başlat.

Eksik olan, bunun yalnızca ana kayıtta olmasıydı. Üç kayıt yuvası, ayarlar, tamamladığınız perdeler, görevler, mağaza, sahip olunan eşyalar, takma adınız ve kayıtlarınız gibi geri kalan her şey düz biçimde yazılıyordu.

## Genişlettik ama her şeye değil

Yedeği, kaybı canımızı yakacak her dosya için açtık. Günlükler, ipuçları, hava durumu ve geçmiş için kapalı bıraktık; çünkü bunları kaybetmek önemli bir şeye mal olmuyor. Listeyi kısa tutmak, telefonda daha az ek dosya ve düşünülecek daha az şey demek. Dosya adları ve içerikleri aynı kaldı, dolayısıyla mevcut kayıtlar çalışmaya devam ediyor. Tek ekleme yedek kopyadır.

## Telefonu bozmadan test etmek

Bir oyuncudan yazma sırasında fişi çekmesini isteyemeyiz; bu yüzden artık yedeği olan her dosya için testlerde dört durumu yeniden ürettik:

- Kayıtta bozuk metin var: yedek geri yüklenir.
- Dosya boş: yedek geri yüklenir.
- Bozuk ve yedek yok: oyun çökmeden yeniden başlar.
- Yalnızca yarım yazılmış geçici dosya var: önceki kayıt yerinde durur.

## Doğrulamadıklarımız

Bunlar bilgisayarda yapılan testler. Gerçek bir cihazda bir dosyayı bilerek bozup kurtarılmasını henüz izlemedik; bu kısım doğrulanmamış durumda. Ayrıca ana kayıt dışında bir şey geri yüklendiğinde oyuncu hiçbir mesaj görmüyor. Sessizce geri geliyor. Ayarlar için bunun doğru olduğunu düşünüyoruz, ama yeniden ele alabiliriz.

// İyi bir kayıt sistemi, yalnızca sizi kurtardığında fark ettiğiniz sistemdir.
