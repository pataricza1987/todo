# TODO (FastAPI + Streamlit + PostgreSQL)

## Futtatás

### 1) venv + csomagok
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### 2) .env
```bash
cp .env .env
```
Állítsd be a `DATABASE_URL`-t a saját PostgreSQL-edhez.

### 3) Backend
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4) Frontend
Új terminálban (ugyanabban a venv-ben):
```bash
streamlit run frontend/app.py
```

### 5) Tesztek
```bash
pytest -q
```

## Végpontok
- `GET /todos` (lista)
- `GET /todos/{id}` (részletek)
- `POST /todos` (létrehozás)
- `PATCH /todos/{id}` (módosítás)
- `DELETE /todos/{id}` (törlés)
- `POST /todos/{id}/enrich` (API-hívás lánc: külső quote API → DB)
- `GET /stats` (statisztika)
