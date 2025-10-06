import { Entity } from "./Entity.js";
import { OtherPlayer } from "./OtherPlayer.js";

export class Player extends Entity{
    constructor(handler, myname, mycolor){
        super(handler, 200, 200, OtherPlayer.PLAYER_WIDTH, OtherPlayer.PLAYER_HEIGHT);
        this.renderX = 0;
        this.renderY = 0;
        this.speed = 5;
        this.toggleG = false;
        this.username = myname;
        this.color = mycolor;
    }

    tick(){
        var moved = false;
        if(this.handler.IM.down.has('KeyW')){
            this.y -= this.speed;
            moved = true;
        }
        if(this.handler.IM.down.has('KeyA')){
            this.x -= this.speed;
            moved = true;
        }
        if(this.handler.IM.down.has('KeyS')){
            this.y += this.speed;
            moved = true;
        }
        if(this.handler.IM.down.has('KeyD')){
            this.x += this.speed;
            moved = true;
        }
        const p = {
            'x': this.x,
            'y': this.y  
        }
        if(moved){
            this.handler.net.send("move", p);
        }


        if(this.handler.IM.down.has('KeyG')){
            this.toggleG = true;
            //console.log("G down!")
        }else if(this.toggleG){
            //console.log("{\"World-Type\":\"Forest\"}")
            // var name = prompt("Enter your name!");
            // this.name = name;
            // console.log(this.name)
            // this.handler.net.send("login", {"username": name});
            this.toggleG = false;
        }


        //instead of rendering at direct center, render at our x my xOffset
        this.renderX = this.x - this.handler.world.xOffset;
        this.renderY = this.y - this.handler.world.yOffset;
    }


    render(ctx){
        ctx.fillStyle = this.color;
        ctx.fillRect(this.renderX, this.renderY, this.width, this.height);

        if(this.username != null){
            ctx.fillStyle = "black";
            ctx.font = "bold 20px monospace";
            ctx.fillText(this.username, this.renderX, this.renderY - 5);
        }
    }

}