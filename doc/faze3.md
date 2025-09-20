# 📄 Dokumentace – Fáze 3 (Datový model & DB)

## Cíl fáze

* Zavést databázovou vrstvu (SQLite + SQLAlchemy).
* Přidat ORM modely `User`, `Symbol`, `Transaction`.
* Nastavit migrace přes Alembic.
* Připravit seed dat.
* Implementovat CRUD endpointy pro `Transaction` (GET, POST, DELETE).
* Pokrýt testy (PyTest).

---

## Postup

### 3.1 Základ DB vrstvy

* Do `requirements.txt` přidán balíček `SQLAlchemy`.
* Vytvořen soubor `app/database.py` s:

  * `engine` (SQLite v `./data/app.db`),
  * `SessionLocal`,
  * `Base`.
* Přidán mount `./data:/app/data` do `docker-compose.yml`.
* Ověření připojení příkazem:

  ```bash
  docker compose run --rm web sh -lc "python - << 'PY'
  from app.database import engine
  from sqlalchemy import text
  with engine.connect() as conn:
      print(conn.execute(text('SELECT 1')).scalar())
  PY"
  ```

  → výstup `1`.

### 3.2 ORM modely

* Vytvořen soubor `app/models.py`.
* Definovány modely:

  * `User` – id, username, vztah k transakcím,
  * `Symbol` – id, ticker, asset\_type (Enum), vztah k transakcím,
  * `Transaction` – id, FK na user a symbol, quantity, price, date (aware UTC datetime).
* Ověřeno vytvoření tabulek:

  ```bash
  docker compose run --rm web sh -lc "python - << 'PY'
  from sqlalchemy import inspect
  from app.database import Base, engine
  import app.models
  Base.metadata.create_all(bind=engine)
  print(inspect(engine).get_table_names())
  PY"
  ```

  → výstup: `['users', 'symbols', 'transactions', '_init']`.

### 3.3 Alembic migrace

* Do `requirements.txt` přidán balíček `alembic`.
* Inicializace:

  ```bash
  docker compose run --rm -v "$PWD":/app -w /app web alembic init migrations
  ```
* Úpravy:

  * `alembic.ini` → `sqlalchemy.url = sqlite:///data/app.db`,
  * `migrations/env.py` → `target_metadata = Base.metadata`, import `app.models`.
* První migrace:

  ```bash
  docker compose run --rm web alembic revision --autogenerate -m "init schema"
  docker compose run --rm web alembic upgrade head
  ```
* DB obsahuje i tabulku `alembic_version`.

### 3.4 Seed dat

* Vytvořen soubor `app/seed.py`, který:

  * vloží 1 demo usera,
  * 2 symboly (AAPL, VWCE),
  * 2 transakce.
* Ověření spuštěním:

  ```bash
  docker compose run --rm web python -m app.seed
  ```

  → `Seed OK`.
* V DB následně: `Users: ['demo']`, `Symbols: ['AAPL', 'VWCE']`, `Transactions: [(1, 10, 150), (2, 5, 100)]`.
* Přidán test `tests/test_seed.py` → zelený.

### 3.5 CRUD endpointy pro Transaction

* Vytvořeny soubory:

  * `app/schemas.py` – Pydantic schémata `TransactionRead`, `TransactionCreate`,
  * `app/routers/transactions.py` – router s GET, POST, DELETE,
  * `app/main.py` – připojení routeru.
* **GET /api/transactions** → vrací seznam transakcí.
* **POST /api/transactions** → vloží novou transakci (201), validace existujících user/symbol.
* **DELETE /api/transactions/{id}** → smaže transakci (204) nebo vrátí 404.
* Ověřeno přes Swagger UI i curl.

### Testy endpointů

* `tests/test_transactions_get.py` – kontrola, že GET vrací seeded data.
* `tests/test_transactions_post.py` – happy path (201), invalid FK (400).
* `tests/test_transactions_delete.py` – happy path (204), not found (404).
* Spuštění:

  ```bash
  docker compose run --rm web pytest -q
  ```

  → všechny testy zelené, bez warnings.

---

## DoD (Definition of Done)

* [x] SQLite databáze funkční (`data/app.db`).
* [x] ORM modely `User`, `Symbol`, `Transaction`.
* [x] Alembic repo + první migrace.
* [x] Seed dat (User, 2× Symbol, 2× Transaction).
* [x] CRUD endpointy pro Transaction (GET/POST/DELETE).
* [x] 6+ testů (seed + CRUD) zelených v PyTestu.
* [x] Žádné warnings z `datetime.utcnow()`.

---

📌 **Fáze 3 splněna.** Projekt má nyní plnohodnotnou databázovou vrstvu, migrace, seed a první API CRUD.
