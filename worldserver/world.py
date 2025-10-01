'''
every world is going to have a 2d array of tile ids to store world data?

'''

class World:
    def __init__(self):
        self.worldData = bytes()
        self.width = 0
        self.height = 0
        self.worldString = ""

    def tick(self, handler):
        pass



    def printWorldData(self):
        print(f"{self.width} x {self.height} = {len(self.worldData)}")

        for y in range(self.height):
            for x in range(self.width):
                idx = y * self.width + x
                print(f"{self.worldData[idx]} ", end="")
            print("")




    def getWorldData(self):
        return self.worldData
    
    def setWorldString(self, string):
        #this function takes the string from the dataserver and stores it so we can send it to clients
        self.worldString = string
    def getWorldString(self): return self.worldString

    def setWorldData(self, byteData, width):
        self.worldData = byteData
        self.width = width
        self.height = len(byteData) // width   # using // is integer division

