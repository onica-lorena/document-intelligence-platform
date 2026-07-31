from fastapi import FastAPI
import logging

from app.core.config import settings
from app.core.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)
logger.info("Application is starting...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)