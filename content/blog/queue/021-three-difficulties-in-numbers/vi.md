---
title: Ba mức độ khó được giữ chặt bằng con số
description: Chúng tôi ghi lại cách mô phỏng hàng nghìn ván để Dễ, Thường và Khó mỗi mức nằm trong khoảng tỷ lệ thắng của riêng nó, và vì sao bot khiến mức Khó trông còn khó hơn.
date: 2026-11-18
slug: three-difficulties-in-numbers
lang: vi
translation_of: ko
---

Khi chọn Dễ, ta kỳ vọng thắng phần lớn các ván. Khi chọn Khó, ta kỳ vọng bị đè bẹp. Nghe có vẻ hiển nhiên, nhưng mỗi khi có ai đổi một quy tắc hay một vị tướng, điều đó lặng lẽ trượt đi. Vì vậy với từng mức độ khó, chúng tôi giữ chặt khoảng giá trị bằng bài kiểm tra. Trò chơi vẫn đang được phát triển, và bài viết này là một ghi chú về cách làm đó.

## Những gì đã được giữ từ trước

Trước đây đã có các bài kiểm tra. Chúng xem một lá bài hay một vị danh tướng nâng tỷ lệ thắng lên bao nhiêu, và xem ở mức Dễ mọi quốc gia có nằm trong khoảng 60 đến 95 phần trăm không. Thứ chưa được che chắn là tỷ lệ thắng tuyệt đối của Thường và Khó, cùng một sự thật đơn giản rằng Dễ phải dễ hơn Thường, và Thường phải dễ hơn Khó.

## Đo như thế nào

Bot chơi 200 ván cho mỗi quốc gia, dùng một bộ hạt giống cố định và cùng quy tắc như lúc ứng dụng khởi động. Kết quả lần nào cũng giống nhau, và toàn bộ chạy xong trong vài giây. Trung bình bốn quốc gia, đo ngày 5 tháng 11, như sau.

| Ván | Dễ | Thường | Khó |
|---|---|---|---|
| Màn 1 | 79,5% | 23,8% | 6,0% |
| Màn 1 bản lịch sử | 77,5% | 30,5% | 7,9% |
| Sông Hán | 72,3% | 45,4% | 4,4% |

Mỗi bài kiểm tra cho phép lệch khoảng 10 điểm phần trăm lên hoặc xuống quanh giá trị đo. Nếu một thay đổi đẩy kết quả ra ngoài khoảng đó, bài kiểm tra sẽ thất bại.

## Các quy tắc bổ sung

- Giữa các mức độ khó phải có khoảng cách hơn 15 điểm phần trăm.
- Ở mức Khó, không quốc gia nào được vượt quá 25 phần trăm.
- Ở mức Dễ, không quốc gia nào được xuống dưới 55 phần trăm.
- Cùng một hạt giống thì kết quả phải lặp lại y hệt.

## Vì sao mức Khó thấp như vậy

Bot không dùng ngoại giao và gián điệp, nên nó chơi yếu hơn con người. Các giá trị thấp của Thường và Khó là giá trị của bot, không phải lời hứa dành cho người chơi. Chúng tôi cố ý làm lệch các khoảng giá trị để xem bài kiểm tra có thật sự thất bại hay không, và nhờ vậy xác nhận cơ chế hoạt động đúng.

## Những gì con số không nói được

Tỷ lệ thắng không cho biết một ván có công bằng hay có vui không. Những câu trả lời đó vẫn có được từ việc tự tay chơi. Nếu có lúc chúng tôi cố ý dịch chuyển các khoảng giá trị, chúng tôi sẽ sửa cả bảng lẫn ghi chú ở đầu tệp kiểm tra.

// Con số giữ cho độ khó trung thực. Chúng không làm cho nó vui.
