from fastapi import FastAPI
import logging

from app.api.health import router as health_router
from app.core.exceptions import register_exception_handlers
from app.core.config import settings
from app.core.logger import setup_logging
from app.core.middleware import log_requests

setup_logging()

logger = logging.getLogger(__name__)
logger.info("Application is starting...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.middleware("http")(log_requests)
register_exception_handlers(app)

app.include_router(health_router)