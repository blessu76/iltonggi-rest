---
title: Một tệp lưu vẫn sống sót khi bị hỏng
description: Chúng tôi ghi lại cách Iltonggi bảo vệ tiến trình khi việc ghi tệp bị gián đoạn, và cách chúng tôi thử nghiệm mà không làm hỏng điện thoại thật.
date: 2026-11-15
copy_review: iris 2026-11-14
slug: a-save-that-survives
lang: vi
translation_of: ko
---

Không gì chán nản bằng việc mở một trò chơi đã chơi lâu mà thấy tiến trình biến mất. Nếu pin điện thoại cạn hoặc ứng dụng bị đóng giữa lúc đang ghi tệp, có thể còn lại một tệp mới ghi được một nửa. Chúng tôi muốn Iltonggi sống sót qua những chuyện như vậy. Trò chơi vẫn đang được phát triển, và bài viết này là một ghi chú về việc hiện giờ sự bảo vệ đã đi được đến đâu.

## Phần lớn đã có sẵn

Khi ngồi xuống để bổ sung các biện pháp an toàn, chúng tôi nhận ra bản lưu chính đã có chúng rồi. Chính chúng tôi đã quên mất. Nó hoạt động theo bốn bước.

1. Bản lưu mới được ghi vào một tệp tạm trước, rồi mới thay vào chỗ cũ. Nếu bị ngắt giữa chừng, bản lưu cũ vẫn nguyên vẹn.
2. Bản lưu ngay trước đó được giữ lại làm bản sao dự phòng một thế hệ.
3. Khi nạp, chúng tôi kiểm tra xem tệp có đọc được bình thường không.
4. Nếu tệp hỏng, quay về bản dự phòng. Nếu bản dự phòng cũng hỏng, trò chơi không dừng lại mà bắt đầu một ván mới.

Chỗ hở chỉ nằm ở chỗ biện pháp này chỉ áp dụng cho bản lưu chính. Ba ô lưu, phần cài đặt, các màn đã vượt qua, nhiệm vụ, chợ, vật phẩm đang có, biệt danh và bản ghi thì vẫn chỉ được ghi thẳng.

## Mở rộng, nhưng không phải tất cả

Chúng tôi bật bản dự phòng cho mọi tệp mà mất đi sẽ đau. Những thứ mất cũng không sao, như nhật ký, hướng dẫn, thời tiết và bản ghi, thì không bật. Giữ danh sách ngắn nghĩa là điện thoại lưu ít tệp hơn và chúng tôi cũng có ít thứ phải cân nhắc hơn. Tên và nội dung tệp vẫn như cũ, nên các bản lưu hiện có vẫn dùng được. Thứ duy nhất được thêm vào là các bản sao dự phòng.

## Thử nghiệm mà không làm hỏng điện thoại

Chúng tôi không thể nhờ người chơi rút nguồn giữa lúc ghi. Vì vậy, với mỗi tệp có bản dự phòng, chúng tôi đã tái hiện bốn tình huống bằng bài kiểm tra.

- Khi nội dung tệp lưu bị hỏng: quay về bản dự phòng.
- Khi tệp rỗng: quay về bản dự phòng.
- Khi tệp hỏng và cũng không có bản dự phòng: không dừng lại, bắt đầu một ván mới.
- Khi chỉ còn lại một tệp tạm ghi dở một nửa: bản lưu trước đó vẫn còn nguyên.

## Những gì chúng tôi chưa xác minh

Đây là những thử nghiệm chạy trên máy tính. Chúng tôi chưa từng cố ý làm hỏng một tệp trên thiết bị thật rồi xem nó được khôi phục, nên phần đó chưa được xác minh. Ngoài ra, khi một tệp không phải bản lưu chính được khôi phục, người chơi không nhận được thông báo nào; nó lặng lẽ quay trở lại. Với phần cài đặt, chúng tôi cho rằng như vậy là đúng, nhưng có thể sẽ cân nhắc lại.

// Một bản lưu tốt là bản lưu bạn không hề để ý, cho đến lúc nó cứu bạn.
