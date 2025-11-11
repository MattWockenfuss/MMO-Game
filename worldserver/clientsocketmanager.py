"""
worldserver/clientsocketmanager.py

ClientSocketManager class manages WebSocket client connections to the world server.

Responsibilities:
- Track all connected clients and authenticated players separately.
- Handle new client connections, message sending, and receiving.
- Facilitate kicking and forceful disconnection of clients or players.
- Periodically tick clients and players for update processing.
- Broadcast messages to all authenticated players.
- Maintain unique session IDs for each client connection.
"""

import asyncio
from websockets.asyncio.server import serve
import websockets.exceptions as wsExceptions
import random, string

from clientsocket import ClientSocket

class ClientSocketManager:
    #Manages all connected client sockets and authenticated players.
    def __init__(self):
        self.clients = {}
        self.players = {}  #clients whom have been authenticated, remember, ids or keys are unique across both lists
        self.server = None
        self._cleaned = set()
        self._clean_lock = asyncio.Lock()
        #this is a dictionary of all the ClientSockets
        #they need to be verified by username before they are let in
        #key is their userID and value is the ClientSocket object


    
    async def cleanup(self, client, code = 1000, reason = "Unknown"):
        """
        Cleanup client data structures when connection is closed or disconnected.

        Args:
            client (ClientSocket): Client to clean up.
            code (int): WebSocket close code.
            reason (str): Reason for disconnection.
        """

        #first check if we alreadu cleaned this guy, if we did, return
        sessID = client.session_id
        async with self._clean_lock:
            if sessID in self._cleaned:
                return
            self._cleaned.add(sessID)


        self.clients.pop(client.session_id, None)
        self.players.pop(client.session_id, None)
        #broadcast to everyone that a client lost connnection, was disconnected, etc...
        d = {
                "session_id": client.session_id,
                "code": code,
                "reason": reason
        }
        self.broadcast("playerLOGOUT", d)


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
                    

    async def _forceDisconnect(self, client, code = 1000, reason = "Forced Disconnect"):
        try:
            await client.ws.close(code=code, reason=reason)
        except Exception as e:
            print(f"[ERROR] Trying to Disconnect {client.session_id}, {repr(e)}")
        finally:
            await self.cleanup(client, code=code, reason=reason)



    def tick(self, handler):
        for id, client in list(self.clients.items()): #chatGPT said run them in lists? so that they are 'snapshots' not the real thing
            client.tick(handler)
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
        except Exception as e:
            print(f"[Error] Handling Receiving and Sending for {key} {repr(e)}")
        finally:
            await client.ws.wait_closed()
            await self.cleanup(client)

    async def start(self, ListenHost, Port, pingInterval, pingTimeout):
        #Start the WebSocket server to listen for incoming client connections.
        
        self.ListenHost = ListenHost
        self.Port = Port
        self.server = await serve(self.handleConnection, self.ListenHost, self.Port, ping_interval=pingInterval, ping_timeout=pingTimeout)
        self.Port = self.server.sockets[0].getsockname()[1]
        print(f"STARTED WORLD SERVER ON {self.ListenHost}:{self.Port}")
        await self.server.serve_forever()
        
    def broadcast(self, type, data):
        for sessID, player in list(self.players.items()):
            player.send(type, data)

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()

    """
    Generate a unique 8-character alphanumeric session ID.

    Ensures no collisions with existing clients or players.

    Returns:
        str: Unique session identifier.
    """
    def _generateNewSessionID(self):
        characterPool = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characterPool) for i in range(4))
            if key not in self.players.keys() and key not in self.clients.keys(): return key