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

        this.CANVAS_WIDTH = 1500;
        this.CANVAS_HEIGHT = 640;

        //camera offsets
        this.xOffset = null;
        this.yOffset = null;

        this.tileMap = new Map();
    }
    tick(){
        //tile animations will go here?
        //also recalculate offsets based on player pos
        //console.log(`${this.handler.player.x}, ${this.handler.player.y}`);
        //we need to clamp the x and y offsets
        //so the x and y offsets are where we should start rendering the world so that our position is adjusted
        //we then clamp it so that when we get to the sides or corners, it doesnt let us see the background

        if(this.worldData != null){
            //console.log("TILE MAP WIDTH: " + this.tileMap.size);
            for(let i = 1; i < this.tileMap.size + 1; i++){
                //console.log(`${this.tileMap.get(i).ID}`);
                this.tileMap.get(i).tick();
            }
        }


        const maxXOffset = this.worldPixelWidth - (this.CANVAS_WIDTH);
        const maxYOffset = this.worldPixelHeight - (this.CANVAS_HEIGHT);
        
        this.xOffset = this.handler.player.x - (this.CANVAS_WIDTH / 2);
        this.yOffset = this.handler.player.y - (this.CANVAS_HEIGHT / 2);

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

            for(let row = startY; row < endY; row++){
                for(let x = startX; x < endX; x++){
                    let renderX = (x * Tile.tileWidth) - this.xOffset;
                    let renderY = (row * Tile.tileWidth) - this.yOffset
                    //what ever the id is, render that tile
                    
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

        for(const key of Object.keys(data)){
            console.log(`${key} : ${data[key]}`)
        }
        
        

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


        console.log(tilesdata)
        for(let tile of tilesdata){
            this.tileMap.set(tile.id, new Tile(this.handler, tile.id, tile.name, tile["is-Solid"], tile["lore-blurb"]))
        }

        // this.tileMap.set(1, new Tile(this.handler, 1, "grass", false));
        // this.tileMap.set(2, new Tile(this.handler, 2, "sand", false));
        // this.tileMap.set(3, new Tile(this.handler, 3, "stone-floor", false));
        // this.tileMap.set(4, new Tile(this.handler, 4, "stone-wall", false));
        // this.tileMap.set(5, new Tile(this.handler, 5, "void", false));
        // this.tileMap.set(6, new Tile(this.handler, 9, "water", false, 20));
        // this.tileMap.set(7, new Tile(this.handler, 7, "wood-floor", false));
        // this.tileMap.set(8, new Tile(this.handler, 8, "wood-wall", false));


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
}