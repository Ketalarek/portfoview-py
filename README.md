# PortfoView-Py
FastAPI aplikace pro sledování portfolia (XTB CSV, FIFO P/L, dashboard).

---

## Fáze 0 — Příprava prostředí

### Požadavky
Aby bylo možné projekt spustit, je potřeba mít nainstalováno:
- Git
- Python 3.12+
- Docker Desktop (s WSL2 na Windows)
- VS Code (doporučeno)

### Kroky
1. Vytvoření GitHub účtu a repozitáře `portfoview-py`.
2. Naklonování repozitáře do lokálního počítače:
   ```bash
   git clone https://github.com/<tvoje_jmeno>/portfoview-py.git
   cd portfoview-py
````

3. Inicializace Gitu a první commit skeletonu.
4. Ověření nástrojů:

   ```bash
   git --version
   python --version
   docker --version
   ```

**Výsledek Fáze 0:**
Repozitář připravený na vývoj, nástroje nainstalované, prostředí ověřené.

---

## Fáze 1 — Skeleton aplikace + Docker

### Kroky

1. **Struktura projektu**

   * `app/main.py` → FastAPI app s endpointem `/healthz`
   * `requirements.txt` → závislosti (`fastapi`, `uvicorn[standard]`)
   * `Dockerfile` → popis obrazu aplikace
   * `.dockerignore` → ignorování nepotřebných souborů v obrazu
   * `docker-compose.yml` → spuštění služby `web` na portu 8000

2. **Spuštění aplikace**

   ```bash
   docker compose up --build
   ```

3. **Ověření běhu**

   * Healthcheck: [http://localhost:8000/healthz](http://localhost:8000/healthz)
     → odpověď: `{"status":"ok"}`
   * Swagger dokumentace: [http://localhost:8000/docs](http://localhost:8000/docs)

### Očekávaný výsledek

* `docker compose up --build` proběhne bez chyby
* `GET /healthz` vrátí **200 OK** a JSON `{"status":"ok"}`
* Swagger UI na `/docs` ukáže endpoint `/healthz`

---

## Roadmapa projektu

* **Fáze 0**: příprava nástrojů, repo (✅ hotovo)
* **Fáze 1**: skeleton aplikace + Docker (✅ hotovo)
* **Fáze 2**: kvalita & CI (pytest, pre-commit, GitHub Actions)
* **Fáze 3**: datový model a SQLite
* **Fáze 4**: import XTB CSV
* **Fáze 5**: výpočty pozic a P/L
* **Fáze 6**: webové UI (Jinja/HTMX)
* **Fáze 7–8**: ceny tickerů, bezpečnost, konfigurace
* **Fáze 9**: Postgres (volitelné)
* **Fáze 10**: prezentace pro pohovor

```

---

👉 Takto to bude vypadat čistě a smysluplně pro někoho, kdo přijde do repa a potřebuje vědět: *co bylo hotovo, jak to spustit, jaký je očekávaný výsledek*.

Chceš, abych ti teď udělal **krátkou rekapitulaci v bodech, co jsme udělali v Fázi 0 a 1** (jako tahák do hlavy), než začneme s Fází 2?
```
