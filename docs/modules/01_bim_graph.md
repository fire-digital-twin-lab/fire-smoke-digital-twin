# Module 01 - BIM/IFC-to-Graph

**Chủ trì:** Trần Phùng Đức Anh. **Reviewer chéo:** Nguyễn Thu Hương.

## Mục tiêu

Chuyển file IFC thành building graph cấp phòng/khu vực có thể dùng cho scenario, mô phỏng và GNN. Module phải tự động tối đa nhưng luôn giữ khả năng truy vết và fallback thủ công.

## Input

- IFC4 ưu tiên, IFC2x3 fallback.
- Quy ước export Revit và file ghi chú chất lượng model.
- Optional manual correction CSV/YAML.

## Entity cần xử lý

`IfcBuildingStorey`, `IfcSpace`, `IfcDoor`, `IfcWindow`, `IfcStair`, `IfcRelSpaceBoundary`; tường/sàn chỉ lấy thuộc tính cần thiết. Không nối chuỗi nhiều loại entity rồi xử lý chung.

## Output bắt buộc

- `building_graph.json` - contract chính.
- `building_graph.graphml` - debug/visualization.
- `node_map.csv`, `edge_map.csv` - truy vết `GlobalId`.
- `graph_check_report.md` - connected components, isolated nodes, thiếu edge, chỉnh sửa thủ công.

## File cần viết

- `ifc_parser.py`: parse entity và quantity/property; không xây graph.
- `graph_builder.py`: chuyển bảng chuẩn hóa thành NetworkX graph.
- `topology_check.py`: kiểm tra và sinh report.
- `fallback_manual_graph.py`: dựng graph từ room/door list khi IFC lỗi.

## Quy tắc kỹ thuật

- Node id nội bộ ổn định, không dùng tên phòng làm khóa duy nhất.
- Giữ `ifc_global_id` để trace.
- Edge phải chỉ rõ loại và chiều đứng/ngang.
- Manual correction phải được version hóa và ghi trong metadata.
- Không phụ thuộc CFAST/FDS/PyTorch.

## Test tối thiểu

- Fixture 3 phòng + hành lang + cầu thang.
- Door nối đúng hai space.
- Isolated node được phát hiện.
- Fallback tạo graph cùng schema.
- Serialize/deserialize không mất thuộc tính.

## DoD

Graph chạy được trên debug layout và case IFC chính; report topology không còn lỗi chưa giải thích; output qua `shared.validation`.
