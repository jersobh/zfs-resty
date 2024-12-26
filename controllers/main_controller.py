from controllers import zfs_controller
from controllers.auth import check_token

import render

from config import logger



async def index(request):
    return await render.json({'error': 'nothing to see here...'}, 200)


async def create_pool(request):
    
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            logger.info(f"Creating pool {data['name']}")
            res = await zfs_controller.create_pool(data['name'], data['raid'], data['devices'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            logger.error(f"Error while creating pool: {str(e)}")
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def delete_pool(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            logger.info(f"Deleting pool {data['name']}")
            res = await zfs_controller.delete_pool(data['name'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            logger.error(f"Error while deleting pool: {str(e)}")
            return await render.raw({'error': str(e)}, 200)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def check_status(request):
    check = await check_token(request)
    if check:
        try:
            logger.info(f"Getting status")
            res = await zfs_controller.get_status()
            return await render.json({'msg': res}, 200)
        except Exception as e:
            logger.error(f"Error while fetching status: {str(e)}")
            return await render.json({'error': str(e)}, 500)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)



async def get_storage_info(request):
    check = await check_token(request)
    if check:
        try:
            logger.info(f"Getting storage info")
            res = await zfs_controller.get_disk_info()
            return await render.json(res, 200)
        except Exception as e:
            logger.error(f"Error while getting storage info: {str(e)}")
            return await render.raw({'error': str(e)}, 500)


async def get_io_status(request):
    check = await check_token(request)
    if check:
        try:
            logger.info(f"Getting io status")
            res = await zfs_controller.get_IO_stats()
            return await render.json({'msg': res}, 200)
        except Exception as e:
            logger.error(f"Error while getting io status: {str(e)}")
            return await render.raw({'error': str(e)}, 500)


async def add_disk(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            logger.info(f"Adding disk to {data['pool']}")
            res = await zfs_controller.add_new_disk(data['pool'], data['device'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            logger.error(f"Error while adding disk: {str(e)}")
            return await render.raw({'error': str(e)}, 500)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def add_spare_disk(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            logger.info(f"Adding spare disk to {data['pool']}")
            res = await zfs_controller.add_spare_disk(data['pool'], data['device'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            logger.error(f"Error while adding spare disk: {str(e)}")
            return await render.raw({'error': str(e)}, 500)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def replace_disk(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            logger.info(f"Replacing disk {data['old_device']} with {data['new_device']}")
            res = await zfs_controller.replace_disk(data['pool'], data['old_device'], data['new_device'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            logger.error(f"Error while replacing disk: {str(e)}")
            return await render.raw({'error': str(e)}, 500)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)


async def set_mountpoint(request):
    check = await check_token(request)
    if check:
        try:
            data = await request.json()
            logger.info(f"Setting mountpoint {data['mountpoint']} to pool {data['pool']}")
            res = await zfs_controller.set_mountpoint(data['mountpoint'], data['pool'])
            return await render.json({"success": res}, 200)
        except Exception as e:
            logger.error(f"Error while setting mountpoint: {str(e)}")
            return await render.raw({'error': str(e)}, 500)
    else:
        return await render.json({'error': 'Invalid or expired token'}, 403)

