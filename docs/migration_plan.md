# Kế hoạch di chuyển từ layout hiện tại

Thực hiện trên nhánh mới và commit theo từng bước.

```cmd
git checkout -b chore/restructure-repo
mkdir src\fire_smoke_dt

git mv src\bim_graph src\fire_smoke_dt\bim_graph
git mv src\scenario src\fire_smoke_dt\scenario
git mv src\cfast_sim src\fire_smoke_dt\cfast_sim
git mv src\fds_sim src\fire_smoke_dt\fds_sim
git mv src\iot_sim src\fire_smoke_dt\iot_sim
git mv src\dataset src\fire_smoke_dt\dataset
git mv src\models src\fire_smoke_dt\models
git mv src\training src\fire_smoke_dt\training
git mv src\comparison src\fire_smoke_dt\comparison
git mv src\common src\fire_smoke_dt\shared
```

Sau đó chạy:

```cmd
scripts\bootstrap_repo.cmd .
scripts\check.cmd
scripts\test.cmd
git status
```

Nếu các file hiện tại đã có nội dung thật, không dùng `--force`. Bootstrap mặc định chỉ tạo file thiếu và không ghi đè file không rỗng.

## Mapping tên file

- `configs/iot_presets.yaml` -> `configs/noise_presets.yaml`.
- `src/cfast_sim/postprocess.py` giữ tên ngắn hoặc đổi `post_processing.py`; chọn một kiểu và dùng thống nhất.
- `src/fds_sim/postprocess.py` gọi chung label logic từ `shared.labels`.
- `src/comparison/metrics.py` chỉ chứa alignment/metrics; không chứa model evaluation chung.
- `src/training/evaluate.py` chịu trách nhiệm metrics AI và ablation.
