import asyncio
from websockets.asyncio.server import serve
import websockets.exceptions as wsExceptions
import random, string

from clientsocket import ClientSocket
from player import Player

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
        if hasattr(client, "id"):
            self.clients.pop(client.id, None)
        if hasattr(client, "session_id") and client.session_id: #by saying and client.session_id, we are asking if its truthy, as in,                     
            self.players.pop(client.session_id, None)      #is client.session_id not None, not empty string


    def kickClient(self, playerUsername, code = 1008, reason = "Auth Failed"):
        for players in list(self.players.values()):
            if players.player.username == playerUsername:
                    print(f"Kicking {players.player.session_id}")
                    asyncio.create_task(self._forceDisconnect(players, code, reason))
    async def _forceDisconnect(self, client, code = 1001, reason = "Forced Disconnect"):
        try:
            client.send("disconnect", {"reason": reason})
        except Exception:
            pass
        
        try:
            await client.ws.close(code=code, reason=reason)
        except Exception:
            pass
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