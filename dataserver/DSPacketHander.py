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

async def DSonWorld(handler, data, ws):
    print(data)
    for world in handler.configs["worlds"]:
        if world.get("World-Name") == data["World-Name"]:
            data = {
                "type":"world",
                "data": world
            }
            await ws.send(json.dumps(data))
            break
    else:
        await ws.send(f"World {data} not found!")