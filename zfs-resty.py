#!/usr/bin/env python3

import logging
import logging.handlers
import argparse
import sys
import aiohttp
import asyncio
from aiohttp import web
import jwt
import render
import ipaddress
from dotenv import load_dotenv
import os
from router import routes

# Load environment variables
load_dotenv()

# Constants from .env or arguments
DEFAULT_PORT = os.getenv("DEFAULT_PORT", "8089")
DEFAULT_SAFE = os.getenv("DEFAULT_SAFE", "false")
LOG_FILENAME = os.getenv("LOG_FILENAME", "/tmp/zfs-resty.log")
LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
JWT_SECRET = os.getenv("JWT_SECRET", "7wXJ4kxCRWJpMQNqRVTVR3Qbc")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_SECONDS = int(os.getenv("JWT_EXP_DELTA_SECONDS", "180"))

# Configure logger
logger = logging.getLogger("zfs-resty")
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ZFSLogger(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.rstrip():
            self.logger.log(self.level, message.rstrip())

# Redirect stdout and stderr to logger
sys.stdout = ZFSLogger(logger, logging.INFO)
sys.stderr = ZFSLogger(logger, logging.ERROR)

# Argument parser
parser = argparse.ArgumentParser(description="ZFS-Resty")
parser.add_argument("-p", "--port", default=DEFAULT_PORT, help="Port to run the server on (default: %(default)s)")
parser.add_argument("-s", "--safe", default=DEFAULT_SAFE, help="Enable safe mode (default: %(default)s)")
args = parser.parse_args()

async def check_safe_ip(request):
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, _ = peername
        return ipaddress.ip_address(host).is_private
    return False

@web.middleware
async def auth_middleware(request, handler):
    if args.safe.lower() == 'true':
        safe_check = await check_safe_ip(request)
        if not safe_check:
            logger.warning("Access denied: unsafe IP")
            return web.json_response({'error': 'Not safe origin'}, status=403)

    jwt_token = request.headers.get('Authorization', None)
    if jwt_token:
        try:
            jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            logger.warning("JWT expired")
            return web.json_response({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT: {e}")
            return web.json_response({'error': 'Invalid token'}, status=401)

    return await handler(request)

async def init_app():
    app = web.Application(middlewares=[auth_middleware])
    routes(app)
    return app

if __name__ == "__main__":
    try:
        port = int(args.port)
        logger.info(f"Starting server on port {port}")
        web.run_app(init_app(), host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
