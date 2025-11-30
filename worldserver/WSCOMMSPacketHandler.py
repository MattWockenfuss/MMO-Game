'''
    What packets does the world server send / recieve from comms server

    
    
    
    World Server -> Comms Server
        register
        switch

    Comms Server -> World Server
        registerReturn

'''

import asyncio

def registerACK(handler, d):
    nameID = d.get('nameID')
    worldType = d.get('type')
    worldID = d.get('ID')

    p = {
        'type':worldType
    }
    handler.dsc.sendMsg("world", p)

    handler.csc.worldType = worldType
    handler.csc.worldID = worldID
    handler.csc.worldName = nameID
    print(f"Oh! I am {handler.csc.worldName}")
    print(f"FROM COMMS: {d}")


def switch_REP(handler, d):
    print(f"{d}")

    message = d.get("MESSAGE")
    ip = d.get("IP")  #this also has the port
    CoordsTo = d.get("CoordsTo")
    UUID = d.get("UUID")

    player = handler.csm.players.get(UUID)

    if not player:
        print(f"[COMMS -> WorldServer] 'switch_REP' Packet missing player or their UUID! Dropping...")
        return
    
    if message == "There is no server of type!":
        print(f"User '{player.username}' tried to switch worlds, but there is not world of that type!")
        player.pendingSwitch = False
        return
    
    #okay so the player exists, and we got a world server IP back, send it to the client, 

    p = {
        "IP": ip,
        "CoordsTo": CoordsTo
    }
    player.send('switch_execute', p)
    print(f"{player.username} is going to switch worlds!")
    #lets cleanup the users
    #player.pendingSwitch = False

    asyncio.create_task(
        handler.csm._forceDisconnect(
            player,
            code=4001,
            reason=f"Switching to {CoordsTo}"
        )
    )
