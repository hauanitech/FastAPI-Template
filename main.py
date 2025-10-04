from fastapi import FastAPI
from database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"data": "App Is Running"}
