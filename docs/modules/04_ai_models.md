# Module 04 - AI Models + Training

**Chủ trì:** Nguyễn Thùy Dương. **Reviewer chéo:** Nguyễn Thu Hương / Đào Ngọc Long.

## Mục tiêu

Xây dựng lộ trình từ baseline đến BAT-GNN để kiểm tra đóng góp của graph, lịch sử IoT, điều kiện biên và trạng thái hệ thống.

## Baseline bắt buộc P0

1. Rule-based graph spread.
2. Non-graph temporal: LSTM/GRU/TCN đơn giản.
3. Graph baseline: GCN/GraphSAGE/GAT.
4. Temporal GNN.
5. BAT-GNN là mô hình chính nếu đủ tiến độ.

## Input hợp lệ tại thời điểm t

Graph và feature tĩnh; scenario config đã biết; nguồn cháy/HRR đã biết; boundary/system/door state đến t; lịch sử IoT `[t-k,t]`. Không dùng target hay mô phỏng tương lai.

## Output P0

- `smoke_label(node, t+horizon)` hoặc probability.
- `time_to_arrival(node,t)` với masked regression.

## Loss và metrics

- BCE/Focal cho smoke.
- Masked MAE/Huber cho TTA.
- F1, Recall, Precision, AUC.
- MAE/RMSE trên `arrival_valid_mask`.
- Inference time và robustness metric drop.

Recall được ưu tiên hơn Accuracy; mọi trade-off F1/Recall và MAE phải báo cáo trung thực.

## Ablation bắt buộc

- Không graph.
- Graph không IoT.
- Graph + IoT.
- Full không boundary.
- Full không system.
- Full model.

## File cần viết

- `models/baselines/*.py`, `models/temporal_gnn.py`, `models/bat_gnn.py`.
- `training/losses.py`, `training/train.py`, `training/evaluate.py`, `training/metrics.py`.

## Reproducibility

Lưu seed, config snapshot, split id/hash, feature manifest, code commit, checkpoint hash và metric JSON. Không chỉ lưu ảnh biểu đồ.

## DoD

Bảng baseline trên cùng split; BAT-GNN chỉ được kết luận tốt hơn khi F1/Recall tăng và MAE không xấu hơn hoặc trade-off được báo cáo rõ. Inference phải được benchmark trên cùng phần cứng với CFAST comparison.
