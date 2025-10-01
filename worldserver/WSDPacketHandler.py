import json
import base64
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
    
def WSonWorld(handler, d):
    #print(f"world data: {d["world-data"]}")
    handler.world.setWorldData(base64.b64decode(d["world-data"]), d["world-width"])
    handler.world.printWorldData()
    handler.world.setWorldString(d)
    #print(handler.world.getWorldData())



'''
    In WSonLogin, we accept the login packet from the dataserver, which tells us whether or not the user is authenticated in the Dataserver, and if so,
    sends back their stored userdata
'''
def WSonLogin(handler, d):
    
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
        client.player = Player(200, 200, client.name, client.session_id, color) #hmm
        client.data = userdata




        client.send('world', handler.world.getWorldString())
        #we also want to tell them about all the other players in the world, they need, players x, y, session_id, username, and color
        #print(f"sending them the client data!")
        #print(f"number of players: {len(handler.csm.players)}")
        


        #alright, we also want to tell the client they are okay to be logged in
        dataToSend = {"auth":"ok"}
        client.send('loginVerify', dataToSend)   #this is working

        for session_id, player in handler.csm.players.items():
            
            #print(f"{client.session_id} =? {player.session_id}")
            if session_id == client.session_id: #client is the one who just logged in, tell everyone else someone just logged in
                continue
            print(f"{player.data}")

            # print(f"sending world data for {player.username}")
            da = {
                "username": player.player.username,
                "x": player.player.x,
                "y": player.player.y,
                "session_id": player.player.session_id,
                "color": player.player.color
            }
            client.send("onOtherPlayer", da)
            #okay so we just told the client about this player, tell this player about the client
            da = {
                "username": client.player.username,
                "x": client.player.x,
                "y": client.player.y,
                "session_id": client.player.session_id,
                "color": client.player.color
            }
            player.send("login", da)

    else:
        print(f"{d["username"]} is NOT in the database!")
        #then kick whoever tried to connect as me
        #alright, we also want to tell the client they are okay to be logged in
        dataToSend = {"auth":"fail"}
        client.send('loginVerify', dataToSend)   #this is working
        handler.csm.kickClient(client.id, code=4001, reason="Username not registered!")


