# Module 02 - Scenario + CFAST

**Chủ trì:** Võ Nguyễn Anh Kiệt. **Reviewer chéo:** Trần Phùng Đức Anh / Đào Ngọc Long.

## Mục tiêu

Tạo catalog kịch bản có kiểm soát, chuyển graph + scenario thành input CFAST, chạy batch có log/retry, chuẩn hóa output về node/sensor time-series và tạo label P0 bằng logic dùng chung.

## Input

- Building graph đã validate.
- `scenario_schema.yaml`, `sensor_schema.yaml`, `label_rules.yaml`.
- CFAST binary path từ biến môi trường.

## Output

- Scenario catalog và từng scenario config.
- Input CFAST có thể tái tạo từ config.
- Raw output/log theo `scenario_id`.
- `node_dynamic.parquet`, `virtual_sensor_clean.parquet`, `labels.parquet`.
- Batch manifest gồm trạng thái, thời gian chạy, exit code, hash input.

## File cần viết

- `scenario/sampler.py`: controlled sampling; không full Cartesian product.
- `cfast_sim/input_writer.py`: mapping compartment/vent/fire/boundary.
- `cfast_sim/batch_runner.py`: subprocess, timeout, retry, resume.
- `cfast_sim/postprocess.py`: raw -> schema chuẩn.

## Label P0

Không viết lại công thức trong module. Gọi `shared.labels` với config: obscuration threshold 23.93 %/m, persistence 2 bước theo đề cương mặc định; mọi thay đổi phải tăng `label_rule_version`.

## Rủi ro cần xử lý

- Mapping graph-CFAST không hợp lệ.
- Tên compartment/vent vượt giới hạn định dạng.
- Scenario lỗi không được làm hỏng toàn batch.
- Output thiếu cột hoặc timestep phải fail validation rõ ràng.
- Không gán TTA giả cho node không đạt ngưỡng.

## Test tối thiểu

- Sampler tái lập với seed.
- Một `base_scenario_id` duy nhất cho các noise variant.
- Writer tạo file deterministic.
- Runner mock exit code/timeout.
- Label test tại biên ngưỡng và persistence.

## DoD

10-20 scenario debug chạy được; sau đó batch 100-200 case tùy phần cứng. Mỗi case có manifest, log và output hợp lệ hoặc trạng thái lỗi giải thích được.
