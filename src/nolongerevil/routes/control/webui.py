"""Web UI routes - serves the device management HTML interface."""

from pathlib import Path

from aiohttp import web

from nolongerevil.config import settings
from nolongerevil.lib.logger import get_logger

logger = get_logger(__name__)

# Path to HTML template (CSS and JS are inlined to avoid ingress path issues)
TEMPLATE_DIR = Path(__file__).parent / "templates"
INDEX_TEMPLATE = TEMPLATE_DIR / "index.html"
HISTORY_TEMPLATE = TEMPLATE_DIR / "history.html"
STATIC_DIR = Path(__file__).parent / "static"
NLE_ICON = TEMPLATE_DIR / "nle-icon.png"
NLE_FAVICON = TEMPLATE_DIR / "nle-favicon.png"


def _page(request: web.Request, template: Path) -> web.Response:
    """Serve a page, injecting the Home Assistant ingress path and login flag."""
    ingress_path = request.headers.get("X-Ingress-Path", "")
    html = template.read_text()

    # Inject the ingress path via data attribute on body tag
    login = "1" if settings.control_auth and not ingress_path else ""
    html = html.replace("<body>", f'<body data-ingress-path="{ingress_path}" data-login="{login}">')

    return web.Response(text=html, content_type="text/html")


async def handle_webui(request: web.Request) -> web.Response:
    """Handle GET / - serve the web UI."""
    return _page(request, INDEX_TEMPLATE)


async def handle_history(request: web.Request) -> web.Response:
    """Handle GET /history - serve the history charts."""
    return _page(request, HISTORY_TEMPLATE)


async def handle_icon(_request: web.Request) -> web.Response:
    """Serve the NLE icon."""
    return web.Response(body=NLE_ICON.read_bytes(), content_type="image/png")


async def handle_favicon(_request: web.Request) -> web.Response:
    """Serve the NLE favicon."""
    return web.Response(body=NLE_FAVICON.read_bytes(), content_type="image/png")


def create_webui_routes(app: web.Application) -> None:
    """Register web UI routes."""
    app.router.add_get("/", handle_webui)
    app.router.add_get("/history", handle_history)
    app.router.add_static("/static/", STATIC_DIR)
    app.router.add_get("/nle-icon.png", handle_icon)
    app.router.add_get("/nle-favicon.png", handle_favicon)
    logger.info("Web UI routes registered")
