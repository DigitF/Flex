from aiohttp import ClientSession, TCPConnector
import asyncio


class AsyncHttp:

    _cs: ClientSession

    def __init__(self):
        self._cs = ClientSession(connector=TCPConnector(verify_ssl=False))

    async def get(self, url):
        async with self._cs.get(url) as resp:
            return await resp.text()

    async def close(self):
        await self._cs.close()