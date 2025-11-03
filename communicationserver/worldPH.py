



def register(handler, d, worldclient):
    #alright in this function, we need to figure out what kind of world it needs to be, and send it back
    print(f"REGISTER: {d}")
    p = {
        'msg': "this is the msg back!"
    }
    worldclient.send('registerRETURN', p)

def switch(handler, d , worldclient):
    print(f"SWITCH: {d}")