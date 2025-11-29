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
    def __init__(self, handler):
        self.handler = handler
        self.players = {}
        self.server = None
        self._cleaned = set()
        self._clean_lock = asyncio.Lock()
        #this is a dictionary of all the ClientSockets
        #they need to be verified by username before they are let in
        #key is their userID and value is the ClientSocket object

        self.IP = None
        self.Port = None #these are set to real values once the server starts

    
    async def cleanup(self, player, code=1000, reason="Unknown"):
        #first check if we already cleaned this guy, if we did, return
        sessID = player.UUID
        async with self._clean_lock:
            if sessID in self._cleaned:
                return
            self._cleaned.add(sessID)


        self.players.pop(sessID, None)
        #broadcast to everyone that a client lost connnection, was disconnected, etc...
        d = {
            "session_id": sessID,
            "code": code,
            "reason": reason
        }

        #everytime a player disconnects, send updates to the communications server and all of the connected clients
        toComms = {}
        for UUID, player in self.players.items():
            toComms[UUID] = player.username

        self.handler.csc.sendMsg('player_count_update', toComms)
        self.broadcast("playerLOGOUT", d)


    def kick(self, UUID, code = 1008, reason = "You've been kicked!"):
        player = self.players.get(UUID, None)
        
        if player is None:
            print(f"[ERROR] Trying to Kick SESSID:{UUID}")
            return

        if player is not None:
            print(f"Kicking Player: {player.username}@{UUID}")
            asyncio.create_task(self._forceDisconnect(player, code, reason))
                    

    async def _forceDisconnect(self, player, code = 1000, reason = "Forced Disconnect"):
        try:
            await player.ws.close(code=code, reason=reason)
        except Exception as e:
            print(f"[ERROR] Trying to Disconnect {player.UUID}, {repr(e)}")
        finally:
            await self.cleanup(player, code=code, reason=reason)



    def tick(self, handler):
        for player in list(self.players.values()):
            player.tick(handler)


    async def handleConnection(self, ws):
        # This function is called when a new socket has connected to our server,
        # all they have is an IP address and a port, lets create a client for them,
        # and functions to handle incoming and outgoing msgs
        
        #so we no longer need to handle authentication via the world server!
        
        key = self._generateNewSessionID()
        player = ClientSocket(key, ws)
        self.players[key] = player

        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(player.handleReceive())
                tg.create_task(player.handleSend())
        except (wsExceptions.ConnectionClosedOK, wsExceptions.ConnectionClosedError) as e:
            print(f"Client {player.UUID} disconnected!: {e.code} {e.reason}")
        except Exception as e:
            print(f"[Error] Handling Receiving and Sending for {key} {repr(e)}")
        finally:
            await player.ws.wait_closed()
            await self.cleanup(player)

    async def start(self, ListenHost, Port, pingInterval, pingTimeout):
        #Start the WebSocket server to listen for incoming client connections.
        self.server = await serve(self.handleConnection, ListenHost, Port, ping_interval=pingInterval, ping_timeout=pingTimeout)
        self.IP = ListenHost
        self.Port = self.server.sockets[0].getsockname()[1]
        print(f"STARTED WORLD SERVER ON {self.IP}:{self.Port}")
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
            if key not in self.players.keys(): return key