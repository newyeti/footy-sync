import time

from fastapi import Request
import logging as logger

async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"method={request.method}, path={request.url.path}, response_time={process_time}")
    return response 
