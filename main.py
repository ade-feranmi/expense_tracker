from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import router as api_router
from views import router as ui_router

app = FastAPI(
    title="Pesa_Flow",
    version="1.0.0",
    description="PesaFlow turns your M-Pesa statement into a clear, categorized picture of your money and helps you do something about it.",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
app.include_router(ui_router)