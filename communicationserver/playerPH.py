


def AUTH_REQ(handler, d, playerclient):
    print(f"AUTH_REQ: {d}")

    # so some is trying to authenticate, they sent us their username and password
    playerclient.username = d.get("username")
    playerclient.password = d.get("password")

    #alright so we set this clients username and password, now we send to the dataserver for check
    dx = {
        "username": playerclient.username,
        "password": playerclient.password,
        "UUID": playerclient.UUID
    }
    handler.dsc.sendMsg("AUTH_REQ", dx)



