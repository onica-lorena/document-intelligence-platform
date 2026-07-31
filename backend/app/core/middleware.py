import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    logger.info(
        "%s %s -> %s (%.3f s)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response