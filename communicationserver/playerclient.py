import asyncio
import json
import websockets

from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

import playerPH as ph


class PlayerClient:
    def __init__(self, UUID, ws):
        self.UUID = UUID
        self.ws = ws
        self.ip = ws.remote_address[0]
        self.port = ws.remote_address[1]
        self.inbound = asyncio.Queue()
        self.outbound = asyncio.Queue()
    
    def tick(self, handler):
        while not self.inbound.empty():
            msg = self.inbound.get_nowait()
            t = msg["type"]
            d = msg["data"]
            print(f"[{self.UUID}] PLAYER CLIENT TICK {t} : {d}")
            match t:
                case "AUTH_REQ":
                    ph.AUTH_REQ(handler, d, self)


    def send(self, type, data):
        p = {
            'type': type,
            'data': data
        }
        self.outbound.put_nowait(json.dumps(p))


    async def handleSend(self):
        try:
            while True:
                msg = await self.outbound.get()
                await self.ws.send(msg)
        except ConnectionClosedOK:
            print(f"[{self.UUID}]'s session was closed gracefully")
            raise
        except ConnectionClosedError:
            print(f"[ERROR] Sending {self.UUID} a msg")
            raise
        except Exception as e:
            print(f"[UNEXPECTED ERROR] Sending {self.UUID} a msg, {e}")
            raise
            


    async def handleReceive(self): 
        try:
            async for msg in self.ws:
                decoded = json.loads(msg)
                print(f"[SESS-ID:{self.UUID}  {self.ip}:{self.port}] MSG: {msg}")
                self.inbound.put_nowait(decoded)
        except ConnectionClosedOK:
            raise
        except ConnectionClosedError:
            print(f"[ERROR] Receiving {self.UUID} a msg")
            raise
        except Exception as e:
            print(f"[UNEXPECTED ERROR] Receiving {self.UUID} a msg, {e}")
            raise