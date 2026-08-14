from contextlib import asynccontextmanager
import logging
from app.vectorstore.repository import VectorRepository

from fastapi import FastAPI

from app.database.mongodb import (
    connect_to_mongo,
    close_mongo_connection,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Connecting to MongoDB...")

    await connect_to_mongo()

    logger.info("MongoDB connected.")

    vector_repository = VectorRepository()

    await vector_repository.create_collection()

    logger.info("Qdrant collection initialized.")

    yield

    logger.info("Closing MongoDB connection...")

    await close_mongo_connection()

    logger.info("MongoDB connection closed.")