---
title: Dừng động cơ khi không ai nhìn
description: Khi màn hình bị che hoặc ứng dụng chuyển sang nền, động cơ game sẽ dừng lại. Đây là quy tắc chúng tôi đặt ra khi chuyển sang bộ công cụ động cơ dùng chung, và những gì chúng tôi chưa đo.
slug: stop-engine-when-hidden
lang: vi
translation_of: en
date: 2026-11-23
---

Các cảnh bản đồ và chiến trận trong Iltonggi là những hình ảnh chuyển động. Lính đi lại, cờ phất phới, và các trận giao tranh diễn ra từng khung hình. Nhưng khi người chơi nghe điện thoại hoặc chuyển sang ứng dụng khác, không có lý do gì để tiếp tục vẽ những hình ảnh mà không ai nhìn thấy. Bài này ghi lại quy tắc chúng tôi đặt ra hôm nay, trong lúc chuyển động cơ game sang một bộ công cụ dùng chung. Game vẫn đang trong quá trình phát triển.

## Dừng khi không có gì để nhìn

Khi màn hình bị che, hoặc ứng dụng chuyển sang nền, động cơ sẽ dừng. Vẽ một cảnh mà không ai nhìn thấy chỉ tốn pin. Khi người chơi quay lại, việc vẽ tiếp tục từ chỗ đã dừng. Bản đồ mà người chơi để lại phải vẫn như cũ, nên chúng tôi không để thời gian trong game trôi lặng lẽ khi ứng dụng đang bị ẩn.

## Một nơi quyết định khi nào dừng

Trước đây, mỗi cảnh có mã dừng riêng. Bản đồ, sân khấu chiến trận và màn hình menu đầu đều tự kiểm tra xem mình có bị ẩn không, và mỗi nơi phải được sửa riêng. Giờ công việc này do một lớp vỏ dùng chung đảm nhận. Các cảnh không còn hỏi mình có đang hiện hay không. Chúng làm theo trạng thái mà lớp vỏ đặt ra.

## Hoạt cảnh giao tranh vẫn tiếp tục

Khi hai đạo quân va chạm trên bản đồ, hoạt cảnh chỉ chuyển động trong lúc động cơ đang chạy. Vì vậy trong lúc giao tranh, động cơ đang dừng được bật lên cho khoảnh khắc đó và tắt lại khi giao tranh kết thúc. Tốc độ và thứ tự của hoạt cảnh không thay đổi. Chúng tôi cũng đã vá một kẽ hở: nếu giao tranh kết thúc khi màn hình đang bị che, động cơ sẽ không tự khởi động lại khi màn hình quay về nữa.

## Những điều chúng tôi chưa đo

Chúng tôi chưa đo được việc này tiết kiệm bao nhiêu pin. Một số việc chỉ kiểm tra được trên thiết bị thật: đưa ứng dụng xuống nền rồi mở lại, chuyển qua lại giữa bản đồ và màn hình khác, giới hạn 30 khung hình mỗi giây, và việc vẽ trên GPU mất bao lâu. Cho đến khi đo được, bài này chưa đưa ra con số nào về pin.

// Hình ảnh không ai nhìn thấy là thứ rẻ nhất để bỏ qua.
