import { Tile } from "./Tile.js";

export class World{ 
    constructor(handler){
        this.handler = handler;
        this.worldName = null;
        this.worldData = null;
        this.worldWidth = null; // in tiles
        this.worldHeight = null; //in tiles
        this.worldPixelWidth = null;
        this.worldPixelHeight = null;

        this.nameID = "";

        this.CANVAS_WIDTH = 1500;
        this.CANVAS_HEIGHT = 640;

        //camera offsets
        this.xOffset = null;
        this.yOffset = null;

        this.tileMap = new Map();
        this.staticsRegistry = null;
    }
    tick(){
        //tile animations will go here?
        //also recalculate offsets based on player pos
        //console.log(`${this.handler.player.x}, ${this.handler.player.y}`);
        //we need to clamp the x and y offsets
        //so the x and y offsets are where we should start rendering the world so that our position is adjusted
        //we then clamp it so that when we get to the sides or corners, it doesnt let us see the background
        
        this.CANVAS_WIDTH = Math.floor(this.handler.GAME_WIDTH);
        this.CANVAS_HEIGHT = Math.floor(this.handler.GAME_HEIGHT);


        if(this.worldData != null){
            //console.log("TILE MAP WIDTH: " + this.tileMap.size);
            for(let i = 0; i < this.tileMap.size; i++){
                //console.log(`${this.tileMap.get(i).ID}`);
                this.tileMap.get(i).tick();
            }
        }


        const maxXOffset = this.worldPixelWidth - (this.CANVAS_WIDTH);
        const maxYOffset = this.worldPixelHeight - (this.CANVAS_HEIGHT);
        
        this.xOffset = Math.round(this.handler.player.x - (this.CANVAS_WIDTH / 2));
        this.yOffset = Math.round(this.handler.player.y - (this.CANVAS_HEIGHT / 2));

        this.xOffset = Math.max(0, Math.min(this.xOffset, maxXOffset));
        this.yOffset = Math.max(0, Math.min(this.yOffset, maxYOffset));
    }
    render(ctx){
        if(this.worldData != null){
            //alright, so we are looping through the world, and its laggy because its trying to render all of the tiles at once
            //lets define startx and startys in tiles
            //remember we have playerX and playerY, and the screensize is constant
            
            let startX = Math.max(0, Math.floor(this.xOffset / Tile.tileWidth) + 0);
            let startY = Math.max(0, Math.floor(this.yOffset / Tile.tileWidth) + 0);
            let endX = Math.min(Math.floor((this.xOffset + this.CANVAS_WIDTH) / Tile.tileWidth) + 1, this.worldWidth);
            let endY = Math.min(Math.floor((this.yOffset + this.CANVAS_HEIGHT) / Tile.tileWidth) + 1, this.worldHeight);

            //okay lets also cast our mouse coords to world coords, get the tile at that location, and highlight it
            //okay so xOffset + mouseX / Tile.tileWidth truncated?


            for(let row = startY; row < endY; row++){
                for(let x = startX; x < endX; x++){
                    
                    let renderX = (x * Tile.tileWidth) - this.xOffset;
                    let renderY = (row * Tile.tileWidth) - this.yOffset;
                    let id = this.worldData[(row * this.worldWidth) + x]
                    this.tileMap.get(id).render(ctx, renderX, renderY);
                }
            }

        }
        
    }
    setWorldData(data){
        //okay so we can set the world data in this function, everything about it
        let worlddata = data.world;
        let tilesdata = data.tiles;
        let tileRegistry = data.tileMap;
        this.staticsRegistry = data.statics;
        
        console.error(`STATICS LIST: ${JSON.stringify(this.staticsRegistry)}`);  //this is actually a list, convert to dictionary?
        

        var decoded = atob(worlddata["world-data"]);
        var bytes = new Int8Array(decoded.length);
        for(let i = 0; i < decoded.length; i++){
            bytes[i] = decoded.charCodeAt(i);
        }

        this.worldName = worlddata["World-Name"]
        this.worldData = bytes;
        this.worldWidth = worlddata["world-width"]
        this.worldHeight = Math.floor(this.worldData.length / this.worldWidth); //essentially turns into an integer
        this.worldPixelWidth = this.worldWidth * Tile.tileWidth;
        this.worldPixelHeight = this.worldHeight * Tile.tileWidth;


        console.log(tilesdata);
        
        for(const key in tilesdata){
            const tile = tilesdata[key];
            //console.log(`Tile ${key} = ${tile.name}, loreblurb ${tile["lore-blurb"]}`);
            
            console.log(tile);
            let codename =  tile['code-name'];
            let name =      tile['name'];
            let loreblurb = tile['lore-blurb'];
            let isSolid =   tile['is-Solid'];
            let mapColor =  tile['map-color'];
            let sprite =    tile['Sprite'];


            let id = tileRegistry[codename];

            this.tileMap.set(id, new Tile(this.handler, codename, name, isSolid, loreblurb, mapColor));
        }

        console.log(`Loaded World: ${this.worldName} ${this.worldWidth}x${this.worldHeight}`);
    }
    printWorldData(){
        //console.log("in the print function!")
        for(let row = 0; row < this.worldHeight; row++){
            //now we get and print the row
            let builderString = "";
            for(let x = 0; x < this.worldWidth; x++){
                builderString += this.worldData[(row * this.worldWidth) + x] + " ";
            }
            console.log(builderString);
        }
    }
    getTileAtAbsoluteCoords(x, y){
        /*
            This function takes in world coords x and y, maps those coordinates to
            a world tile, and returns whether or not that tile is solid, or has collision.
        */
        let tileX = Math.trunc(x / Tile.tileWidth);
        let tileY = Math.trunc(y / Tile.tileWidth);

        return this.tileMap.get(this.worldData[(tileY * this.worldWidth) + tileX]);
    }
    getTileAtWorldCoords(x, y){
        /*
            This function returns the tile found at world coords (x,y), note that these can
            only be integers where 0,0 is the top left of the world
        */
       if(x < 0 || x >= this.worldWidth) return null;
       if(y < 0 || y >= this.worldHeight) return null;
       return this.tileMap.get(this.worldData[y * this.worldWidth + x]);
    }
    getTileByID(id){
        return this.tileMap.get(id);
    }
}