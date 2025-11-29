import { Entity } from "./Entity.js";

export class OtherPlayer extends Entity{
    // in clientsocket.py on world server I also set the player width and height so i can test for collision with tile triggers!
    static PLAYER_WIDTH = 40;
    static PLAYER_HEIGHT = 40;
    
    constructor(handler, x, y, session_id, username, color){
        super(handler, x, y, OtherPlayer.PLAYER_WIDTH, OtherPlayer.PLAYER_HEIGHT);
        this.session_id = session_id;
        this.username = username;
        this.color = color;
        this.renderX = 0;
        this.renderY = 0;
    }

    tick(){
        this.renderX = this.x - this.handler.world.xOffset;
        this.renderY = this.y - this.handler.world.yOffset;
    }

    render(ctx){
        ctx.fillStyle = this.color;
        ctx.fillRect(this.renderX, this.renderY, this.width, this.height);

        ctx.fillStyle = "black";
        ctx.font = "bold 20px monospace";
        ctx.fillText(this.username, this.renderX, this.renderY - 5);
    }

    /*
        Desert Tile 2 if not 3 variations
        rivers

        Tiles:
            Sand Tile(3 variations)
            lighter water
        
        Structures
            Rivers with crops along the side
            Oasis
            Ruins of buildings
            Mountain, dug into side
            Quarry where you walk down to the bottom

        Static Entities:
            Cactus
            Flowers
            Crops by rivers




    */


}