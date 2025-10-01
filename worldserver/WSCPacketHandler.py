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
        if not clientSocket.is_authed:
            print(f"Move Packet from unauthenticated client, or player is null")
            return
        
        x = d.get("x")
        y = d.get("y")

        if x is None or y is None:
            print(f"Bad Movement Packet! (Missing x/y): {d}")
            return
        
        clientSocket.x = x
        clientSocket.y = y

        for sessID, otherPlayer in list(handler.csm.players.items()):
            if otherPlayer is clientSocket:
                continue
            da = {
                'session_id': clientSocket.session_id,
                'x': x,
                'y': y
            }
            otherPlayer.send('move', da)


    except Exception:
        import traceback
        traceback.print_exc()





'''
    This function handles the type 'login' packet from the clients. They tell us their username, password and color. 
    We do a quick check to see if someone is already on the server as this player, and if so, don't bother, this method will
    change in the future

    p = {'username': 'Alex', 'password': '23423', 'color': '#e020ee'}

'''
def WSonLogin(handler, d, clientSocket):
    #print(f"Handling Login Packet {d}")
    username = d.get("username")
    password = d.get("password")
    color = d.get("color")

    #print(f"{clientSocket.session_id}  {username} {password} {color}")

    for sessID, player in list(handler.csm.players.items()):
        if username == player.username:
            print(f"{username} tried to connect but they are already on the server!")
            handler.csm.kick(clientSocket.session_id, code=1000, reason="Username already in use!")
            return

    #attach the session id so we can associate it to this client when it comes back
    p = {
        'username': username,
        'password': password,
        'color': color,
        'session_id': clientSocket.session_id
    }
    handler.dsc.sendMsg("login", p)

