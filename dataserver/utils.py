import base64
from PIL import Image

def loadMapImage(item, database): 
        #item is the dictionary for this world, this function reads the image file and loads data into world dict of their ids
        print(item)
        im = Image.open(f"configs/worlds/{item["Tile-Map"]}")
        print(im.format, im.size, im.mode)
        print(f"{im.width} x {im.height}")
        im = im.convert("RGB")

        #alright so we know the width and height of the world, now lets load it in, and store it in a byte array
        tiles = bytearray(im.width * im.height)
        
        for y in range(im.height):
            for x in range(im.width):
                idx = y * im.width + x
                point = (x, y)
                r, g, b = im.getpixel(point)

                for tile in database["tiles"]:
                    if f"#{r:02x}{g:02x}{b:02x}" == tile.get("map-color"):
                        tiles[idx] = tile.get("id")
                        break
                else:
                    tiles[idx] = 5 #the void tile, ehh

        world_data = bytes(tiles)
        
        item["world-data"] = base64.b64encode(world_data).decode("utf-8")   #add it to the database, probably change this later?
        item["world-width"] = im.width
        

        # for worlds in database["worlds"]:
        #     if worlds == item:
        #         print(f"We are in the {worlds.get("World-Name")} World")
        #         print(f"{worlds}")
                


        #alright so now out data is set
        #lets print it
        for y in range(im.height):
            for x in range(im.width):
                idx = y * im.width + x
                print(f"{world_data[idx]} ", end="")
            print("")


        #so we know the width and height of the server, how are we going to send the tile map
        # i also need to figure out how to send images to clients

        

        for y in range(im.height):
            for x in range(im.width):
                point = (x,y)
                r , g, b = im.getpixel(point)
                #print(f"#{r:02x}{g:02x}{b:02x}")   #python formatting, L is the format specifier, x means hexadecimal and 02 means pad with 0s to be atleast 2 wide  
