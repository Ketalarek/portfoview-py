from fastapi import FastAPI

app = FastAPI(title="PortfoView-Py")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
