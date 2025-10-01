import { Entity } from "./Entity.js";

export class OtherPlayer extends Entity{
    constructor(x, y, session_id, username, color){
        super();
        this.x = x;
        this.y = y;
        this.session_id = session_id;
        this.username = username;
        this.color = color;
    }
    tick(){

    }
    render(ctx){
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, 40, 40);

        ctx.fillStyle = "black";
        ctx.font = "bold 20px monospace";
        ctx.fillText(this.username, this.x, this.y - 5);
        

    }

}