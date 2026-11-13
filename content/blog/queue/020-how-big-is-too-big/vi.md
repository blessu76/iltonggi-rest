---
title: Trò chơi điện thoại lớn đến mức nào là quá lớn
description: Chúng tôi ghi lại cách đặt ngân sách kích thước cho hình ảnh, âm thanh và phông chữ của Iltonggi, và để bản dựng dừng lại khi vượt ngân sách.
date: 2026-11-17
slug: how-big-is-too-big
lang: vi
translation_of: ko
---

Một trò chơi tải về lâu hoặc màn hình đầu tiên hiện chậm sẽ mất người chơi trước cả khi họ kịp thử. Iltonggi chứa rất nhiều thứ. Có phông chữ mang cảm giác cổ xưa, hình ảnh, nhạc và hiệu ứng âm thanh, và chữ của mười một ngôn ngữ. Nếu không ai trông chừng, nó chỉ có thể to ra. Vì vậy chúng tôi đặt ra một ngân sách và để máy tính giữ nó. Trò chơi vẫn đang được phát triển.

## Đo cái gì

Chúng tôi không đếm mọi thứ có trong dự án, mà chỉ đếm những tệp mà ứng dụng thật sự đóng gói. Các giá trị tính đến ngày 5 tháng 11 như sau.

| Hạng mục | Số đo | Giới hạn |
|---|---|---|
| Toàn bộ tài nguyên đóng gói (74 tệp) | 9,83 MiB | 12.000.000 byte |
| Tệp lớn nhất (phông chữ Myeongjo, đã nén) | 1,29 MB | 1,5 MB |
| Âm thanh | 4,27 MB | 5 MB |
| Ảnh (23 ảnh) | 3,55 MB | 4,2 MB |
| Phần đọc trước màn hình đầu tiên | 1,48 MB | 1,7 MB |

Mỗi giới hạn chừa khoảng 15 đến 18 phần trăm dư địa. Chúng tôi cũng chặn những định dạng không nên được đóng gói, chẳng hạn âm thanh chưa nén hoặc tệp hình ảnh có nhiều lớp.

## Một cơ chế, không phải một lời hứa

Một quy tắc chỉ nằm trong tài liệu sẽ bị quên. Vì vậy việc kiểm tra kích thước chạy trong cùng cổng kiểm soát với việc chuẩn hóa định dạng, phân tích và kiểm thử. Nếu vượt giới hạn, bản dựng thất bại. Nâng giới hạn thì được, nhưng chỉ khi làm có chủ ý: phải sửa cả con số trong đoạn mã lẫn bảng này.

## Phông chữ để bên ngoài

Tệp gốc của phông chữ Myeongjo nặng 3,18 MB, quá lớn cho điện thoại. Chúng tôi đóng gói bản nén 1,29 MB và chỉ giữ bản gốc trong kho lưu trữ. Nếu ai đó vô tình đưa nó vào ứng dụng, quy tắc định dạng bị cấm và giới hạn tổng sẽ cùng bắt được.

## Thời gian khởi động

Giải nén phông chữ trên máy Mac mất khoảng 6 mili giây, và đọc hình ảnh mở đầu mất khoảng 14 mili giây. Chúng tôi không đặt giới hạn thời gian. Con số đo trên máy Mac nói được rất ít về lần chạy đầu tiên trên một chiếc điện thoại thật.

## Những gì chúng tôi chưa biết

Chúng tôi chưa biết kích thước cuối cùng của gói cài đặt. Phần nén, mã và bộ máy chỉ được cộng vào khi dựng bản. Khi biết giá trị, chúng tôi dự định ghi nó bên cạnh bảng này.

// Ngân sách có sức mạnh vì nó có thể nói không.
