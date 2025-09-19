# PortfoView-Py – FÁZE 0 (Nástroje + Repo)

## Cíl fáze
Mít připravené a ověřené vývojové prostředí (Python, Git, Docker), založené public GitHub repo `portfoview-py` a minimální základ repozitáře (`README.md`, `LICENSE`, `.gitignore`).
Tím uzavíráme Fázi 0 a můžeme stavět skeleton aplikace (Fáze 1).

---

## 1) Instalace a ověření nástrojů

### 1.1 Python
- **Proč:** běh aplikace, knihovny, testy.
- **Ověření:**
  ```bash
  python --version
  # očekávám: Python 3.13.x
````

### 1.2 Git

* **Proč:** verzování + GitHub workflow.
* **Ověření:**

  ```bash
  git --version
  # očekávám: git version 2.x
  ```

### 1.3 Editor (VS Code)

* **Proč:** pohodlné psaní kódu a práce s Gitem.
* **Ověření:** otevření projektu ve VS Code.

### 1.4 Docker Desktop

* **Proč:** jednotné běhové prostředí, snadné “nasazení” lokálně.
* **Ověření:**

  ```bash
  docker --version
  docker run --rm hello-world
  # očekávám text "Hello from Docker!"
  ```

### (Volitelné) 1.5 Lokální virtualenv

* **Proč:** izolace Python balíčků mimo systém.
* **Příkaz:**

  ```bash
  python -m venv .venv
  source .venv/Scripts/activate   # Windows (Git Bash/PowerShell)
  python -m pip install --upgrade pip
  ```

---

## 2) Založení repozitáře a minimální obsah

### 2.1 Inicializace lokálně (varianta A)

```bash
mkdir portfoview-py && cd portfoview-py
git init
```

### 2.2 Klon existujícího GitHub repa (varianta B)

```bash
git clone git@github.com:<uzivatel>/portfoview-py.git
cd portfoview-py
```

### 2.3 Minimální soubory (root)

* `README.md` – popis projektu
* `LICENSE` – MIT licence
* `.gitignore` – ignorované soubory (`venv`, `__pycache__`, atd.)

Ukázkové příkazy (pokud zakládám z nuly):

```bash
echo "# portfoview-py" > README.md
curl -s https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore > .gitignore
# MIT licenci vložím ručně nebo použiji šablonu GitHubu
git add README.md .gitignore LICENSE
git commit -m "chore: initial repo (README, LICENSE, .gitignore)"
```

---

## 3) Napojení na GitHub & kontrola práv

### 3.1 Napojení remotu

```bash
git remote add origin git@github.com:<uzivatel>/portfoview-py.git
```

### 3.2 První push

```bash
git branch -M main
git push -u origin main
```

### 3.3 Kontrola remotu a větví

```bash
git remote -v
git ls-remote --heads origin
git remote show origin
git push --dry-run
```

**Očekávání:**

* `remote -v` ukáže URL `portfoview-py.git`
* `ls-remote --heads origin` vypíše `refs/heads/main`
* `remote show origin` bez chyb, ukáže tracked větve
* `push --dry-run` projde bez chyby (mám push práva)

---

## 4) RoadMap (zdroj pravdy)

Dokument *RoadMap* existuje (Word/PDF).
Místo: v repu (např. `docs/RoadMap.docx`) nebo mimo repo.
**Proč:** Každý krok měříme proti DoD v RoadMap.

---

## 5) Stav na konci FÁZE 0 (Definition of Done)

* ✅ Python, Git, Docker nainstalovány a ověřeny (`--version`, `hello-world`)
* ✅ Veřejné GitHub repo `portfoview-py` existuje a je napojené (origin)
* ✅ Základní soubory v repu: `README.md`, `LICENSE (MIT)`, `.gitignore`
* ✅ RoadMap existuje a používáme ji při plánování
* ✅ (Nice-to-have) `.venv` vytvořen pro lokální utilitky

---

## 6) Evidence — typické výstupy

```bash
$ python --version
Python 3.13.5

$ git --version
git version 2.50.1.windows.1

$ docker --version
Docker version 28.3.2, build 578cc6f

$ docker run --rm hello-world
Hello from Docker!
```

```bash
$ git remote -v
origin  git@github.com:<uzivatel>/portfoview-py.git (fetch)
origin  git@github.com:<uzivatel>/portfoview-py.git (push)

$ git ls-remote --heads origin
<hash>  refs/heads/main
<hash>  refs/heads/feature/scaffold

$ git remote show origin
* remote origin
  Fetch URL: git@github.com:<uzivatel>/portfoview-py.git
  Push  URL: git@github.com:<uzivatel>/portfoview-py.git
  HEAD branch: main
  Remote branches: main, feature/scaffold (tracked)
  Local refs configured for 'git push':
    main -> main
    feature/scaffold -> feature/scaffold

$ ls -1
README.md
LICENSE
.gitignore
```

---

## 7) Co následuje

➡️ Fáze 1 – skeleton + dockerizace

* větev `feature/scaffold` pro skeleton FastAPI (`/healthz`)
* větev `feature/dockerize` pro Dockerfile, docker-compose.yml, .dockerignore, requirements.txt
* cíl: `docker compose up --build` → 200 OK na `/healthz`

```

---
