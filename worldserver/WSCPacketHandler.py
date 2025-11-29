"""
worldserver/WSCPacketHandler.py

Packet handler module for processing incoming client packets on the world server.

Responsibilities:
- Handle client packets related to player movement and login.
- Update server-side client state based on received packets.
- Broadcast relevant state changes (e.g., movement) to other connected clients.
- Validate client authentication before processing sensitive packets.
- Interact with the data server client (dsc) for login processing.
"""

import json
import base64
from enemy import Enemy
from static_entity import StaticEntity
'''
    This file handles all packets For the world server FROM THE
    CLIENTS

'''


'''
    This function handles the onMove packet from the player, updating their x and y positions in the server, and broadcasting
    to the rest of the players connected to this world server.
'''
def WSonMove(handler, d, player):
    """
    Handle a player 'move' packet from a client.

    Updates the player's x and y position coordinates according to the packet data,
    and broadcasts this movement update to all other authenticated connected players.

    Args:
        handler (Handler): The main server handler containing subsystem references.
        d (dict): The parsed packet data containing 'x' and 'y' fields.
        clientSocket (ClientSocket): The client socket object representing the player connection.

    Behavior:
        - Verifies the client is authenticated.
        - Validates presence of x and y coordinates in the packet.
        - Updates the player's position on the server.
        - Sends movement update packets to all other connected players.
    """

    try:
        if not player:
            print(f"Move Packet From broken client socket!")
            return
        
        x = d.get("x")
        y = d.get("y")

        if x is None or y is None:
            print(f"Bad Movement Packet! (Missing x/y): {d}")
            return
        
        player.x = x
        player.y = y

        for UUID, otherPlayer in list(handler.csm.players.items()):
            if otherPlayer is player:
                continue
            da = {
                'UUID': player.UUID,
                'x': x,
                'y': y
            }
            otherPlayer.send('move', da)


    except Exception:
        import traceback
        traceback.print_exc()



def login(handler, d, player):
    '''
        This function handles user logging in, they have already been authenticated and sent to us
    
    '''
    
    #what do we want to do?
    #give them world data, other player data, entity data, tile data?
    #add them to our list

    newUUID = handler.em.generateUUID()
    username = d.get('username')
    color = d.get('color')
    handler.csm.players.pop(player.UUID, None)



    handler.csm.players[newUUID] = player

    print(f"Player Connecting! [{username}, {color}]")
    #now we need to add the player to our list and send them the data and stuff!
    player.x = 200
    player.y = 200
    player.username = username
    player.color = color
    player.UUID = newUUID

    #we want to tell them what kind of server we are
    p = {
        "nameID": handler.csc.worldName
    }
    player.send('login_res', p)


    #everytime a player logs in, send updates to the communications server and all of the connected clients
    toComms = {}
    for UUID, player in handler.csm.players.items():
        toComms[UUID] = player.username

    handler.csc.sendMsg('player_count_update', toComms)

    p = {
        "world": handler.world.worldDict,
        "tiles": handler.world.tilesDict,
        "tileMap": handler.world.tileMapDict,
        "statics": handler.world.staticsDict
    }
    print(f"Tiles DICT: {handler.world.tilesDict}")
    print(f"TilesMap DICT: {handler.world.tileMapDict}")
    print(f"STATICS DICT: {handler.world.staticsDict}")
    player.send('world', p)


    enemies = {}
    statics = {}


    for entity in handler.em.items:
        print(entity.UUID)
        if isinstance(entity, Enemy):
            #then this is an Enemy, build the appropriate packet
            px = {
                "UUID": entity.UUID,
                "type": entity.type,
                "x": entity.x,
                "y": entity.y,
                "level": entity.level,
                "health": entity.health,
                "attack": entity.attack,
                "attackSpeed": entity.attackSpeed,
                "dodgeChance": entity.dodgeChance,
                "criticalChance": entity.criticalChance,
                "movementSpeed": entity.movementSpeed,
                "visionRadius": entity.visionRadius,
                "size": entity.size,
                "movementType": entity.movementType
            }
            enemies[entity.UUID] = px
        if isinstance(entity, StaticEntity):
            #then this is a static entity packet, build appropriately
            px = {
                "UUID": entity.UUID,
                "type": entity.type,
                "x": entity.x,
                "y": entity.y,
                "level": entity.level,
                "health": entity.health
            }
            statics[entity.UUID] = px

    player.send('enemy', enemies)
    player.send('static', statics)
    print(f"ENEMIES: {enemies}")

    for UUID, otherplayer in handler.csm.players.items():
        #here we are looping through all the clients, and if they didnt just log in, tell them
        #someone just logged in, and tell the person who just logged in they exist
        if UUID != newUUID:
            #then this is another player on the server, tell them someone just logged in
            #and then tell the person who just logged in about this person
            toPlayer = {
                "username": otherplayer.username,
                "x": otherplayer.x,
                "y": otherplayer.y,
                "UUID": otherplayer.UUID,
                "color": otherplayer.color
            }
            
            toOther = {
                "username": player.username,
                "x": player.x,
                "y": player.y,
                "session_id": player.UUID,
                "color": player.color
            }

            otherplayer.send("login", toOther)
            player.send("playerLOGIN", toPlayer)