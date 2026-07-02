# Phạm vi P0 / P1 / P2

## P0 - bắt buộc

- Một case study tòa nhà cao tầng và một debug layout thấp tầng.
- IFC-to-Graph có topology report và fallback bán thủ công.
- CFAST là nguồn dataset chính; FDS tối thiểu 3 case tham chiếu.
- IoT preset: `clean`, `low_noise`, `medium_noise`, `faulty`, `no_iot`.
- Baseline bắt buộc: rule-based, non-graph temporal, graph baseline.
- Mô hình chính: Temporal GNN/BAT-GNN rút gọn.
- Output: `smoke_label`, `time_to_arrival`, `arrival_valid_mask`.
- Metrics: F1, Recall, Precision, MAE/RMSE có mask, inference time, robustness drop.
- Dashboard replay + inference + comparison.

## P1 - chỉ làm sau mốc go/no-go

- Gió, cửa sổ, CO, hút khói, chênh áp cầu thang.
- `hazard_label`, `unsafe_time`, calibration.
- Mở rộng FDS đến 6 case.

## P2 - ngoài cam kết

- HVAC duct network đầy đủ, atrium CFD, leakage chính xác.
- IoT phần cứng thật, ASET/RSET đầy đủ, mô hình thoát nạn.
- `smoke_path` hoàn chỉnh hoặc 8-12 case FDS.

## Mốc go/no-go tuần 10

Chỉ giữ P1/P2 khi đồng thời có:

1. Building graph đã kiểm tra topology.
2. Batch CFAST đủ để tạo dataset thử nghiệm.
3. Virtual sensor clean và ít nhất một noisy stream chạy được.

Mọi quyết định thay đổi scope phải ghi ngày, người duyệt, lý do và ảnh hưởng tới sản phẩm.
