import asyncio
from websockets.asyncio.server import serve
import websockets.exceptions as wsExceptions
import random, string

from clientsocket import ClientSocket

class ClientSocketManager:
    def __init__(self):
        self.clients = {}
        self.players = {}  #clients whom have been authenticated, remember, ids or keys are unique across both lists
        self.server = None
        #this is a dictionary of all the ClientSockets
        #they need to be verified by username before they are let in
        #key is their userID and value is the ClientSocket object


    
    def cleanup(self, client):
        #remove the client from either of our lists
        self.clients.pop(client.session_id, None)
        self.players.pop(client.session_id, None)


    def kick(self, session_id, code = 1008, reason = "You've been kicked!"):
        client = self.clients.get(session_id, None)
        player = self.players.get(session_id, None)
        
        if client is None and player is None:
            print(f"[ERROR] Trying to Kick SESSID:{session_id}")
            return
        
        
        if client is not None:
            print(f"Kicking Client SESSID:{session_id}")
            asyncio.create_task(self._forceDisconnect(client, code, reason))

        if player is not None:
            print(f"Kicking Player: {player.username}@{session_id}")
            asyncio.create_task(self._forceDisconnect(player, code, reason))
                    

    async def _forceDisconnect(self, client, code = 1001, reason = "Forced Disconnect"):
        try:
            client.send("disconnect", {"reason": reason})
        except Exception:
            pass
        try:
            await client.ws.close(code=code, reason=reason)
        except Exception as e:
            print(f"[ERROR] Trying to Disconnect {client.session_id}, {repr(e)}")
        finally:
            self.cleanup(client)



    def tick(self, handler):
        for id, client in list(self.clients.items()): #chatGPT said run them in lists? so that they are 'snapshots' not the real thing
            client.tick(handler)
            #print(f"ID: {id} {client.id}")
        for player in list(self.players.values()):
            player.tick(handler)


    async def handleConnection(self, ws):
        # This function is called when a new socket has connected to our server,
        # all they have is an IP address and a port, lets create a client for them,
        # and functions to handle incoming and outgoing msgs
        
        key = self._generateNewSessionID()
        client = ClientSocket(key, ws)
        self.clients[key] = client

        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(client.handleReceive())
                tg.create_task(client.handleSend())
        except (wsExceptions.ConnectionClosedOK, wsExceptions.ConnectionClosedError) as e:
            print(f"Client {client.id} disconnected!: {e.code} {e.reason}")
        finally:
            self.cleanup(client)

    async def start(self, ListenHost, Port):
        self.ListenHost = ListenHost
        self.Port = Port
        print(f"{ListenHost} : port={Port} and is type {type(ListenHost)}:{type(Port)}")
        self.server = await serve(self.handleConnection, self.ListenHost, self.Port)
        await self.server.serve_forever()
        
        

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()

    def _generateNewSessionID(self):
        characterPool = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characterPool) for i in range(8))
            if key not in self.players.keys() and key not in self.clients.keys(): return key