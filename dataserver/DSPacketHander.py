import json
'''
This file holds all the functions that handle all packets for the data server from the
WORLD SERVER
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

 
async def DSonLogin(handler, data, ws):
    #this is when the server wants to verify login attempt, see if the username is in the database
    #if it is, say so and send it back, if not say so
    #print(f"searching players for {data}")
    for player in handler.configs["players"]:
        if player.get("name") == data["username"]:
            d = {
                'username': data["username"],
                'color': data["color"],
                'message': 'EXISTS',
                'userdata': player,
                'session_id': data["session_id"]
            }
            break
    else:
        d = {
            'username': data["username"],
            'message': 'NOT',
            'session_id': data["session_id"]
        }

    p = {
        'type': "login",
        'data': d
    }
    await ws.send(json.dumps(p))


async def AUTH_REQ(handler, d, ws):
    username = d.get('username')
    password = d.get('password')
    UUID = d.get('UUID')
    print(f"Attempting to authenticate {username}")
    for player in handler.configs["players"]:
        if player.get("name") == username:
            d = {
                'UUID': UUID,
                'userdata': player,
                'message': 'AUTH_OK'
            }
            break
    else:
        d = {
            'UUID': UUID,
            'username': username,
            'message': 'NOT AUTH'
        }

    p = {
        'type': "authenticateREP",
        'data': d
    }
    await ws.send(json.dumps(p))

async def DSonWorld(handler, data, ws):
    print(f"RECEIVING {data} FROM WORLD SERVER")

    for world in handler.configs["worlds"]:#this is a list of dictionaries
        print(f"Getting {world.get('World-Name')}")
        for key, value in world.items():
            if key == "world-data":
                print("world-data: ...")
            else:
                print(f"{key}: {value}")

        print(f"is {world.get("folderName")} ==? {data["type"]}")
        if world.get("folderName") == data["type"]:
            data = {
                "type":"world",
                "data": {
                    "world": world,
                    "tiles": handler.configs["tiles"],
                    "tileMap": handler.configs["tileMap"],
                    "statics": handler.configs["statics"]
                }
            }
            
            # for key, value in data.items():
            #     if key == "data":
            #         for key2, value2, in value.items():
            #             print()
            #             print(f"\t{key2}: {value2}")
            #     else:
            #         print(f"{key}: {value}")

            # print(f"SENDING PACKET TO WORLD SERVER")
            await ws.send(json.dumps(data))
            break
    else:
        await ws.send(f"World {data} not found!")