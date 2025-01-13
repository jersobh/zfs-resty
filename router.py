import aiohttp_cors
from controllers import auth, main_controller

def routes(app):
    # Set up CORS
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_methods=("*"),
                allow_credentials=True,
                expose_headers=("*",),
                allow_headers=("*"),
                max_age=3600,
            )
        }
    )

    # Define routes and their handlers
    route_definitions = [
        {"method": "GET", "path": "/", "handler": main_controller.index},
        {"method": "POST", "path": "/auth", "handler": auth.login},
        {"method": "POST", "path": "/create-pool", "handler": main_controller.create_pool},
        {"method": "POST", "path": "/delete-pool", "handler": main_controller.delete_pool},
        {"method": "GET", "path": "/devices", "handler": main_controller.get_storage_info},
        {"method": "GET", "path": "/status", "handler": main_controller.check_status},
        {"method": "GET", "path": "/io-status", "handler": main_controller.get_io_status},
        {"method": "POST", "path": "/add-disk", "handler": main_controller.add_disk},
        {"method": "POST", "path": "/add-spare-disk", "handler": main_controller.add_spare_disk},
        {"method": "POST", "path": "/replace-disk", "handler": main_controller.replace_disk},
        {"method": "POST", "path": "/mountpoint", "handler": main_controller.set_mountpoint},
    ]

    # Add routes and attach CORS
    for route in route_definitions:
        cors.add(app.router.add_route(route["method"], route["path"], route["handler"]))
