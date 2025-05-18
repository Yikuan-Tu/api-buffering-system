from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.utils.database import init_db
from app.utils.config import DB_PATH
from app.routes.submit import router as submit_router
from app.utils.logger import setup_logging

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info(f"✅ Database initialized at {DB_PATH}")
    yield


app = FastAPI(
    title="API Buffering System",
    description="DevOps Assessment Task",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(submit_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API Buffering System"}


@app.get("/health/")
def health_check():
    return {"message": "API Buffering System is running"}


@app.get("/count/")
def get_count():
    from app.utils.database import execute_query

    count = execute_query("SELECT COUNT(*) FROM people")
    return {"count": count}
