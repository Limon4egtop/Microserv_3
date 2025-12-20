- **Pascal-Legacy** переписан на Python: генерация CSV с типами (timestamp, ИСТИНА/ЛОЖЬ, числа, текст), визуализация CSV как таблицы, экспорт в **.xlsx** с подстановкой значений даты/времени.
- **Backend в Docker**: FastAPI сервис с **Rate-Limit**, **Redis** (кэш/лимитер), валидацией через отдельные классы (Pydantic), слоистой структурой `routes/ handlers/ services/ clients/ repo/ domain/ config/`.
- **Диаграммы/блок-схемы** в `docs/` (Mermaid).
- **Тесты** (pytest) для CSV/XLSX и rate-limit.

> Примечание: исходная работа описывает Rust/Laravel/Pascal. Здесь сделана эквивалентная по смыслу реализация на Python, чтобы вы могли приложить код и демонстрацию в одном архиве.

## Быстрый старт (Docker)

```bash
docker compose up --build
```

Откроется:
- API: http://localhost:8000 (Swagger: /docs)
- Redis: внутри compose
- Postgres: внутри compose (опционально — используется репозиторием)

## Локальный запуск (без Docker)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export APP_ENV=dev
uvicorn app.main:app --reload
```

## Legacy утилита (CSV/XLSX)

```bash
python -m legacy generate --rows 50 --out ./data/sample.csv
python -m legacy view --csv ./data/sample.csv
python -m legacy to-xlsx --csv ./data/sample.csv --out ./data/sample.xlsx
```

## Тесты

```bash
pytest -q
```

## Структура

- `app/` — API (routes/handlers/services/clients/repo/domain/config)
- `legacy/` — утилита генерации/визуализации CSV и экспорта XLSX
- `docs/` — диаграммы (Mermaid)
- `tests/` — тесты
