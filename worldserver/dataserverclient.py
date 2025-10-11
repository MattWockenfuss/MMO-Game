#this object is represents the link between the data server and the world server
#this is the client in the relationship, the data server is the server

import websockets
import asyncio
import json
import reprlib

import WSDPacketHandler as ph

class DataServerClient:
    def __init__(self):
        self.IP = None        #these are the ip and port of the data server
        self.Port = None
        self.outbound = asyncio.Queue()
        self.inbound = asyncio.Queue()  #might need tweaking in the future, limit?
        self._shutdown_event = asyncio.Event()
    
    def tick(self, handler):
        while not self.inbound.empty():
            data = self.inbound.get_nowait()
            #print(data)
            
            try:
                msg = json.loads(data)
                t = msg["type"]
                d = msg["data"]
                match t:
                    case "world":
                        ph.WSonWorld(handler, d)
                    case "login":
                        ph.WSonLogin(handler, d)
                    case default:
                        pass
            except Exception as e:
                print(f"[ERROR] {e}")
                print(f"[World Server Data Client => Error Processing incoming packets] \n packet = {data}")




            




    def sendMsg(self, type, data):
        #okay so we want to send data to the data server
        packet = {
            "type": type,
            "data": data
        }
        self.outbound.put_nowait(json.dumps(packet))

    async def receiver(self):
        myrepr = reprlib.Repr()
        myrepr.maxstring = 100

        async for msg in self.ws:
            print(f"[FROM DS]: {myrepr.repr(msg)}")
            await self.inbound.put(msg)
            


    async def sender(self):
        while True:
            #print(f"im awaiting for something to be put in the queue")
            msg = await self.outbound.get()
            print(f"[TO DS] {msg}")
            await self.ws.send(msg)
            #self.outbound_queue.task_done()

    async def start(self, IP, Port):
        self.IP = IP
        self.Port = Port
        async with websockets.connect(f"ws://{self.IP}:{self.Port}") as ws:   #python only allows plain variable names after as, not 'attribute access' 
            self.ws = ws
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.receiver())
                tg.create_task(self.sender())

    async def stop(self, code, reason):
        self._shutdown_event.set()
        await self.ws.close(code = code, reason = reason)
        