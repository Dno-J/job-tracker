from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from fastapi.requests import Request

from app.auth.jwt import verify_access_token

# -----------------------------------------------
# 🌐 Public routes that don't require authentication
# -----------------------------------------------
# These paths are accessible without login
PUBLIC_PATHS = [
    "/", "/login", "/register", "/signup", "/ping",
    "/api/register", "/api/login"
]

# -------------------------------------------------------
# 🛡️ AuthMiddleware - Restrict access to authenticated users
# -------------------------------------------------------
class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts requests and enforces authentication
    for protected routes. Redirects unauthenticated users to /login.
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # ✅ Allow access to public paths or static assets
        if path in PUBLIC_PATHS or path.startswith("/static"):
            return await call_next(request)

        # 🔐 Extract JWT token from cookies
        token = request.cookies.get("access_token")
        if not token:
            # No token → redirect to login
            return RedirectResponse(url="/login")

        # 🔍 Verify token validity
        payload = verify_access_token(token)
        if not payload:
            # Invalid token → redirect to login
            return RedirectResponse(url="/login")

        # ✅ Token is valid → proceed to requested route
        return await call_next(request)
