import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router as todos_router
from .automation.scheduler import run_scheduler_forever
from .db import Base, engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Todo Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos_router)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    asyncio.create_task(run_scheduler_forever())
    logger.info("startup complete")
