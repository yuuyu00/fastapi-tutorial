from fastapi import FastAPI
import uvicorn

from app.routers import items
from app.database import engine
from app.models import database as db_models

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Tutorial",
    description="TypeScript開発者向けFastAPIチュートリアル",
    version="0.1.0"
)

# register routers
app.include_router(items.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9000, reload=True)