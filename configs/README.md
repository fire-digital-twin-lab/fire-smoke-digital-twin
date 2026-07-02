# Config contracts

Mọi module đọc config qua một loader chung. Sửa config dùng PR có reviewer chéo vì thay đổi có thể làm dataset/model không tương thích.

- Không đổi nghĩa field mà giữ nguyên version.
- Không hard-code bản sao trong code.
- Config dùng đơn vị trong tên field hoặc mô tả rõ đơn vị.
