"""
worldserver/WSCPacketHandler.py

Packet handler module for processing incoming client packets on the world server.

Responsibilities:
- Handle client packets related to player movement and login.
- Update server-side client state based on received packets.
- Broadcast relevant state changes (e.g., movement) to other connected clients.
- Validate client authentication before processing sensitive packets.
- Interact with the data server client (dsc) for login processing.
"""

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
    """
    Handle a player 'move' packet from a client.

    Updates the player's x and y position coordinates according to the packet data,
    and broadcasts this movement update to all other authenticated connected players.

    Args:
        handler (Handler): The main server handler containing subsystem references.
        d (dict): The parsed packet data containing 'x' and 'y' fields.
        clientSocket (ClientSocket): The client socket object representing the player connection.

    Behavior:
        - Verifies the client is authenticated.
        - Validates presence of x and y coordinates in the packet.
        - Updates the player's position on the server.
        - Sends movement update packets to all other connected players.
    """

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



def WSonLogin(handler, d, clientSocket):
    """
    Handle a client 'login' packet.

    Processes login requests containing username, password, and color.

    Validates that no other player on the server has the same username.
    If the username is already connected, kicks the new client connection.

    Sends a login message to the data server client (dsc) for authentication/processing.

    Args:
        handler (Handler): The main server handler containing subsystem references.
        d (dict): The parsed packet data containing 'username', 'password', and 'color'.
        clientSocket (ClientSocket): The client socket object representing the player connection.

    Packet example:
    p = {'username': 'Alex', 'password': '23423', 'color': '#e020ee'}
    """

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

