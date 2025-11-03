import asyncio
import string
import random

from websockets.asyncio.server import serve
import websockets.exceptions as wsExceptions

from worldclient import WorldClient
import worldPH as ph

# import logging

# logging.basicConfig(
#     format="%(asctime)s %(message)s",
#     level=logging.DEBUG,
# )

# logger = logging.getLogger("websockets")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

class WorldClientManager:
    def __init__(self):
        self.handler = None

        #   desiredWorlds key is world name, like beach and value would be 2 (we want to try and have 2 beach worlds)
        self.desiredWorlds = {}



        self.worldclients = {}


    def tick(self, handler):
        for c in self.worldclients.values():
            c.tick(handler)

    async def handleConnection(self, ws):
        print(f"Establishing New Connection!")
        key = self._generateNewSessionID()
        print(f"Generated Key {key}")
        client = WorldClient(key, ws)
        print(f"---New World Client Object!")
        self.worldclients[key] = client
        print(f"Setting self.worldclients[{key} == new client!]")

        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(client.handleReceive())
                tg.create_task(client.handleSend())
        # except (wsExceptions.ConnectionClosedOK, wsExceptions.ConnectionClosedError) as e:
        #     print(f"Client {client.UUID} disconnected!: {e.code} {e.reason}")
        except Exception as e:
            print(f"[Error] Handling Receiving and Sending for {key} {e}")
        finally:
            await client.ws.wait_closed()
            await self.cleanup(client)

    async def start(self, ListenHost, Port, handler):
        self.ListenHost = ListenHost
        self.Port = Port
        self.handler = handler
        self.server = await serve(self.handleConnection, self.ListenHost, self.Port)
        await self.server.serve_forever()

    async def cleanup(self, client, code = 1000, reason = "Unknown"):
        UUID = client.UUID
        self.worldclients.pop(client.UUID, None)

    def _generateNewSessionID(self):
        characterPool = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characterPool) for i in range(4))
            if key not in self.worldclients.keys(): return key
