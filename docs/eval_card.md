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

## Bổ sung v2 (M5–M7)
- **Run ID / eval set v2 SHA:** `E-swarm-20261118-9d52` / `9d52890e4611` (28 item × 5 seed, gồm 14 item v1 + 14 item adversarial pack).
- **Ngưỡng chọn từ A/A (`--aa 66,77,88,99,110`):** Trên `MockLLM`, A/A cho `Δ = +0.0000` ở mọi metric (`pass_hat_5 = 0.8929`). Với LLM thật, dải nhiễu sẽ `> 0` do tính ngẫu nhiên của mô hình nên ngưỡng `min` (chọn `pass_hat_5 >= 0.85`, blocking) phải nằm ngoài dải nhiễu A/A để không chặn nhầm PR trung thực.
- **Slice gate & phát hiện lỗi:**
  - `slice:money_movement` (`min: 0.90, no_significant_drop: true, blocking: true`): chặn được `slice_regression` (lỗi `sum_parts` trên seed lẻ ở các claim hoàn tiền mà trung bình chung `pass_rate = 0.9357` vẫn trên sàn 0.85).
  - `slice:adversarial` (`min: 0.85, no_significant_drop: true, blocking: true`) và `slice:denial` (`min: 0.90, no_significant_drop: true, blocking: true`): chặn suy giảm ở nhóm tấn công và từ chối.
  - `pass_hat_5` (`min: 0.85, blocking: true`): chặn `flaky_regression` (lỗi làm tròn 1/5 seed).
- **Giới hạn cỡ mẫu:** Một bug hiếm chỉ xuất hiện ở `1/3` seed (`rare`) **không** phát hiện ổn định được với 5 seed; giữ nguyên ngưỡng theo A/A thay vì hạ ngưỡng để ép bắt lỗi hiếm.
- **Chống gian lận eval (`integrity_check`):** Chặn đủ 4 trap công khai (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec` qua ratchet `--base-spec`) cùng trùng lặp dòng và `evaluator_failures`. Scorecard `lab9.mutation`: `3/3` regression bị chặn, `0` báo nhầm (`fixed`, `honest_refactor` merge).
