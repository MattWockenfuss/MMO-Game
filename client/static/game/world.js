export class World{ 
    constructor(handler){
        this.handler = handler;
        this.worldName = null;
        this.worldData = null;
        this.worldWidth = null; // in tiles
        this.worldHeight = null; //in tiles
        this.worldPixelWidth = null;
        this.worldPixelHeight = null;
        
        this.size = 64;

        this.CANVAS_WIDTH = 1500;
        this.CANVAS_HEIGHT = 640;

        //camera offsets
        this.xOffset = null;
        this.yOffset = null;
    }
    tick(){
        //tile animations will go here?
        //also recalculate offsets based on player pos
        //console.log(`${this.handler.player.x}, ${this.handler.player.y}`);
        //we need to clamp the x and y offsets
        //so the x and y offsets are where we should start rendering the world so that our position is adjusted
        //we then clamp it so that when we get to the sides or corners, it doesnt let us see the background

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
            
            let startX = Math.max(0, Math.floor(this.xOffset / this.size) + 0);
            let startY = Math.max(0, Math.floor(this.yOffset / this.size) + 0);
            let endX = Math.min(Math.floor((this.xOffset + this.CANVAS_WIDTH) / this.size) + 1, this.worldWidth);
            let endY = Math.min(Math.floor((this.yOffset + this.CANVAS_HEIGHT) / this.size) + 1, this.worldHeight);

            for(let row = startY; row < endY; row++){
                for(let x = startX; x < endX; x++){

                    
                    let id = this.worldData[(row * this.worldWidth) + x]
                    if (this.handler.AM.get(this.worldData[(row * this.worldWidth) + x])){
                        let renderX = (x * this.size) - this.xOffset;
                        let renderY = (row * this.size) - this.yOffset
                        //console.log(`${x},${row} => ${startX},${startY}`);
                        ctx.drawImage(this.handler.AM.get(id), renderX, renderY, this.size, this.size)
                    } 
                    
                }
            }
        }


    }
    setWorldData(data){
        //okay so we can set the world data in this function, everything about it
        for(const key of Object.keys(data)){
            console.log(`${key} : ${data[key]}`)
        }
        //AQIDBAUGBwgICAECAgICAgICBwcBAQEBAQQEBAcHAQEBBgYGBgQDAwEBAQYGBgYEAwM= is the world data right now
        console.log("Trying to decode world data!")
        //okay
        var decoded = atob(data["world-data"]);
        this.worldName = data["World-Name"]
        console.log(decoded);
        var bytes = new Int8Array(decoded.length);
        for(let i = 0; i < decoded.length; i++){
            //console.log(decoded.charCodeAt(i));
            bytes[i] = decoded.charCodeAt(i);
        }
        //console.log("setting class vars")
        this.worldData = bytes;
        this.worldWidth = data["world-width"]
        this.worldHeight = Math.floor(this.worldData.length / this.worldWidth); //essentially turns into an integer
        this.worldPixelWidth = this.worldWidth * this.size;
        this.worldPixelHeight = this.worldHeight * this.size;
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