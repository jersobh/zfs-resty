import uuid
from datetime import datetime, timedelta
from controllers import zfs_controller
import jwt
import pam

import render

from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS



async def index(request):
    return await render.json({'error': 'nothing to see here...'}, 200)



async def check_token(request):
    try:
        jwt_token = request.headers.get('Authorization', None)
        payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload['session_id']
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False

async def create_pool(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            res = await zfs_controller.create_pool(data['name'], data['raid'], data['devices'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def delete_pool(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            res = await zfs_controller.delete_pool(data['name'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def check_status(request):
    check = await check_token(request)
    if check:
        try:
            res = await zfs_controller.get_status()
            return await render.json({'msg': res}, 200)
        except Exception as e:
            print(str(e))


async def get_storage_info(request):
    check = await check_token(request)
    if check:
        try:
            res = await zfs_controller.get_disk_info()
            return await render.json(res, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 500)


async def get_io_status(request):
    check = await check_token(request)
    if check:
        try:
            res = await zfs_controller.get_IO_stats()
            return await render.json({'msg': res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 500)


async def add_disk(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            res = await zfs_controller.add_new_disk(data['pool'], data['device'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 500)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def add_spare_disk(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            res = await zfs_controller.add_spare_disk(data['pool'], data['device'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def replace_disk(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            res = await zfs_controller.replace_disk(data['pool'], data['old_device'], data['new_device'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def set_mountpoint(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            res = await zfs_controller.set_mountpoint(data['mountpoint'], data['pool'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            print(str(e))
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)

