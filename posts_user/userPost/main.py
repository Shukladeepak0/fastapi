from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def index():
    return {'data': "Blog List"}
    

@app.get("/blog/{id}")
def show(id: int):
    return {'data': id}
    