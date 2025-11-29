





def register(handler, d, worldclient):
    #alright in this function, we need to figure out what kind of world it needs to be, and send it back
    #we need to set out port to the one provided
    worldclient.port = d.get('port')
    #print(f"REGISTERING WORLD SERVER AT {worldclient.ip}:{worldclient.port}")



    '''
        Alright so whats the best way to assign world types, well we want it to be round robin, okay, and then a max? or what
        we want to be able to show off load balancing and maybe have a a world server wait and show off crashes

        okay so the algorithm has been simplifed to go for the first lowest whos current is less than max
    '''
    currentCountDict = {}
    for key, value in handler.wcm.desiredWorlds.items():
        #print(f"{key}: {value}")
        #for every world type, loop through all the worlds and how many are of this type
        currentCountDict[key] = 0
        #print(currentCountDict)
        for world in handler.wcm.worldclients.values():
            #print(world)
            if world.type is not None:
                if key == world.type:
                    currentCountDict[key] += 1

    #print(handler.wcm.desiredWorlds)
    #print(currentCountDict)

    #alright, so now loop through the current counts and find the lowest whos current is less than desired

    lowestType = None
    for key, value in currentCountDict.items():
        if lowestType is None:
            lowestType = key

        #first check if its less than max, to even consider
        if value < handler.wcm.desiredWorlds.get(key):
            #print(f"currentCount: {value} IS LESS THAN {handler.wcm.desiredWorlds.get(key)}")
            #then the current is less than desired
            #if its value is lower than currentcount@key then set new lowest type
            #print(f"CHECKING IS currentCount: {value} LESS THAN {currentCountDict[lowestType]}")
            if value < currentCountDict[lowestType]:
                #print(f"currentCount: {value} IS LESS THAN {currentCountDict[lowestType]}")
                lowestType = key


    #print(f"Type       Desired  Current")
    for key, value in handler.wcm.desiredWorlds.items():
        #print(f"{key}       {value} {currentCountDict[key]}")
        pass
    

    #alright now we know what type they should be
    #what should their ID be?
    #first lowest?

    existing_ids = set()
    for world in handler.wcm.worldclients.values():
        if world is worldclient: continue
        # We check if the world's type matches the target type AND
        # ensure the world's ID is not None before adding it to the set.
        if world.type == lowestType and world.ID is not None:
            existing_ids.add(world.ID)

    # 2. Find the lowest available ID
    i = 1
    while i in existing_ids:
        # If the current number 'i' is already in our set of existing IDs,
        # increment 'i' and check the next number. Set lookups (i in existing_ids)
        # are extremely fast (O(1) complexity).
        i += 1

    found_id = i
    #print(f"Found the lowest available ID for type {lowestType}: {found_id}")

    #okay so this world can now update its stuff, its going to be lowestType-i
    worldclient.type = lowestType
    worldclient.ID = i
    worldclient.updateName()

    print(f"[{worldclient.ip}:{worldclient.port}] REGISTERING NEW WORLD SERVER")
    print(f"\tASSIGNED WORLD {worldclient.nameID}")

    

    p = {
        'nameID': worldclient.nameID,
        'type': worldclient.type,
        'ID': worldclient.ID,
    }
    worldclient.send('registerACK', p)

def switch(handler, d , worldclient):
    print(f"SWITCH: {d}")


def player_count_update(handler, d , worldclient):
    #this function is sent by the world server everytime their player count changes to keep the comms server up to date
    #we recieve a list of usernames of currently connected players? or just the num lets do list
    #we recieve a list of usernames of currently connected players to that server
    #print(f"player count update! {d}")

    #we keep track of a dictionary of UUIDs and Usernames currently connected to this server, then we update the player count
    worldclient.players = d
    worldclient.playerCount = len(worldclient.players)
    