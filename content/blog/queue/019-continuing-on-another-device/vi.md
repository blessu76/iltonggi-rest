---
title: Tiếp tục chơi trên một thiết bị khác
description: Chúng tôi ghi lại cách Iltonggi cho phép tiếp tục ván chơi giữa các thiết bị Apple, và quy tắc đã chọn khi nội dung trên hai thiết bị khác nhau.
date: 2026-11-16
slug: continuing-on-another-device
lang: vi
translation_of: ko
---

Yêu cầu ban đầu rất đơn giản. Một ván đang chơi trên một thiết bị Apple phải có thể tiếp tục trên thiết bị khác cùng tài khoản. Nghe có vẻ nhỏ, nhưng phần khó không phải là sao chép bản lưu. Phần khó là quyết định phải làm gì khi hai thiết bị có hai phiên bản khác nhau. Bài viết này là một ghi chú về quy tắc chúng tôi đã chọn. Trò chơi vẫn đang được phát triển.

## Bản gốc nằm trên thiết bị

Mỗi thiết bị coi tệp của chính nó là bản lưu thật. iCloud chỉ giữ một bản sao, không phải bản gốc. Nếu iCloud bị tắt, đã đăng xuất, hoặc thiết bị chạy Android, mọi thứ lặng lẽ chạy ngay trong thiết bị đó mà không báo lỗi. Bản lưu chính, ba ô lưu và phần cài đặt tham gia vào việc này.

## So sánh ba bên

Để quyết định làm gì, mỗi thiết bị nhớ dấu vân tay của phiên bản mà lần cuối nó khớp với đám mây. Sau đó nó so sánh.

- Chỉ thiết bị này thay đổi: tải lên.
- Chỉ đám mây thay đổi: tải xuống.
- Cả hai đều thay đổi: dùng quy tắc để chọn một bên.

## Khi cả hai đều thay đổi

Thứ tự chúng tôi đã chọn như sau.

1. Bản lưu có nội dung thắng bản lưu rỗng.
2. Nếu thời điểm lưu chênh nhau hơn 2 phút, bản mới hơn thắng.
3. Nếu chênh trong vòng 2 phút và cùng một ván, bản có nhiều lượt hơn thắng.
4. Nếu vẫn chưa phân định, bản của thiết bị này thắng.

Phần này khiến chúng tôi bất đồng ý kiến. Nói «bên chơi được nhiều nhất» thì dễ giải thích hơn, nhưng chúng tôi cho rằng «bên lưu sau cùng» gần với điều người chơi mong muốn hơn. Bên thua không bị xóa mà được giữ riêng thành một bản sao xung đột.

## Gộp lại thay vì chọn

Có những thứ không nên mất vì một lần tung đồng xu. Các màn đã vượt qua, những màn đã xem và những thứ đang có được gộp lại thành hợp của cả hai bên, thay vì chọn một bên.

## Giới hạn kích thước

Nếu một đoạn văn bản vượt quá 200.000 ký tự, chúng tôi không tải nó lên mà chỉ giữ trên thiết bị. Giới hạn này được xác nhận bằng bài kiểm tra.

## Nhận biết ngay khi đang chơi

Ban đầu, chúng tôi chỉ đọc lại đám mây khi quay trở lại ứng dụng. Từ bản dựng 85, ứng dụng cũng nhận biết những thay đổi từ thiết bị khác trong lúc nó đang hiển thị phía trước, và màn hình cài đặt cho thấy đồng bộ iCloud đang bật hay không.

## Những gì chúng tôi chưa xác minh

Tất cả những điều này đều là thử nghiệm chạy trên máy tính. Chúng tôi chưa tận mắt thấy hai thiết bị thật cùng tài khoản trao đổi một ván với nhau, nên phần đó chưa được xác minh. Hình các tướng và tiến độ nhiệm vụ được chủ ý chỉ giữ trên từng thiết bị.

// Đồng bộ thì dễ. Quyết định ai đúng mới là công việc.
