from aiohttp import web
import jwt
from config import JWT_SECRET, JWT_ALGORITHM, logger

@web.middleware
async def auth_middleware(request, handler):
    jwt_token = request.headers.get('Authorization')
    if not jwt_token:
        logger.warning("Missing Authorization header")
        return web.json_response({'error': 'Missing Authorization header'}, status=401)

    try:
        jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.warning("JWT expired")
        return web.json_response({'error': 'Token expired'}, status=401)
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT: {e}")
        return web.json_response({'error': 'Invalid token'}, status=401)

    return await handler(request)
