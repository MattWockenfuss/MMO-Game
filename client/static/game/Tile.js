//alright so every tile is going to be instantiated from this tile class
export class Tile {
    static tileWidth = 64;  //all tiles have the same width
    static tilePixelWidth = 16;  //like in the actual files

    constructor(handler, codename, name, isSolid, loreBlurb, mapColor, animationSpeed = 60){
        this.codename = codename;
        this.handler = handler;
        this.name = name;  
        this.isSolid = isSolid;
        this.loreBlurb = loreBlurb;
        this.mapColor = mapColor;

        this.frames = Math.trunc(handler.AM.get(this.codename).naturalWidth / Tile.tilePixelWidth);
        if(this.frames > 1){
            //console.log(`Created a new Animated Tile(${this.codename}), it has ${this.frames} frames`);
            this.animationSpeed = animationSpeed;
            this.animationIndex = 0;
            this.animationI = 0;
        }else{
            //console.log(`Created a new Tile (${this.codename}), isSolid: ${this.isSolid} lore:${this.loreBlurb}`);
        }
    }
    tick(){
        this.animationI += 1;
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
            ctx.drawImage(this.handler.AM.get(this.codename), this.animationIndex * Tile.tilePixelWidth, 0, 16, 16, renderX, renderY, Tile.tileWidth, Tile.tileWidth);
        }else{
            ctx.drawImage(this.handler.AM.get(this.codename), renderX, renderY, Tile.tileWidth, Tile.tileWidth);
        }
    }
    renderDebug(ctx, renderX, renderY){
        ctx.fillStyle = "black";
        ctx.lineWidth = 2;
        ctx.strokeRect(renderX + 1, renderY + 1, Tile.tileWidth - 2, Tile.tileWidth - 2);
        if(this.frames > 1){
            ctx.font = "16px monospace";
            ctx.fillStyle = "black";
            ctx.fillText(`${this.animationIndex}`, renderX + 2, renderY + 16);
        }
    }
}