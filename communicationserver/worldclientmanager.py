import asyncio
from websockets.asyncio.server import serve


class WorldClientManager:

    def tick(self, handler):
        pass

    async def handleConnection(self, ws):
        pass

    async def start(self, ListenHost, Port):
        self.ListenHost = ListenHost
        self.Port = Port
        self.server = await serve(self.handleConnection, self.ListenHost, self.Port)
        await self.server.serve_forever()