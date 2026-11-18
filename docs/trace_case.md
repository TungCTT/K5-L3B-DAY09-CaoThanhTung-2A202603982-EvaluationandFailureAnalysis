# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi bạn 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID `E-seeded_regression-20261118-6c8d` |
| Triệu chứng | `TrialPass` (`status resolved != denied`) và `RefundAmountCorrect` đều FAIL; reply nói *"Dạ, LogiX đã hoàn 20.000đ cho đơn O-202."*, ledger ghi `refund_vnd=20000`, `refund_count=1` trong khi nhãn là `0` và `denied`. |
| Bước sai đầu tiên | Event `3` `model_override` `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event `1` (`handoff`) giao đúng `allowed_tools`; Event `2` (`investigator`) tra `lookup_order` trả đúng đơn `O-202` với `delay_days=2` từ DB. Chỉ tới Event `3`, agent mới tin ticket (`"trễ 5 ngày"`) và ghi đè `delay_days=5`, kéo theo Event `4` (`quote`) tính sai 20.000đ. |
| Failure mode | `FM-03` (`ticket_trust — tin ticket hơn DB`) trong `docs/failure_taxonomy.md` |
| Đối chứng | Trên `fixed C-002@11`: không có event `model_override`; sau Event `2` (`investigator`) đi thẳng sang Event `3` (`quote`, `amount_vnd=0, reason="no_entitlement"`) và Event `4` (`reply`, từ chối hợp lệ), ledger `refund_vnd=0`, `status=denied`. |
| Regression test | `src/tests/test_lab9_trace_regression.py` (`test_c002_seeded_regression_caught_by_graders` & `test_c002_fixed_passes_db_fact_and_refund`) dùng `DbFactKept` và `RefundAmountCorrect`; đã thấy bắt lỗi trên `seeded_regression` và pass trên `fixed`. |
| Chưa chắc chắn | Trace trên `MockLLM` không chứng minh được model thật sẽ không bị lừa nếu prompt/ticket diễn đạt tinh vi hơn mà không phát sinh event `model_override`. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
