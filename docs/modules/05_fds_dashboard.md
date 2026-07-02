# Module 05 - FDS Validation + Comparison + Dashboard

**Chủ trì:** Đào Ngọc Long. **Reviewer chéo:** Võ Nguyễn Anh Kiệt.

## Vì sao tách code

FDS, comparison và dashboard cùng owner nhưng không cùng dependency. Giữ ba khu vực riêng: `fds_sim`, `comparison`, `dashboard`. Dashboard không được import parser FDS trực tiếp; chỉ đọc artifact chuẩn hóa/API service.

## FDS reference set

P0 tối thiểu:

- FDS-01: phòng -> hành lang.
- FDS-02: hành lang dài.
- FDS-03: phòng -> hành lang -> cầu thang.

Cùng hình học rút gọn, nguồn cháy, điều kiện biên, sensor location/height, `dt_out` và label rule với CFAST. FDS là mô hình tham chiếu số, không phải ground truth thí nghiệm và không trộn vào train chính.

## Alignment/metrics

- Sensor quantity so tại cùng vị trí/cao độ.
- Chuỗi nội suy về cùng `dt_out`.
- Upper-layer comparison chỉ khi có quy tắc aggregation rõ.
- Metrics: F1/Recall/Precision smoke label; MAE/RMSE arrival; MAE/RMSE/correlation sensor series.

## Dashboard P0

- Graph filter theo tầng.
- Sensor state và timeline replay.
- Smoke probability và TTA per node.
- AI/CFAST/FDS comparison khi có reference.
- API endpoints: scenarios, graph, timeseries, labels, inference, comparison, stream.

## File cần viết

- `fds_sim/input_writer.py`, `fds_sim/postprocess.py`, `fds_sim/cases.py`.
- `comparison/alignment.py`, `comparison/metrics.py`.
- FastAPI routers và schema ở `dashboard/backend`.
- React/Cytoscape/ECharts ở `dashboard/frontend` sau khi API ổn định.

## Test tối thiểu

- Alignment cùng timestep/sensor.
- Metric mask hợp lệ.
- API schema test bằng TestClient.
- Inference rejects future timestamps/invalid feature window.
- Dashboard không hiển thị artifact thiếu provenance.

## DoD

Một FDS pilot sớm để khóa alignment; 3 case P0 chuẩn hóa; backend API trước frontend; replay một scenario end-to-end.
