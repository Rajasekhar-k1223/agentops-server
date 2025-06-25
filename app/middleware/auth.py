from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
import os

class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.token = os.getenv("AGENT_SECRET_TOKEN", "mysecrettoken")
        self.security = HTTPBearer()

    async def dispatch(self, request: Request, call_next):
        auth: HTTPAuthorizationCredentials = await self.security.__call__(request)
        if not auth or auth.credentials != self.token:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
        return await call_next(request)
