import asyncio
import string
import random

from websockets.asyncio.server import serve
import websockets.exceptions as wsExceptions

from playerclient import PlayerClient

class PlayerClientManager:
    def __init__(self):
        self.handler = None

        self.unauthedclients = {}
        self.playerclients = {}


    def tick(self, handler):
        for c in self.unauthedclients.values():
            c.tick(handler)
        for c in self.playerclients.values():
            c.tick(handler)

    async def cleanup(self, player, code = 1000, reason = "Unknown"):
        sessID = player.UUID

        async with self._clean_lock:
            if sessID in self._cleaned:
                return
            self._cleaned.add(sessID)

        self.unauthedclients.pop(sessID, None)
        self.playerclients.pop(sessID, None)
    async def forceDisconnect(self, player, code=1000, reason="Forced Disconnect"):
        try:
            await player.ws.close(code=code, reason=reason)
        except Exception as e:
            print(f"[ERROR] Trying to Disconnect {player.UUID}, {repr(e)}")
        finally:
            await self.cleanup(player, code=code, reason=reason)


    async def handleConnection(self, ws):
        key = self._generateNewSessionID()
        client = PlayerClient(key, ws)
        self.unauthedclients[key] = client

        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(client.handleReceive())
                tg.create_task(client.handleSend())
        except (wsExceptions.ConnectionClosedOK, wsExceptions.ConnectionClosedError) as e:
            print(f"Client {client.UUID} disconnected!: {e.code} {e.reason}")
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


    def _generateNewSessionID(self):
        characterPool = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characterPool) for i in range(4))
            if key not in self.playerclients.keys(): return key
