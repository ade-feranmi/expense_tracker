from fastapi import FastAPI
from routers import router
from database import engine
from models import Base

app = FastAPI(
    title="Personal_Expense_Tracker",
    version="1.0.0",
    description="A fast and reliable personal expense tracker"
)
Base.metadata.create_all(engine)
app.include_router(router)