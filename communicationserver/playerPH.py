


def AUTH_REQ(handler, d, playerclient):
    print(f"AUTH_REQ: {d}")

    # so some is trying to authenticate, they sent us their username and password
    playerclient.username = d.get("username")
    playerclient.password = d.get("password")

    #this client is trying to authenticate, first lets check if someone has already logged in using this username
    for wUUID, worldserver in  handler.wcm.worldclients.items():
        #lets loop through every world, and if found than break, otherwise they are good
        for pUUID, playername in worldserver.players.items():
            
            if playerclient.username == playername:
                #then they are already logged in!
                dx = {
                    "AUTH": "AUTH_FAILED",
                    "MESSAGE": "Username already in use!"
                }
                playerclient.send("authenticateRES", dx)
                handler.pcm.forceDisconnect(playerclient, code=1001, reason="Username Already in Use!")
                return




    #alright so we set this clients username and password, now we send to the dataserver for check
    dx = {
        "username": playerclient.username,
        "password": playerclient.password,
        "UUID": playerclient.UUID
    }
    handler.dsc.sendMsg("AUTH_REQ", dx)



