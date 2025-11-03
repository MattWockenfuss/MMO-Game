import websockets
import asyncio
import json

import WSCOMMSPacketHandler as ph

class CommsServerClient:
    def __init__(self):
        self.IP = None
        self.Port = None
        self.outbound = asyncio.Queue()
        self.inbound = asyncio.Queue()
        self._shutdown_event = asyncio.Event()

        # ex... beach-1 or crypts-5
        self.worldType = None
        self.worldID = None
        self.worldName = None
    
    def tick(self, handler):
        while not self.inbound.empty():
            data = self.inbound.get_nowait()
            
            try:
                msg = json.loads(data)
                t = msg["type"]
                d = msg["data"]
                match t:
                    case "registerRETURN":
                        ph.registerRETURN(handler, d)
                    case _:
                        print(f"[ERROR] UNKNOWN PACKET TYPE")
            except Exception as e:
                print(f"[ERROR] {e}")
                print(f"[World Server Comms Client => Error Processing incoming packets] \n packet = {data}")

    def sendMsg(self, type, data):
        #okay so we want to send data to the data server
        packet = {
            "type": type,
            "data": data
        }
        self.outbound.put_nowait(json.dumps(packet))

    async def receiver(self):
        async for msg in self.ws:
            print(f"[FROM COMMS]: {msg}")
            await self.inbound.put(msg)
    async def sender(self):
        while True:
            msg = await self.outbound.get()
            print(f"[TO COMMS] {msg}")
            await self.ws.send(msg)

    async def start(self, IP, Port):
        self.IP = IP
        self.Port = Port
        async with websockets.connect(f"ws://{self.IP}:{self.Port}") as ws:
            self.ws = ws
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.receiver())
                tg.create_task(self.sender())

    async def stop(self, code, reason):
        self._shutdown_event.set()
        await self.ws.close(code = code, reason = reason)
        