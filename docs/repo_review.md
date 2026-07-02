# Review repo hiện tại và quyết định giữ / sửa / bỏ

Snapshot review: 2026-07-03, branch `main`.

## Kết luận

Repo hiện tại là một skeleton hợp lý về tên miền kỹ thuật nhưng hầu hết file quan trọng đang rỗng. Vì chưa có code thật, đây là thời điểm tốt nhất để chuẩn hóa namespace, contract dữ liệu và ownership; chi phí di chuyển gần như bằng không.

## Giữ

| Thành phần hiện tại | Lý do giữ |
|---|---|
| `configs/` | Đúng hướng: tách factor, label, split và model config khỏi code. |
| `src/bim_graph`, `scenario`, `cfast_sim`, `fds_sim`, `iot_sim`, `dataset`, `models`, `training`, `comparison` | Ranh giới kỹ thuật tương đối tốt và bám pipeline đề cương. |
| `dashboard/` riêng | Dashboard không nên nằm trong package mô phỏng FDS. |
| `data/`, `outputs/`, `notebooks/`, `docs/`, `scripts/`, `tests/` | Cần thiết cho repo nghiên cứu, miễn có quy tắc rõ. |
| `.github/workflows/` | Đúng vị trí để triển khai CI. |

## Sửa ngay

| Vấn đề | Hành động |
|---|---|
| Các package chung nằm trực tiếp dưới `src/` | Bọc toàn bộ trong `src/fire_smoke_dt/`. |
| Thiếu `__init__.py` và README package | Thêm cho mọi package. |
| `common` quá mơ hồ | Đổi thành `shared`, giới hạn chỉ schema/I/O/validation/label/path/logging. |
| Config đang rỗng | Điền schema có version và test parse YAML. |
| Label logic có nguy cơ bị viết lặp | Chỉ có `shared/labels.py`; CFAST/FDS cùng gọi. |
| Chưa có contract | Thêm `docs/data_contracts.md` và integration test. |
| Chưa có ownership | Thêm `MODULE_OWNERS.md` và `.github/CODEOWNERS`. |
| Chưa có chiến lược split | Split theo `base_scenario_id`, khóa mọi `noise_seed` cùng split. |
| Chưa có CI thực chất | CI chạy ruff + pytest; test external simulator tách khỏi CI mặc định. |
| `requirements.txt` và `pyproject.toml` dễ lệch | Dùng `pyproject.toml` làm nguồn chính; requirements chỉ là bootstrap. |

## Bỏ hoặc chưa nên dùng

| Thành phần | Quyết định |
|---|---|
| `Makefile` rỗng | Bỏ nếu nhóm chủ yếu Windows; thay bằng `scripts/*.cmd`. Chỉ thêm lại khi CI/Linux thực sự cần. |
| Commit nội dung `data/` và `outputs/` | Bỏ; chỉ giữ README và `.gitkeep`. |
| Notebook dùng như production code | Không dùng; notebook chỉ cho khám phá, logic phải chuyển về `src/`. |
| Gộp FDS và dashboard thành một package | Không làm. Có thể cùng owner nhưng phải tách dependency. |
| Tạo thư mục code cấp cao `module_01_...` đến `module_05_...` | Không cần. Dùng package kỹ thuật + CODEOWNERS; tránh import dài và trùng logic. |
| Full Cartesian product cho scenario | Không làm; dùng controlled sampling và catalog có metadata. |
| FDS data trong tập train chính | Không làm; giữ làm reference set độc lập. |

## Ưu tiên 3 PR đầu

1. `chore/repo-contracts`: namespace, configs, shared schema/label/validation, CI.
2. `feat/bim-graph/minimal-pipeline`: fixture IFC/debug graph, output contract, topology report.
3. `feat/scenario-cfast/debug-case`: scenario catalog 10-20 case và một CFAST case nhỏ chạy end-to-end.
