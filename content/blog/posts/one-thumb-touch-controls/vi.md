---
title: Một ngón cái, một vùng đất: thiết kế điều khiển cảm ứng cho game bản đồ
description: Game tranh đoạt lãnh thổ phải chơi được chỉ bằng một ngón cái trên màn hình nhỏ. Đây là cách chúng tôi nghĩ về chạm, kéo và những lỗi cần tránh.
slug: one-thumb-touch-controls
lang: vi
translation_of: en
copy_review: iris 2026-11-19
date: 2026-11-22
published: 2026-11-22T16:00:00+09:00
---

Iltonggi là game bản đồ, và một game bản đồ trên điện thoại đòi hỏi rất nhiều từ một ngón cái. Bạn phải chọn một vùng, xem quân của vùng đó, di chuyển đội quân và đọc kết quả, mà không che chính vùng mình muốn chạm. Bài viết này mô tả cách chúng tôi nghĩ về thao tác cảm ứng. Game vẫn đang được phát triển, vì vậy hãy đọc các quy tắc này như những điều đang được thử nghiệm, không phải hướng dẫn hoàn chỉnh.

## Chạm và kéo là hai việc khác nhau

Lỗi phổ biến nhất trong game bản đồ là coi mọi lần chạm là một lần nhấp chuột. Một ngón tay di chuyển nhẹ trong lúc bản đồ trượt bên dưới không phải là một lựa chọn. Vì vậy chúng tôi tách hai ý định: chạm ngắn để chọn, và di chuyển dài hơn để kéo bản đồ. Nếu ngón tay đi quá một khoảng cách nhỏ trước khi nhấc lên, lần chạm đó thuộc về bản đồ và không vùng nào được chọn.

Nguyên tắc quan trọng hơn con số chính xác. Người chơi không bao giờ được chọn nhầm một vùng khi đang cuộn qua một khu vực đông đúc của bản đồ.

## Vùng đất trên điện thoại nhỏ bé

Có những vùng rất hẹp, trong khi ngón cái thì rộng. Khi xung quanh không có vùng nào khác, chúng tôi cho phép vùng chạm của một vùng vượt ra ngoài đường viền đã vẽ một chút. Nhưng chúng tôi không để vùng đó lớn đến mức cướp mất lần chạm dành cho vùng láng giềng. Khi hai vùng nằm gần nhau, lựa chọn phải phụ thuộc vào chỗ ngón tay chạm vào, không phụ thuộc vào vùng nào được vẽ sau cùng.

## Xác nhận những nước đi tốn kém

Tấn công hoặc di chuyển quân làm thay đổi trạng thái game, nên việc làm chúng do nhầm lẫn phải khó hơn việc chỉ nhìn vào một vùng. Một lần chạm cho thấy điều gì sẽ xảy ra, và một thao tác thứ hai có chủ ý mới thực hiện nó. Cách này làm chậm đi một chút, và người đã thuộc bản đồ có thể thấy chậm hơn. Chúng tôi chấp nhận sự đánh đổi này, vì một đội quân gửi nhầm còn phiền hơn một lần chạm thừa.

## Phiên chơi ngắn, thường bị gián đoạn

Mọi người chơi Iltonggi trong những phiên ngắn: trên xe buýt, khi xếp hàng, vài phút trước khi đi ngủ. Sự gián đoạn có thể đến bất cứ lúc nào, như một cuộc gọi hoặc việc chuyển sang ứng dụng khác. Vì vậy điều khiển không được phụ thuộc vào một cử chỉ kéo dài. Một thao tác kéo dở dang phải kết thúc mà không có kết quả, và bản đồ phải giữ nguyên vị trí người chơi đã rời đi.

## Những điều chúng tôi còn phải kiểm tra

Kích thước ngón tay khác nhau, và màn hình điện thoại cũng vậy. Các giả định của chúng tôi chủ yếu đến từ những thiết bị mình có. Chúng tôi dự định thử vùng chạm trên nhiều màn hình hơn và quan sát nơi người chơi chạm nhầm. Chúng tôi chưa đo điều này ở quy mô lớn, nên bài viết này không đưa ra con số nào.

// Lần chạm an toàn nhất là lần chạm bạn có thể hoàn tác.
