from fastapi import FastAPI
from routers import router

app = FastAPI(
    title="Pesa_Flow",
    version="1.0.0",
    description="PesaFlow turns your M-Pesa statement into a clear, categorized picture of your money and helps you do something about it.",
)
app.include_router(router)