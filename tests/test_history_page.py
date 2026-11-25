"""The history page and its bundled chart library are served."""

from aiohttp import web

from nolongerevil.routes.control.webui import create_webui_routes


async def test_history_page_and_chart_library(aiohttp_client):
    app = web.Application()
    create_webui_routes(app)
    client = await aiohttp_client(app)
    page = await client.get("/history", headers={"X-Ingress-Path": "/api/hassio_ingress/x"})
    html = await page.text()
    assert page.status == 200 and 'data-ingress-path="/api/hassio_ingress/x"' in html
    assert 'src="static/uplot/uPlot.iife.min.js"' in html  # Relative, so it works under ingress
    script = await client.get("/static/uplot/uPlot.iife.min.js")
    assert script.status == 200 and len(await script.read()) > 10000
