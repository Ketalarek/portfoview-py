from fastapi import FastAPI

from app.routers.transactions import router as transactions_router

app = FastAPI(title="PortfoView-Py")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


app.include_router(transactions_router)
