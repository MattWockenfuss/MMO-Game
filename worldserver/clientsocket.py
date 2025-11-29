"""
worldserver/clientsocket.py

ClientSocket class represents an individual client WebSocket connection to the world server.

Responsibilities:
- Manage incoming and outgoing message queues asynchronously.
- Deserialize incoming JSON packets and dispatch them to appropriate packet handlers.
- Serialize outgoing messages and send them asynchronously via the websocket.
- Track client session metadata such as IP, port, authentication status, and session ID.
"""

'''
When a new client connects, a ClientSocket instance is created to handle:
- Receiving incoming messages asynchronously and queuing them for processing.
- Sending queued outgoing messages asynchronously to the client.
- Managing client identification by unique UUID.
- Authentication status tracking.
'''

import json
import asyncio
import WSCPacketHandler as ph


from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

class ClientSocket():
    def __init__(self, UUID, ws):
        self.UUID = UUID
        self.ws = ws
        self.ip = ws.remote_address[0]
        self.port = ws.remote_address[1]
        self.inbound = asyncio.Queue()
        self.outbound = asyncio.Queue()

        print(f"NEW CLIENT: [{self.ip}:{self.port}] UUID: {self.UUID}")

    def tick(self, handler):
        while not self.inbound.empty():
            msg = self.inbound.get_nowait()
            t = msg["type"]
            d = msg["data"]
            match t:
                case "login":
                    ph.login(handler, d, self)
                case "world":
                    pass
                case "move":
                    ph.WSonMove(handler, d, self)

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
                print(f"SEND TO CLIENT [self.UUID] {msg}")
                await self.ws.send(msg)
        except ConnectionClosedOK:
            print(f"[{self.UUID}]'s session was closed gracefully")
            raise
        except ConnectionClosedError:
            print(f"[ERROR] Sending {self.UUID} a msg")
            raise
        except Exception as e:
            print(f"[UNEXPECTED ERROR] Sending {self.UUID} a msg, {repr(e)}")
            raise
            


    async def handleReceive(self): 
        """
        Coroutine handling asynchronous reception of incoming messages from the client websocket.

        Decodes JSON messages and enqueues them for processing.

        Logs received messages and handles connection closing or errors.
        """

        try:
            async for msg in self.ws:
                #this is called everytime the world server receives data from this client
                
                #okay so we just received a packet?
                decoded = json.loads(msg)
                #print(json.dumps(decoded, indent=4))  #json.dumps takes in a JSON object, so we have to load it first
                #if decoded.get("type") != "move":
                print(f"[UUID:{self.UUID}  {self.ip}:{self.port}] MSG: {msg}")
                self.inbound.put_nowait(decoded)
        except ConnectionClosedOK:
            raise
        except ConnectionClosedError:
            print(f"[ERROR] Receiving {self.UUID} a msg")
            raise
        except Exception as e:
            print(f"[UNEXPECTED ERROR] Receiving {self.UUID} a msg, {repr(e)}")
            raise