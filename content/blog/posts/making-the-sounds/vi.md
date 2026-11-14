---
title: Từ tiếng trống trận đến đàn gayageum, âm thanh cũng do chúng tôi tự làm
description: 15 hiệu ứng và 4 bản nhạc nền của Iltonggi được tổng hợp bằng script mà không dùng âm thanh bên ngoài ra sao, và vì sao chúng tôi làm lại một số.
slug: making-the-sounds
lang: vi
translation_of: ko
date: 2026-11-06
copy_review: iris 2026-11-14
published: 2026-11-06T12:00:00+09:00
---

Âm thanh là phần của Iltonggi mà chúng tôi chỉnh sửa lâu nhất. Hình ảnh thì nhìn là thấy ngay, còn âm thanh khi sai thì khó nói được sai ở chỗ nào. Bài này ghi lại cách làm âm thanh và lý do chúng tôi đã làm lại một số trong đó một lần.

## Không dùng âm thanh bên ngoài

Hiện trong game có 19 âm thanh: 15 hiệu ứng và 4 bản nhạc nền. Tất cả đều được tổng hợp từ con số không bằng script. Chúng tôi không dùng mẫu tải về hay âm thanh mua sẵn. Vì vậy, chạy lại cùng một script sẽ tạo lại đúng âm thanh ấy. Giải thích được nguồn gốc của từng âm thanh là lý do chính khiến chúng tôi chọn cách này.

## Trống, ấn, cờ và mực

Có bốn tiếng trống cho chiến đấu và hành quân. Mỗi tiếng bắt đầu từ một sóng sin có cao độ hạ dần, thêm một chút nhiễu ngắn ở trên để gợi cảm giác dùi đánh vào mặt da. Cao độ được tách ra, khoảng 55, 59, 65 và 85 Hz.

Tiếng ấn khi chiếm đất là một nốt trầm hạ từ 94 Hz xuống 39 Hz. Nhưng loa nhỏ của điện thoại gần như không phát được những nốt thấp như vậy. Vì thế chúng tôi trộn thêm một ít họa âm để dù phần trầm nhất mất đi, cảm giác thịch vẫn còn.

Tiếng cờ, dùng khi thắng trận và khi qua lượt, chỉ cho nhiễu đi qua một dải hẹp rồi làm nó rung nhanh, như tấm vải trong gió. Dài 1,4 giây. Tiếng mực dùng trong ngoại giao lan ra chậm trong 2,2 giây và đậm nhất vào khoảng giây thứ 1,3. Tiếng nút bấm chồng hai âm ngắn 620 và 1240 Hz và tắt trong 0,15 giây, như một chiếc nút gỗ.

## Những âm thanh đã làm lại

Tám trong số các hiệu ứng đầu tiên có vài vấn đề nên chúng tôi làm lại.

- Một số đỉnh âm chạm tới trần. Giờ tất cả đều thấp hơn trần ít nhất 1 dB, không còn chỗ để méo tiếng.
- Ba tiếng trống bị cắt trước khi nhát đánh thứ hai kết thúc. Giờ mỗi âm thanh được giảm dần mềm mại trong 5 ms đầu và cuối, nên không còn tiếng lách cách.
- Độ lớn của các âm thanh không đồng đều. Giờ mức trung bình của cả tám được cân trong khoảng 0,1 dB.

Khi làm lại, chúng tôi cố không đổi tính cách của âm thanh. Cao độ của trống, hình dáng hạ xuống của tiếng ấn và thời điểm mực đậm nhất đều được giữ nguyên.

## Nhạc nền

Nhạc nền xoay quanh âm thanh mô phỏng đàn gayageum và sáo daegeum. Gayageum được làm bằng cách tính toán một sợi dây được gảy (phương pháp Karplus-Strong), còn daegeum bằng cách chồng các họa âm và trộn thêm tiếng thở. Thêm vào đó là một tiếng trống và nốt trầm kéo dài, còn các nốt lấy từ thang năm âm của nhạc truyền thống Hàn Quốc. Mỗi cảnh menu, bản đồ, chiến đấu và chiến thắng có một bản.

## Trên màn hình nghe như thế này

- Khi các chữ của tiêu đề giáng xuống đánh thịch, có rung đi kèm với âm thanh.
- Các video giữa các màn có tiếng trống, vó ngựa, gió, sấm và tiếng ấn.
- Âm thanh vẫn vang lên dù công tắc im lặng của điện thoại đang bật, và nhạc nền phát ở bốn màn hình.
- Trong phần cài đặt có thể tắt hoặc giảm hiệu ứng.

## Điều chúng tôi chưa làm được

Nói thật, chúng tôi chưa nghe những âm thanh này bằng đôi tai con người đủ lâu. Độ lớn, độ dài, việc có bị cắt hay không đã được kiểm tra bằng con số, nhưng nút gỗ và mặt da trống nghe có hay không thì còn cần nghe thêm trên loa và tai nghe thật. Nhạc nền là phiên bản đầu tiên, vẫn còn chỗ để trau chuốt.

// Âm thanh có thể chỉnh bằng con số, nhưng cuối cùng vẫn do đôi tai quyết định.
