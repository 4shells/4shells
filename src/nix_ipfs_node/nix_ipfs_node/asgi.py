# Third party libraries
from starlette.applications import Starlette
from starlette.routing import Route

# Local libraries
from nix_ipfs_node import (
    handlers,
)

# Constants
APP = Starlette(
    routes=[
        Route('/', handlers.route),
    ],
)
