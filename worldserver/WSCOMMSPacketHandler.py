'''
    What packets does the world server send / recieve from comms server

    
    
    
    World Server -> Comms Server
        register
        switch

    Comms Server -> World Server
        registerReturn

'''


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