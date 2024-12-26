from aiohttp import web
from config import logger
from middlewares import auth_middleware
from router import routes

async def init_app():
    app = web.Application(middlewares=[auth_middleware])
    routes(app)
    return app


if __name__ == "__main__":
    try:
        app = init_app()
        web.run_app(app, host="0.0.0.0", port=8089)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
