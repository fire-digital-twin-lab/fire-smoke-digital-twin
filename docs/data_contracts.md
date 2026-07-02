# Hợp đồng dữ liệu giữa các module

## Nguyên tắc chung

Mọi bảng phải có `schema_version`. Artifact theo scenario phải có `building_id`, `scenario_id`, `base_scenario_id`. Output hậu xử lý phải có `post_processing_version` và `label_rule_version`.

## Building graph

`building_graph.json`:

- `nodes[]`: `node_id`, `ifc_global_id`, `node_type`, `floor_id`, `area_m2`, `volume_m3`, `ceiling_height_m`.
- `edges[]`: `edge_id`, `source`, `target`, `edge_type`, `opening_area_m2`, `opening_height_m`, `is_vertical`.
- `metadata`: building id, IFC version, graph version, manual corrections.

`node_map.csv` và `edge_map.csv` phục vụ truy vết BIM-graph. `building_graph.graphml` chỉ dùng debug/visualization, không phải contract chính.

## Scenario catalog

Mỗi row/config gồm:

- `scenario_id`, `base_scenario_id`, `building_id`;
- `fire_node`, `fire_floor`, HRR/growth/soot config;
- door/system/boundary config;
- `t_end_s`, `dt_out_s`;
- seed lấy mẫu, version config.

Biến thể nhiễu không tạo `base_scenario_id` mới.

## Time-series chuẩn hóa

Khóa chính khuyến nghị: `(scenario_id, time_s, node_id)` hoặc `(scenario_id, time_s, sensor_id)`.

Các bảng chính:

- `node_dynamic.parquet`;
- `edge_dynamic.parquet`;
- `boundary_dynamic.parquet`;
- `virtual_sensor_clean.parquet`;
- `iot_noisy_stream.parquet`;
- `labels.parquet`.

## Label P0

- `smoke_label`: 0/1 tại `t + forecast_horizon` cho target phân loại.
- `arrival_time_abs_s`: thời điểm đầu tiên đạt điều kiện duy trì.
- `time_to_arrival_s`: `max(arrival_time_abs_s - t, 0)`.
- `arrival_valid_mask`: 1 nếu node đạt ngưỡng trong thời gian mô phỏng.

Ngưỡng và số bước duy trì chỉ đọc từ `configs/label_rules.yaml`.

## Dataset split

`splits/<split_id>.json` chứa danh sách `base_scenario_id` cho train/val/test và hash của catalog. Không split theo từng time window và không để biến thể noise của một base scenario rơi sang tập khác.

## Prediction contract

Inference trả:

- `scenario_id`, `prediction_time_s`, `forecast_horizon_s`, `model_id`;
- per-node `smoke_probability`, `smoke_label_pred`, `time_to_arrival_pred_s`, `tta_valid_probability` nếu dùng;
- `schema_version`, checkpoint hash và feature manifest.
