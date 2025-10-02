import { Entity } from "./Entity.js";

export class OtherPlayer extends Entity{
    constructor(handler, x, y, session_id, username, color){
        super(handler);
        this.x = x;
        this.y = y;
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
        ctx.fillRect(this.renderX - 20, this.renderY - 20, 40, 40);

        ctx.fillStyle = "black";
        ctx.font = "bold 20px monospace";
        ctx.fillText(this.username, this.renderX - 20, this.renderY - 20 - 5);
        

    }

}