//alright so every tile is going to be instantiated from this tile class
export class Tile {
    static tileWidth = 64;  //all tiles have the same width
    static tilePixelWidth = 16;  //like in the actual files

    constructor(handler, ID, name, isSolid, loreBlurb, animationSpeed = 60){
        //what does every tile type have?
        this.ID = ID; //how you access the sprite for this tile
        this.handler = handler;
        this.name = name;  
        this.isSolid = isSolid;
        this.loreBlurb = loreBlurb
        //i need to be able to dynamically tell what kind of tile something is, like is it animated or not?
        //maybe we create the tiles in the assets?
        //if its animated, pass an object, detailing the animation speed in ticksPerFrame
        //so like 60 would take 1 second per frame about
        //see the thing is how do i know how many frames there are in the animation without the image? 
        //I dont, and i dont have the image here I dont believe, well maybe i do, 
        //this is called on receive of the world data
        //so i could defintitely get the image width here
        //should I? idk

        this.frames = Math.trunc(handler.AM.get(this.ID).naturalWidth / Tile.tilePixelWidth);
        if(this.frames > 1){
            console.log(`Created a new Animated Tile#${this.ID}, it has ${this.frames} frame(s)`);
            this.animationSpeed = animationSpeed;
            this.animationIndex = 0;
            this.animationI = 0;
        }else{
            console.log(`Created a new Tile#${this.ID}, isSolid: ${this.isSolid} lore:${this.loreBlurb}`);
        }
        



    }
    tick(){
        this.animationI += 1;
        //console.log(this.animationI);
        if(this.animationI >= this.animationSpeed){
            this.animationI = 0;
            this.animationIndex += 1;
            if(this.animationIndex >= this.frames){
                this.animationIndex = 0;
            }
        }
    }
    render(ctx, renderX, renderY){

        /*
            the water is going to get desynced then from clients, thats fine
            alright, so render the image of the appropriate ID
            the object instantiated from this client, represents all of those tiles, as such we pass through the renderX and renderY
            const image = this.handler.AM.get(this.ID);
            console.log(image, renderX, renderY); 
            okay so we are loading the right image in, we want to animate, how do we do so?
        

            okay so if we are animating a tile, we have x number of images in the rotation, we dont know how many
            we know the width of the total image
            and we know that each one is 64

            okay so we can figure out how many frames it has in the constructor no problems,
            then we can pass in a speed, 

            https://codehs.com/tutorial/andy/Programming_Sprites_in_JavaScript
            very helpful tutorial
        */
        
        
        if(this.frames > 1){
            ctx.drawImage(this.handler.AM.get(this.ID), this.animationIndex * Tile.tilePixelWidth, 0, 16, 16, renderX, renderY, Tile.tileWidth, Tile.tileWidth);

            //ctx.font = "16px monospace";
            //ctx.fillStyle = "black";
            //ctx.fillText(`${this.animationIndex}`, renderX + 2, renderY + 16);
        }else{
            ctx.drawImage(this.handler.AM.get(this.ID), renderX, renderY, Tile.tileWidth, Tile.tileWidth);
        }
    }
    renderDebug(ctx, renderX, renderY){
        ctx.fillStyle = "Red";
        ctx.fillRect(renderX, renderY, Tile.tileWidth, Tile.tileWidth);
    }
}