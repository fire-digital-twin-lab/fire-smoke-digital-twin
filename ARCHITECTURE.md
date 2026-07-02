# Kiến trúc đề xuất

## 1. Quyết định chính

Repo dùng một namespace Python duy nhất: `fire_smoke_dt`.

Không đặt các package tên chung như `common`, `models`, `dataset`, `training` trực tiếp dưới `src/`, vì dễ xung đột import với thư viện bên ngoài và làm `pyproject.toml` khó cấu hình. Các package kỹ thuật vẫn được giữ riêng để đảm bảo độ kết dính:

- `scenario` không bị nhét vào `cfast_sim`, vì FDS cũng cần dùng cùng scenario.
- `fds_sim`, `comparison` và `dashboard` vẫn tách riêng dù cùng một người phụ trách.
- `iot_sim` tách khỏi `dataset`: một bên tạo stream cảm biến, một bên đóng gói dữ liệu ML.
- `models` tách khỏi `training`: mô hình không phụ thuộc vòng lặp train.

Phân công theo người được quản lý bằng `MODULE_OWNERS.md`, `CODEOWNERS` và tài liệu trong `docs/modules/`, không ép code thành thư mục theo tên người.

## 2. Luồng phụ thuộc

```text
shared <- configs
bim_graph -> scenario -> cfast_sim -> iot_sim -> dataset -> models -> training
                |             |                     |
                +----------> fds_sim -> comparison <-+
                                                  -> dashboard
```

Quy tắc: package bên trái không được import package bên phải. `shared` không import module nghiệp vụ.

## 3. Hợp đồng dữ liệu

Các điểm nối phải được kiểm tra schema trước khi ghi output:

1. IFC parser -> bảng BIM thô.
2. Graph builder -> `building_graph.json`, `node_map.csv`, `edge_map.csv`.
3. Scenario generator -> scenario catalog và từng scenario config.
4. CFAST/FDS post-processing -> chuỗi node/sensor đã chuẩn hóa.
5. Label logic -> label P0 và mask.
6. IoT simulator -> stream sạch/noisy/faulty.
7. Dataset builder -> parquet + split manifest + PyG object.
8. Model inference -> xác suất khói, TTA, mask và metadata model.

Chi tiết ở `docs/data_contracts.md`.

## 4. Quy tắc chia config

- `scenario_schema.yaml`: field và miền giá trị kịch bản.
- `sensor_schema.yaml`: vị trí/cao độ/loại cảm biến dùng chung CFAST và FDS.
- `label_rules.yaml`: duy nhất một nguồn định nghĩa label P0.
- `noise_presets.yaml`: preset suy giảm IoT.
- `split_rules.yaml`: split theo `base_scenario_id`.
- `schema_version.yaml`: version tất cả contract.

Không hard-code ngưỡng label, forecast horizon, tên cột hoặc preset trong module.

## 5. Kiểm thử

- Unit test: hàm thuần, parser nhỏ, noise, label, metric.
- Contract test: schema output module trước có hợp lệ với module sau.
- Integration test: pipeline debug layout nhỏ, không cần CFAST/FDS trong CI mặc định.
- Smoke test tùy chọn: chỉ chạy khi máy có biến môi trường trỏ tới binary CFAST/FDS.
