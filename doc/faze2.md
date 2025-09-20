# PortfoView-Py – FÁZE 2 (Kvalita & CI)

## Cíl fáze

Zavést základní kvalitu projektu: **automatické testy, formátování, lint a CI**.
Hotovo je, když testy běží lokálně i v Dockeru, hooky hlídají styl při commitu a GitHub Actions spouští lint + testy na každém pushi/PR.

---

## 1) Testování (pytest)

### 1.1 Závislosti

* Úprava: `requirements.txt`

  ```
  fastapi
  uvicorn[standard]
  pytest
  httpx
  ```

  **Proč:** `pytest` = test runner; `httpx` vyžaduje `TestClient` (Starlette).

### 1.2 První test endpointu `/healthz`

* Nový soubor: `tests/test_healthz.py`

  ```python
  from fastapi.testclient import TestClient
  from app.main import app

  client = TestClient(app)

  def test_healthz_returns_ok():
      r = client.get("/healthz")
      assert r.status_code == 200
      assert r.json() == {"status": "ok"}
  ```

### 1.3 Nastavení importů pro pytest

* Nový soubor: `app/__init__.py` (prázdný) – z adresáře `app/` udělá Python balíček.
* Nový soubor: `pytest.ini`

  ```
  [pytest]
  pythonpath = .
  addopts = -q
  ```

### 1.4 Spuštění testů

* **Lokálně (venv):**

  ```bash
  pip install -r requirements.txt
  pytest -q
  ```
* **Přes Docker:**

  ```bash
  docker compose build
  docker compose run --rm web pytest -q
  ```

**Očekávání:** `1 passed in …s`.

> Typické chyby a opravy:
> `ModuleNotFoundError: httpx` → doplnit `httpx` do requirements.
> `No module named 'app'` → přidat `app/__init__.py` a `pytest.ini (pythonpath = .)`.

---

## 2) pre-commit (Black, Ruff) + EditorConfig

### 2.1 Instalace nástrojů

```bash
pip install pre-commit black ruff
```

### 2.2 Konfigurace

* Nový soubor: `pyproject.toml`

  ```toml
  [tool.black]
  line-length = 100
  target-version = ["py313"]

  [tool.ruff]
  line-length = 100
  target-version = "py313"
  select = ["E", "F", "I"]  # errors, flakes, importy
  ```
* Nový soubor: `.pre-commit-config.yaml`

  ```yaml
  repos:
    - repo: https://github.com/psf/black
      rev: 24.8.0
      hooks:
        - id: black

    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.6.9
      hooks:
        - id: ruff
          args: ["--fix"]

    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v4.6.0
      hooks:
        - id: trailing-whitespace
        - id: end-of-file-fixer
        - id: check-added-large-files
  ```
* Nový soubor: `.editorconfig`

  ```
  root = true

  [*]
  charset = utf-8
  end_of_line = lf
  insert_final_newline = true
  trim_trailing_whitespace = true
  indent_style = space
  indent_size = 4
  ```

### 2.3 Aktivace a první běh

```bash
pre-commit install
pre-commit run --all-files
# pokud upraví soubory -> spustit znovu, až vše "Passed"
```

**Pozn.:** Když hook něco opraví, commit se z bezpečnosti zruší. Proveď `git add -A` a commit znovu.

---

## 3) GitHub Actions CI (lint + test)

### 3.1 Workflow

* Nový soubor: `.github/workflows/ci.yml`

  ```yaml
  name: CI

  on:
    push:
    pull_request:

  jobs:
    test:
      runs-on: ubuntu-latest
      strategy:
        matrix:
          python-version: ["3.13"]
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: ${{ matrix.python-version }}
            cache: "pip"
        - name: Install deps
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
            pip install black ruff
        - name: Ruff (lint)
          run: ruff check .
        - name: Black (format check)
          run: black --check .
        - name: Pytest
          run: pytest -q
  ```

### 3.2 Ověření běhu

* Vytvoření PR z větve `feature/ci` → `main`.
* Záložka **Checks** na PR / karta **Actions** v repu → běh jobu „test (3.13)“.
* **Zelené kroky:** Ruff ✓, Black (check) ✓, Pytest ✓.

### 3.3 (Volitelně) Ochrana `main`

* *Settings → Branches → Add rule* pro `main`:

  * **Require a pull request before merging**
  * **Require status checks to pass** → vybrat `CI / test (3.13)`.

---

## 4) Stav na konci FÁZE 2 (Definition of Done)

* ✅ `pytest -q` zelený lokálně i v Dockeru (1 test `/healthz` → 200 + `{"status":"ok"}`).
* ✅ `pre-commit` aktivní; Black/Ruff/EditorConfig běží při každém commitu.
* ✅ GitHub Actions CI na `push` i `pull_request`: Ruff + Black check + Pytest vše zelené.
* ✅ (Volitelně) `main` chráněná: merge jen přes PR se zelenou CI.

---

## 5) Evidence — typické výstupy

```
$ pytest -q
1 passed in 0.3s

$ pre-commit run --all-files
black....................Passed
ruff.....................Passed
trim trailing whitespace.Pass
end-of-file-fixer.......Passed

$ git log -1 --name-only
chore: add CI workflow (ruff, black --check, pytest)
.github/workflows/ci.yml

# GitHub → PR → Checks
CI / test (3.13) — Success
  ✓ Ruff (lint)
  ✓ Black (format check)
  ✓ Pytest
```

---

## 6) Co následuje

➡️ **FÁZE 3 – Datový model & DB (SQLite + SQLAlchemy + Alembic)**

* Základ DB (`app/database.py`), inicializace Alembicu, první model `Symbol`, první migrace.

---
