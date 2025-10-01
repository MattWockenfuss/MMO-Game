'''
okay so we are going to create a client socket when a new client connects and it will handle incoming msgs
it will add to the queue and send msgs to the client

what are user IDs?
whenever we create an account it will create one?


'''

import json
import asyncio
import WSCPacketHandler as ph


from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

class ClientSocket():
    def __init__(self, session_id, ws):
        self.session_id = session_id
        self.ws = ws
        self.ip = ws.remote_address[0]
        self.port = ws.remote_address[1]
        self.inbound = asyncio.Queue()
        self.outbound = asyncio.Queue()
        self.is_authed = False

        print(f"NEW CLIENT: [{self.ip}:{self.port}] SESSION_ID: {self.session_id}")

    def tick(self, handler):
        while not self.inbound.empty():
            msg = self.inbound.get_nowait()
            t = msg["type"]
            d = msg["data"]
            match t:
                case "login":
                    ph.WSonLogin(handler, d, self)
                case "world":
                    pass
                case "move":
                    ph.WSonMove(handler, d, self)


        #await self.ws.send(f"SENDING BACK: {msg}")


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
                #print(f"Sending {msg}")
                await self.ws.send(msg)
        except(ConnectionClosedOK, ConnectionClosedError):
            print("Connection Error!")
            return
        except asyncio.CancelledError:
            print("handleSend cancelled by TaskGroup")
            # choose pass or re-raise; see notes below
            raise
        except Exception as e:
            print(f"Unexpected Error in handleSend(), {repr(e)}")
        finally:
            print("Awaiting Close!")
            await self.ws.wait_closed()


    async def handleReceive(self): 
        try:
            async for msg in self.ws:
                #this is called everytime the world server receives data from this client
                
                #okay so we just received a packet?
                decoded = json.loads(msg)
                #print(json.dumps(decoded, indent=4))  #json.dumps takes in a JSON object, so we have to load it first
                if decoded.get("type") != "move":
                    print(f"[SESS-ID:{self.session_id}  {self.ip}:{self.port}] MSG: {msg}")
                self.inbound.put_nowait(decoded)



                #handle packet info
                #move packet
                #alex takes damage
                #pranav kills a monster
                #matt picks up an item

                #add to the queue
        except (ConnectionClosedOK, ConnectionClosedError) as e:
            return