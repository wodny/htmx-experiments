#!/usr/bin/env python3

import asyncio
import weakref
import pathlib
import itertools
import contextlib
import logging

from aiohttp import web

logger = logging.getLogger()

routes = web.RouteTableDef()

@routes.get("/")
async def welcome(request):
    return web.FileResponse(pathlib.Path(__file__).parent / "index.html")

@routes.get("/ws")
async def websocket_user(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app["websockets"].add(ws)
    async for msg in ws:
        pass
    return ws

async def handle_notifications(app):
    for serial in itertools.count():
        logger.info(f"notification {serial}")
        for ws in set(app["websockets"]):
            logger.info(f"sending {serial} to {ws}")
            try:
                await ws.send_str(f'{{"serial": {serial}}}')
            except (RuntimeError, OSError):
                app["websockets"].discard(ws)
        await asyncio.sleep(1)

async def start_notifications(app):
    asyncio.create_task(handle_notifications(app))

def main():
    logging.basicConfig(level="INFO")
    app = web.Application()
    app["websockets"] = weakref.WeakSet()
    routes.static("/js", pathlib.Path(__file__).parent / "js", show_index=True)
    app.add_routes(routes)
    app.on_startup.append(start_notifications)
    web.run_app(app)

if __name__ == "__main__":
    main()
