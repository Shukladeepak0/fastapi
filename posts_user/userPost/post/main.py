from fastapi import FastAPI
from .Models import models
from .Database.database import engine
from .routers import route

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(route.mainrouter)

models.Base.metadata.create_all(engine)

