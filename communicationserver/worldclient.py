import asyncio
import json
import websockets
import traceback
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

import worldPH as ph


class WorldClient:
    def __init__(self, UUID, ws):
        self.UUID = UUID
        self.ws = ws
        self.ip = ws.remote_address[0]
        self.port = ws.remote_address[1]
        print(f"NEW WORLD CLIENT [{self.ip}:{self.port}]")
        self.inbound = asyncio.Queue()
        self.outbound = asyncio.Queue()
        self.playerCount = 0
        self.players = {}
        self.type = None
        self.ID = None
        self.nameID = self.updateName()
    
    def tick(self, handler):
        while not self.inbound.empty():
            msg = self.inbound.get_nowait()
            t = msg["type"]
            d = msg["data"]
            print(f"[{self.UUID}] WORLD CLIENT TICK {t} : {d}")
            match t:
                case "register":
                    ph.register(handler, d, self)
                case "switch":
                    ph.switch(handler, d, self)
                case "player_count_update":
                    ph.player_count_update(handler, d, self)


    def send(self, type, data):
        p = {
            'type': type,
            'data': data
        }
        self.outbound.put_nowait(json.dumps(p))


    async def handleSend(self):
        #print(f"Handling Send!")
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
        #print(f"Handling Receive!")
        try:
            async for msg in self.ws:
                decoded = json.loads(msg)
                print(f"[SESS-ID:{self.UUID}  {self.ip}:{self.port}] MSG: {msg}")
                self.inbound.put_nowait(decoded)
        except ConnectionClosedOK:
            raise
        except ConnectionClosedError as e:
            print(f"[ERROR] Receiving {self.UUID} ConnectionClosedError {e} ")
            traceback.print_exc()
            raise
        except Exception as e:
            print(f"[UNEXPECTED ERROR] Receiving {self.UUID} a msg, {e}")
            raise
    
    def getIPString(self):
        return f"{self.ip}:{self.port}"

    def updateName(self):
        #print(f"REDOING NAME")
        if self.type is None or self.ID is None:
            self.nameID = None
        else:
            self.nameID = self.type + '-' + str(self.ID)