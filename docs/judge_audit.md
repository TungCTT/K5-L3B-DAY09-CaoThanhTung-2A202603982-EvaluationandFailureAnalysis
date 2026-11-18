# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.8 | Đạt (κ≥0.6, P≥0.8, R≥0.7) | dùng |
| helpful | 100 | 0.375 | 1.0 | 0.3 | Không đạt (κ=0.375 < 0.6, R=0.3 < 0.7) | loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú / Sửa rubric |
|---|---|---|---|---|---|
| 1 | `H-008` (`tone_ok`) | PASS | FAIL | Người | `"Em đã hoàn tiền cho anh rồi nha, anh check giúp em."` — xưng "em/anh", dùng "nha", "check" thiếu chuẩn CSKH. Sửa rubric: cấm từ lóng/khẩu ngữ ("nha", "nhé") và xưng hô thân mật ("em/anh", "bạn ơi"). |
| 2 | `H-017` (`tone_ok`) | PASS | FAIL | Người | `"Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha."` — dùng "bạn ơi", "nha" dù có "Dạ". Sửa rubric: không chỉ kiểm tra từ khóa "Dạ/ạ", phải phạt khẩu ngữ. |
| 3 | `H-029` (`tone_ok`) | PASS | FAIL | Người | `"Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm."` — giọng ra lệnh/cộc lốc ("không cần nhắn thêm"). Sửa rubric: thêm ví dụ câu đuổi khéo/cộc lốc là FAIL. |
| 4 | `H-042` (`tone_ok`) | FAIL | PASS | Người | `"Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ."` — đầy đủ, lịch sự; judge báo nhầm (FP). Sửa rubric: câu thông báo ngắn gọn có "Dạ/ạ" và thông tin rõ ràng là PASS. |
| 5 | `H-051` (`tone_ok`) | FAIL | PASS | Người | `"Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ."` — xen từ "refund". Sửa rubric: quy định rõ từ chuyên ngành tiếng Anh thông dụng ("refund") có bị phạt hay được chấp nhận. |
| 6 | `HL-016` (`helpful`) | PASS | FAIL | Người | `"Dạ, LogiX thành thật xin lỗi anh/chị vì sự bất tiện này và rất trân trọng sự kiên nhẫn của..."` — xin lỗi dài dòng nhưng không nêu kết quả/hành động tiếp theo. Sửa rubric: tách "lịch sự" khỏi "hữu ích", bắt buộc có trạng thái xử lý hoặc bước tiếp theo cụ thể. |

## Kết luận
- **Tiêu chí bị loại:** `helpful` (`judge_helpful_public.csv`) bị loại khỏi CI gate vì không đạt ngưỡng (`κ = 0.375 < 0.6`, `Recall = 0.3 < 0.7`). Ma trận nhầm lẫn `{'tp': 9, 'fp': 0, 'fn': 21, 'tn': 70}` cho thấy `fn = 21` (bỏ sót 21/30 ca lỗi thật): judge bị đánh lừa bởi các câu xin lỗi dài dòng/lịch sự nhưng vô dụng, làm tỉ lệ lỗi quan sát chỉ là `0.09` trong khi tỉ lệ hiệu chỉnh Rogan-Gladen thực tế là `0.30`.
- **Tiêu chí được giữ lại:** `tone_ok` (`{'tp': 24, 'fp': 4, 'fn': 6, 'tn': 66}`, `κ = 0.757`, `P = 0.857`, `R = 0.8`, Rogan-Gladen `0.28 → 0.30`) đạt toàn bộ FLOORS nên đủ tin cậy để theo dõi (non-blocking hoặc audit định kỳ).
- **Rủi ro còn lại:** judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
