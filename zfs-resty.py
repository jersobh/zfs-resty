#!/usr/bin/env python3

import logging
import logging.handlers
import argparse
import sys
import time  # this is only being used as part of the example
import aiohttp
import asyncio
from router import routes
import jwt
import render
import ipaddress

JWT_SECRET = "7wXJ4kxCRWJpMQNqRVTVR3Qbc"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 180
# # Deafults
# LOG_FILENAME = "/tmp/zfs-resty.log"
# LOG_LEVEL = logging.INFO
PORT = '8089'
SAFE = 'false'
# parser = argparse.ArgumentParser(description="ZFS-Resty")
# parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
# parser.add_argument("-p", "--port", help="port (default '" + PORT + "')")
# parser.add_argument("-s", "--safe", help="port (default '" + SAFE + "')")
#
# args = parser.parse_args()
# if args.log:
#         LOG_FILENAME = args.log
#
# logger = logging.getLogger(__name__)
# logger.setLevel(LOG_LEVEL)
# handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
#
# class ZFSLogger(object):
#         def __init__(self, logger, level):
#                 self.logger = logger
#                 self.level = level
#
#         def write(self, message):
#                 if message.rstrip() != "":
#                         self.logger.log(self.level, message.rstrip())
#
# sys.stdout = ZFSLogger(logger, logging.INFO)
# sys.stderr = ZFSLogger(logger, logging.ERROR)

parser = argparse.ArgumentParser(description="zfs-resty")
parser.add_argument("-p", "--port", help="port (default '" + PORT + "')")
parser.add_argument("-s", "--safe", help="port (default '" + SAFE + "')")
args = parser.parse_args()


async def check_safe_ip(request):
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, port = peername
        return ipaddress.ip_address(host).is_private


async def auth_middleware(app, handler):
    async def middleware(request):
        if args.safe == 'true':
            check = await check_safe_ip(request)
            if not check:
                return await render.json({'error': 'Not safe origin'}, 403)
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            try:
                jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception as e:
                response = {'error': str(e)}
                return await render.json(response, 401)

        return await handler(request)
    return middleware


loop = asyncio.get_event_loop()
app = aiohttp.web.Application(loop=loop,  middlewares=[auth_middleware])
routes(app)

aiohttp.web.run_app(app, host='0.0.0.0', port=args.port)

