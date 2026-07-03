# Fire Smoke Digital Twin

Prototype nghiên cứu end-to-end cho bài toán dự báo lan truyền khói cấp phòng/khu vực:

`BIM/IFC -> Building Graph -> Scenario -> CFAST/FDS -> Virtual IoT -> Dataset -> AI -> Dashboard`

## Phạm vi P0

- Chuyển IFC thành building graph có truy vết về `GlobalId`.
- Sinh và chạy batch kịch bản CFAST.
- Tạo ba lớp dữ liệu: `physics_truth`, `virtual_sensor_clean`, `iot_noisy_stream`.
- Dự báo hai đầu ra bắt buộc:
  - `smoke_label(node, t + horizon)`;
  - `time_to_arrival(node, t)` cùng `arrival_valid_mask`.
- Đối sánh chọn lọc với FDS; FDS không được trộn vào tập train CFAST.
- Dashboard chỉ dùng để replay, inference và so sánh; không điều khiển PCCC thật.

## Cấu trúc chính

```text
configs/                     Cấu hình dùng chung
src/fire_smoke_dt/shared/    Schema, I/O, validation, label logic
src/fire_smoke_dt/bim_graph/ IFC -> graph
src/fire_smoke_dt/scenario/  Catalog kịch bản có kiểm soát
src/fire_smoke_dt/cfast_sim/ Writer, runner, hậu xử lý CFAST
src/fire_smoke_dt/fds_sim/   Case tham chiếu và hậu xử lý FDS
src/fire_smoke_dt/comparison/Đối sánh CFAST-FDS và AI-FDS
src/fire_smoke_dt/iot_sim/   Nhiễu, trễ, missing, fault
src/fire_smoke_dt/dataset/   Dataset graph-time-series và split
src/fire_smoke_dt/models/    Baseline, Temporal GNN, BAT-GNN
src/fire_smoke_dt/training/  Train, loss, evaluate, ablation
dashboard/                   FastAPI và frontend
tests/                       Unit + integration, mirror theo package
docs/modules/                Mô tả chi tiết theo 5 workstream
```

## Cài đặt nhanh trên Windows

```cmd
py -3.11 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Các dependency nặng như `IfcOpenShell`, `PyTorch`, `PyTorch Geometric`, CFAST và FDS nên được cài theo README của module tương ứng; không buộc toàn nhóm cài mọi thứ ở tuần đầu.

## Kiểm tra

```cmd
scripts\check.cmd
scripts\test.cmd
```

## Quy tắc dữ liệu

- Không commit IFC lớn, output CFAST/FDS, parquet dataset, checkpoint hoặc log batch.
- Mỗi artifact phải có `schema_version`, `post_processing_version`, `label_rule_version` và `base_scenario_id` khi áp dụng.
- Mọi biến thể `noise_seed` của cùng `base_scenario_id` phải nằm trong cùng split.
- Không dùng dữ liệu sau thời điểm `t` hoặc label làm input AI.

Đọc tiếp: [ARCHITECTURE.md](ARCHITECTURE.md), [SCOPE.md](SCOPE.md), [CONTRIBUTING.md](CONTRIBUTING.md), [docs/repo_review.md](docs/repo_review.md).
