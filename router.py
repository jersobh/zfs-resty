
from controllers import mainController
import aiohttp_cors

def routes(app):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_methods=("*"),
            allow_credentials=True,
            expose_headers=("*",),
            allow_headers=("*"),
            max_age=3600,
        )
    })
    cors.add(app.router.add_get('/', mainController.index))
    cors.add(app.router.add_post('/auth', mainController.auth))
    cors.add(app.router.add_post('/create-pool', mainController.create_pool))
    cors.add(app.router.add_post('/delete-pool', mainController.delete_pool))
    cors.add(app.router.add_get('/status', mainController.check_status))
    cors.add(app.router.add_get('/io-status', mainController.get_io_status))
    cors.add(app.router.add_post('/add-disk', mainController.add_disk))
    cors.add(app.router.add_post('/add-spare-disk', mainController.add_spare_disk))
    cors.add(app.router.add_post('/replace-disk', mainController.replace_disk))
    cors.add(app.router.add_post('/mountpoint', mainController.set_mountpoint))
