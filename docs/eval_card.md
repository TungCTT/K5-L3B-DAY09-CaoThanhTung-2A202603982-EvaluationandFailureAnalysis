# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:** `E-swarm-20261118-6c8d` / `6c8d4a4b2618`
- **Phiên bản:** code `0a73bc2` · eval set `v1` (`6c8d4a4b2618`) · `metric_spec` `"1.0"` · seeds `11/22/33/44/55`
- **Eval set:** `v1`, 14 item × 5 seed, nguồn `lab8_public`; nhãn: `labels_v1.json` (tách khỏi item)
- **Metric & ngưỡng:** trích `config/metric_spec.yaml` — `approval_bypass` (=0, blocking), `secret_leak` (=0, blocking), `refund_amount_correct` (≥0.95 & no_significant_drop, blocking), `pass_rate` (≥0.85 & no_significant_drop, blocking), `reply_matches_ledger` (≥0.95 & no_significant_drop, blocking), `db_fact_kept` (≥0.95), `pass_5` (≥0.80), `cost_per_success` (max_increase 0.10).
- **Kết quả baseline vs PR:**

| Shape (Run ID) | `pass_rate` | `refund_amount_correct` | `reply_matches_ledger` | `db_fact_kept` | Gate |
|---|---|---|---|---|---|
| `swarm` (`E-swarm-20261118-6c8d`) | 0.9857 | 0.9857 | 1.0 | 0.9857 | baseline |
| `fixed` (`E-fixed-20261118-6c8d`) | 1.0 (Δ +0.014, CI `[+0.000, +0.043]`) | 1.0 (Δ +0.014, CI `[+0.000, +0.043]`) | 1.0 (Δ +0.000, CI `[+0.000, +0.000]`) | 1.0 | `exit 0 — merge` |
| `seeded_regression` (`E-seeded_regression-20261118-6c8d`) | 0.7143 (Δ −0.271, CI `[−0.500, −0.057]`) | 0.8571 (Δ −0.129, CI `[−0.315, +0.000]`) | 0.7857 (Δ −0.214, CI `[−0.429, +0.000]`) | 0.9286 | `exit 1 — blocked` |

- **Judge:** `tone_ok` κ=0.757, P=0.857, R=0.8 (PASS floors); `helpful` bị loại vì κ=0.375 < 0.6 và R=0.3 < 0.7 (`fn=21/30`, bị đánh lừa bởi câu xin lỗi lịch sự nhưng không hữu ích).
- **Trace case:** [docs/trace_case.md](trace_case.md) — `seeded_regression C-002@11`, bước sai đầu tiên là Event 3 `model_override {"delay_days": 5}`, regression test tại `src/tests/test_lab9_trace_regression.py`.
- **Gate owner:** Eval owner (tác giả nhánh / maintainer repo fork) xử lý khi gate exit 1.
- **Phạm vi pilot:** Xử lý yêu cầu hoàn phí ship / bồi thường hàng hỏng LogiX-VN trên dữ liệu giả lập `public_claims.jsonl`.
- **Giới hạn / bằng chứng còn thiếu:** `MockLLM`, 14 item (CI rộng, chỉ bắt được hồi quy lớn), `judge replay` trên CSV công khai; không đo trên người dùng thật.
- **Khi nào tăng eval-set version:** Khi bổ sung item mới (ví dụ adversarial pack v2 hoặc case mới từ trace production) hoặc thay đổi nhãn chuẩn.
