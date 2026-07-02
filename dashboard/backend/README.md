# Dashboard backend

FastAPI cung cấp artifact đã chuẩn hóa và model inference. Backend không parse raw CFAST/FDS trong request. Ưu tiên hoàn thành API schema/test trước frontend.

Run:

```cmd
pip install -e ".[api]"
uvicorn dashboard.backend.app.main:app --reload
```
