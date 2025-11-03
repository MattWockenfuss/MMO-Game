'''
    What packets does the world server send / recieve from comms server

    
    
    
    World Server -> Comms Server
        register
        switch

    Comms Server -> World Server
        registerReturn

'''


def registerRETURN(handler, d):
    print(f"FROM COMMS: {d}")