export class Player {
    constructor(handler, myname, mycolor){
        this.handler = handler;
        this.x = 200;
        this.y = 200;
        this.speed = 5;
        this.toggleG = false;
        this.name = myname;
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
    }


    render(ctx){
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, 40, 40);

        if(this.name != null){
            ctx.fillStyle = "black";
            ctx.font = "bold 20px monospace";
            ctx.fillText(this.name, this.x, this.y - 5);
        }
    }

}