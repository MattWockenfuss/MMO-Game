"""
worldserver/WSDPacketHandler.py

Packet handler module for processing incoming packets from the data server to the world server.

Responsibilities:
- Handle world data synchronization from the data server.
- Process login authentication responses from the data server.
- Update world state and notify clients accordingly.
- Manage player authentication status and broadcast login events.
"""

import json
from enemy import Enemy

'''
This file lists all the functions that handle packets for the world server from the
DATA SERVER

'''

#all packets are built like so
testpacket = {
    "type":"world",
    "data":
            {
                'World-Name': 'Forest', 
                'Tile-Map': 'forest.png', 
                'World-Entrance-Color': '#33cc33', 
                'world-data': 'BQUFBQUFBQUF', 
                'world-width': 3
            }
}
#       We just received the world data from the data server, store in world, also parse and decode the data, 
#       setting the width and height of the world as well,
#       type = "world" data = {World-Name:"", Tile-Map:"", World-Entrance-Color:"", world-data:"", world-width:""}
#       type = "tiles" data = {name:"", id:"", lore-blurb:"", is-Solid:"", map-color:"", Sprite:""}
def WSonWorld(handler, d):
    """
    Handle 'world' type packets from the data server.

    Receives world metadata, tileset, static objects, and enemy herd information.

    Updates the server's world state by setting world data and associated dictionaries.

    Args:
        handler (Handler): The main server handler containing subsystem references.
        d (dict): Packet data containing keys like 'world', 'tiles', and 'statics'.
    """

    #print(d)
    print("---------------------------------------------------------------------------------")
    print(d.get("world"))
    print("---------------------------------------------------------------------------------")
    print(d.get("tiles"))
    print("---------------------------------------------------------------------------------")
    print(d.get("statics"))

    # for tile in d.get("tiles"):
    #     print(tile)

    for static in d.get("statics"):
        print(static)

    # for enemyHerd in d.get("world").get("enemyHerds"):
    #     print(f"")
    #     for keys, values in enemyHerd.items():
    #         if not keys == "name": print(f"\t", end="")
    #         print(f"{keys}: {values}")



    # worldName =           d.get("world").get("World-Name")
    # tileMap =             d.get("world").get("Tile-Map")
    # worldEntranceColor =  d.get("world").get("World-Entrance-Color")
    # worldData =           d.get("world").get("world-data")
    # worldWidth =          d.get("world").get("world-width")

    handler.world.setWorldData(d)



def WSonLogin(handler, d):
    """
    Handle 'login' type packets from the data server which indicate the result of user authentication.

    If the user exists and is authenticated:
     - Move client from unauthenticated to authenticated players list.
     - Update client information from data server userdata.
     - Send current world entities and enemy data to the client.
     - Notify all other players of the new player's login.

    If authentication fails:
     - Notify client of failure.
     - Kick the client from the server.

    Args:
        handler (Handler): The main server handler containing subsystem references.
        d (dict): Packet data containing login results and user information.

    Packet examples:
        Exists: {'username': ..., 'color': ..., 'message': 'EXISTS', 'userdata': ..., 'session_id': ...}
        Not Exists: {'username': ..., 'message': 'NOT', 'session_id': ...}
    """
    
    username = d.get("username")
    color = d.get("color")
    message = d.get("message")
    userdata = d.get("userdata")
    session_id = d.get("session_id")

    client = handler.csm.clients.get(session_id)

    if client is None:
        print(f"[DS->WS] BAD LOGIN PACKET, {d}")
        return


    if message == "EXISTS":
        print(f'{session_id} tried to login as {username}, They are in the Database!')

        #lets auth them right here, no method
        handler.csm.clients.pop(session_id)
        handler.csm.players[session_id] = client
        client.is_authed = True

        client.x = 200
        client.y = 200
        client.username = username
        client.session_id = session_id
        client.color = color
        client.userdata = userdata
        
        #lets also send them all of the entities currently in the world as well
        #lets build an enemies dictionary to send to the player as well
        #         
        
        enemies = {}
        #loop through every enemy in the game and send it to the player
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

        p = {
            "world": handler.world.worldDict,
            "tiles": handler.world.tilesDict,
        }
        client.send('world', p)
        client.send('Enemy', enemies)
        print(f"ENEMIES: {enemies}")

        dataToSend = {"auth":"ok"}
        client.send('loginVerify', dataToSend)

        for sessID, player in handler.csm.players.items():
            #here we are looping through all the clients, and if they didnt just log in, tell them
            #someone just logged in, and tell the person who just logged in they exist
            if sessID != session_id:
                da = {
                    "username": player.username,
                    "x": player.x,
                    "y": player.y,
                    "session_id": player.session_id,
                    "color": player.color
                }
                client.send("onOtherPlayer", da)
                da = {
                    "username": client.username,
                    "x": client.x,
                    "y": client.y,
                    "session_id": client.session_id,
                    "color": client.color
                }
                player.send("login", da)

    else:
        print(f"{username} is NOT in the database!")
        #then kick whoever tried to connect as me
        #alright, we also want to tell the client they are okay to be logged in
        dataToSend = {"auth":"fail"}
        client.send('loginVerify', dataToSend)   #this is working
        handler.csm.kickClient(client.id, code=4001, reason="Username not registered!")


