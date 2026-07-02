# Module 03 - Virtual IoT + Dataset

**Chủ trì:** Nguyễn Thu Hương. **Reviewer chéo:** Trần Phùng Đức Anh.

## Mục tiêu

Tạo dữ liệu cảm biến thực tế hơn từ output mô phỏng và đóng gói dataset graph-time-series không label leakage, không split leakage.

## Ba lớp dữ liệu

1. `physics_truth`: output mô phỏng gốc, có truy vết node/time.
2. `virtual_sensor_clean`: lấy mẫu tại sensor schema, không nhiễu.
3. `iot_noisy_stream`: Gaussian noise, delay, missing, stuck, offline, drift, false alarm.

## Preset P0

`clean`, `low_noise`, `medium_noise`, `faulty`, `no_iot`. Mọi random operation dùng `noise_seed`, ghi fault mask và không sửa label.

## Dataset output

- `building_graph.json`;
- static: node/edge/scenario;
- dynamic: node/edge/boundary;
- clean/noisy sensor stream;
- labels và mask;
- split manifests theo `base_scenario_id`;
- PyG objects chỉ là cache dẫn xuất, không phải nguồn dữ liệu duy nhất.

## Quy tắc chống leakage

- Input tại t chỉ dùng dữ liệu trong `[t-k, t]`.
- Target là `smoke_label(t+horizon)` và TTA tại t.
- Không dùng label, arrival time, output tương lai hoặc post-processing feature nhìn trước.
- Tất cả `noise_seed` của cùng base scenario ở cùng split.
- Standardization fit trên train בלבד rồi áp dụng val/test.

## File cần viết

- `iot_sim/noise_models.py`, `iot_sim/presets.py`, `iot_sim/simulator.py`.
- `dataset/build_dataset.py`, `dataset/split_builder.py`, `dataset/windowing.py`.

## Test tối thiểu

- Seed tái lập.
- Delay/missing/fault mask đúng.
- `no_iot` không rò thông tin qua sentinel.
- Split không giao nhau theo base scenario.
- Window cuối không đọc vượt t.
- Schema parquet ổn định.

## DoD

Tạo được clean và 4 biến thể suy giảm cho batch CFAST; dataset loader trả đúng shape/mask và có contract test với model baseline.
