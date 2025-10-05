from fastapi import FastAPI
from database import Base, engine
from api.routes import router as api_router


app = FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(api_router)


@app.get("/")
async def root():
    return {"data": "App Is Running"}
