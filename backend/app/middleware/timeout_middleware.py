import asyncio

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int = 10):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request, call_next):
        try:
            # Run the request within the timeout limit
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            # Handle timeout by returning a custom response
            return JSONResponse(
                {"error": "Request timed out. Please try again later."}, status_code=504
            )
