# PortfoView-Py – FÁZE 1 (Skeleton aplikace + Docker)

## Cíl fáze
Lokálně spustit **Hello API** ve FastAPI, zabalené v Dockeru.
Ověřit běh přes endpoint `/healthz` (200 OK).

---

## 1) Struktura projektu
- `app/main.py` – hlavní aplikace s endpointem `/healthz`
- `requirements.txt` – seznam Python závislostí
- `Dockerfile` – definice Docker image
- `.dockerignore` – ignorace nepotřebných souborů
- `docker-compose.yml` – konfigurace služby `web`

**Proč:**
Abychom měli minimální kostru projektu, kterou dokáže Docker spustit a která se dá dále rozšiřovat.

---

## 2) Implementace FastAPI aplikace
Soubor `app/main.py`:
```python
from fastapi import FastAPI

app = FastAPI(title="PortfoView-Py")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
````

**Proč:**

* `FastAPI()` inicializuje aplikaci.
* Dekorátor `@app.get("/healthz")` přiřadí funkci k HTTP GET endpointu `/healthz`.
* Funkce vrací JSON `{"status": "ok"}`, což slouží jako health check.

---

## 3) Definice závislostí

Soubor `requirements.txt`:

```
fastapi
uvicorn[standard]
```

**Proč:**

* `fastapi` = framework pro API.
* `uvicorn[standard]` = server + užitečné extra balíčky (watchfiles, httptools, uvloop…).

---

## 4) Dockerfile

Soubor `Dockerfile`:

```dockerfile
FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Proč:**

* `slim` image je malý a rychlý.
* Rozdělení kopií: nejdřív `requirements.txt` (keš instalace), pak zdrojáky.
* `--reload` → v dev režimu se změny kódu ihned projeví.

---

## 5) .dockerignore

Soubor `.dockerignore`:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
.git/
.gitignore
.env
```

**Proč:**
Zabránili jsme, aby se do image kopírovaly nepotřebné soubory (cache, git historie, secrets).
Image je menší, build rychlejší a bezpečnější.

---

## 6) Docker Compose

Soubor `docker-compose.yml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app:rw
    restart: unless-stopped
```

**Proč:**

* `docker compose up` místo ručního build/run.
* Volume umožňuje hot reload kódu bez rebuildu image.
* Restart policy → kontejner se zvedne po pádu.

---

## 7) Spuštění

```bash
docker compose up --build
```

**Očekávaný log:**

```
Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 8) Ověření běhu

* `curl http://localhost:8000/healthz` →
  `{"status":"ok"}`
* Swagger dokumentace: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Stav na konci FÁZE 1 (Definition of Done)

* ✅ Projekt má základní strukturu.
* ✅ V Dockeru běží FastAPI aplikace.
* ✅ Endpoint `/healthz` funguje a vrací **200 OK**.
* ✅ Swagger UI dostupný na `/docs`.

---

## 9) Co následuje

➡️ **Fáze 2 – kvalita & CI**

* přidat pytest a první test `test_healthz.py`
* nastavit pre-commit hooky (Black, Ruff, EditorConfig)
* připravit GitHub Actions workflow (`ci.yml`)
* cíl: push do repa spustí CI a projde zeleně

```

---
