import json
import base64
'''
    This file handles all packets For the world server FROM THE
    CLIENTS

'''


'''
    This function handles the onMove packet from the player, updating their x and y positions in the server, and broadcasting
    to the rest of the players connected to this world server.
'''
def WSonMove(handler, d, clientSocket):
    try:
        if not clientSocket.is_authed or clientSocket.player is None:
            print(f"Move Packet from unauthenticated client, or player is null")
            return
        
        x = d.get("x")
        y = d.get("y")

        if x is None or y is None:
            print(f"Bad Movement Packet! (Missing x/y): {d}")
            return
        
        clientSocket.player.x = x;
        clientSocket.player.y = y;

        for sessID, otherPlayer in list(handler.csm.players.items()):
            if otherPlayer is clientSocket:
                continue
            da = {
                'session_id': clientSocket.player.session_id,
                'x': x,
                'y': y
            }
            otherPlayer.send('move', da)


    except Exception:
        import traceback
        traceback.print_exc()





'''
    This function handles the type 'login' packet from the clients. They tell us their username, password and color. 
    We associate this with their temporary client, and pass the data along to the dataserver to be authenticated.

'''
def WSonLogin(handler, d, clientSocket):
    print(f"Handling Login Packet {d}")
    clientSocket.name = d["username"]

    for key, player in list(handler.csm.players.items()):
        if player.name == clientSocket.name:
            print(f"{clientSocket.name} tried to connect but they are already on the server!")
            handler.csm.kickClient(player.name, code=1003, reason="Username already in use!")
            return


    p = {
        'username': d["username"],
        'password': d["password"],
        'color': d["color"],
        'session_id': clientSocket.session_id
    }
    handler.dsc.sendMsg("login", p)

