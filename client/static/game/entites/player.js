import { Entity } from "./Entity.js";
import { OtherPlayer } from "./OtherPlayer.js";

export class Player extends Entity{
    constructor(handler, myname, mycolor){
        super(handler, 1000, 1000, OtherPlayer.PLAYER_WIDTH, OtherPlayer.PLAYER_HEIGHT);
        this.renderX = 0;
        this.renderY = 0;
        this.speed = 5;
        this.toggleG = false;
        this.username = myname;
        this.color = mycolor;
        this.xMove = 0;
        this.yMove = 0;
    }

    tick(){
        
        var moved = false;
        if(this.handler.IM.down.has('KeyW')){
            this.yMove -= this.speed;
            moved = true;
        }
        if(this.handler.IM.down.has('KeyA')){
            this.xMove -= this.speed;
            moved = true;
        }
        if(this.handler.IM.down.has('KeyS')){
            this.yMove += this.speed;
            moved = true;
        }
        if(this.handler.IM.down.has('KeyD')){
            this.xMove += this.speed;
            moved = true;
        }

        //alright, so we have these xMove and yMove variables that represent how much we want to move on that axis
        //now what?
        //normalize client movement?
        //if i somehow hold A and D and W at the same time, xMove will cancel out, and yMove will be positive
        
        //if both are non zero, than normalize?
        if(this.xMove != 0 && this.yMove != 0){
            //then multiply both by cos(45) and keep the signs? 
            //that should work perfectly fine
            let cos45 = 0.7071067812;
            this.xMove = this.xMove * cos45;
            this.yMove = this.yMove * cos45;
        }
        
        //okay so now speed is normalized right?
        //now we want to do handling of collisions
        //well
        //this.x += this.xMove;
        //this.y += this.yMove;

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
        this.handleCollisions(ctx, this.xMove, this.yMove);
        this.xMove = 0;
        this.yMove = 0;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.renderX, this.renderY, this.width, this.height);

        if(this.username != null){
            ctx.fillStyle = "black";
            ctx.font = "bold 20px monospace";
            ctx.fillText(this.username, this.renderX, this.renderY - 5);
        }
    }
}