import { Entity } from "./Entity.js";

export class OtherPlayer extends Entity{
    static PLAYER_WIDTH = 40;
    static PLAYER_HEIGHT = 96;
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

}