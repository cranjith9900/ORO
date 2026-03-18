from fastapi import FastAPI
from app.database import Base, engine

# IMPORT YOUR ROUTE
from app.modules.master_data.routes import router as department_router
from app.modules.users.routes import router as user_router

app = FastAPI(
    title="FastAPI + PostgreSQL + pgvector",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(department_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "FastAPI server running 🚀"}