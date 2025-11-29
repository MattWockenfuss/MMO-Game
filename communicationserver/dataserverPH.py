





def authenticateREP(handler, d):
    print(d)
    UUID = d.get("UUID")
    userdata = d.get('userdata')
    username = d.get('username')
    message = d.get('message')

    #first check if UUID is supplied
    if UUID is None:
        return

    client = handler.pcm.unauthedclients.get(UUID)

    #next check if there is a client with this UUID
    if client is None:
        return

    #   we know there is some client associated with this

    if message != "AUTH_OK":
        #okay so they are not authenticated, we want to tell the player so, kick them from the server
        dx = {"AUTH": "AUTH_FAILED"}
        client.send("authenticateRES", dx)
        handler.pcm.forceDisconnect(client, code=1001, reason="Failed Authentication")
        return

    #okay so this means the player pass authentication, and they are an unauthed client
    #lets move them to the authed section

    handler.pcm.unauthedclients.pop(UUID, None)
    handler.pcm.playerclients[UUID] = client

    #okay so the client has been moved to the other list
    #now lets send them the IP of the world server they can connect to

    uuidOfServer = handler.wcm.getBestServer(handler.wcm.defaultServer)
    server = handler.wcm.worldclients[uuidOfServer]

    print(f"Sending '[{UUID}]:{client.username}' to '{server.nameID}, ({server.getIPString()})'!") 

    dx = {
        "IP": server.getIPString(),
        "AUTH": "AUTH_OK"
    }
    client.send('AUTH_REP', dx)





