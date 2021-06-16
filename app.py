from aiohttp import web
from server_logging import logging

from routes import routes

app = web.Application()
app.add_routes(routes)
logging.warning("Starting server...")
web.run_app(app)
logging.warning("Server stopped")
