import json
from websockets import ConnectionClosedOK, ConcurrencyError
import DSPacketHander as ph
import asyncio
from websockets.asyncio.server import serve


class WorldClientManager:
    def __init__(self):
        self.server = None
        self.handler = None


    async def handleConnection(self, websocket): #just for dataserver
        try:
            async for message in websocket:
                try:
                    msg = json.loads(message)  #returns a dictionary of lists, strings, and other dictionaries
                    print(f"Received: {msg} from {websocket.remote_address}")
                    t = msg["type"]
                    d = msg["data"]
                    print(f"{t}     :     {d}")
                    match t:
                        case "login":
                            await ph.DSonLogin(self.handler, d, websocket)
                        case "world":
                            await ph.DSonWorld(self.handler, d, websocket)
                        case _:
                            print(f"[ERROR PACKET READ] {msg}")

                except (json.JSONDecodeError, KeyError) as e:
                    msg = {"message": f"Not Decodable in JSON from {websocket.remote_address}"}
                except Exception as e:
                    msg = {"message": e}
                    await websocket.send(json.dumps(msg))
        
        except (ConnectionClosedOK, ConnectionError) as e:
            print(f"Cient {websocket.remote_address} disconnected: {e.code} {e.reason}")
        except Exception as e:
            print(f"Error: {e}")

    async def start(self, ListenHost, Port, handler):
        self.ListenHost = ListenHost
        self.Port = Port
        self.handler = handler

        self.server = await serve(self.handleConnection, ListenHost, Port)
        await self.server.serve_forever()

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()