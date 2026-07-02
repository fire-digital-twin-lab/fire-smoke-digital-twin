# Hướng dẫn đóng góp

## Nhánh

- `main`: luôn import được và test P0 không đỏ.
- Nhánh làm việc: `feature/<module>/<short-task>` hoặc `fix/<module>/<short-task>`.
- Không duy trì một nhánh feature sống nhiều tháng; mỗi PR nên nhỏ và có DoD rõ.

## PR bắt buộc có

- Mục tiêu và module bị ảnh hưởng.
- Input/output contract thay đổi hay không.
- Test đã chạy.
- Artifact mẫu nhỏ nếu có.
- Reviewer chéo theo `MODULE_OWNERS.md`.

## Quy ước code

- Python có type hint và docstring cho public API.
- Không đọc file bằng đường dẫn rải rác; dùng `shared.paths`.
- Không tự định nghĩa lại tên cột; dùng `shared.schema`.
- Không copy label logic giữa CFAST và FDS; dùng `shared.labels`.
- Không commit dữ liệu lớn hoặc checkpoint.

## Definition of Done chung

- Code chạy trên fixture nhỏ.
- Output qua validation.
- Có test cho lỗi quan trọng.
- README module cập nhật nếu contract thay đổi.
- Không tạo label leakage hoặc split leakage.
