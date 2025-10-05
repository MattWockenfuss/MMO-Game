export class Entity {
    constructor(handler, x, y, width, height){
        this.handler = handler;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        console.log("New Entity created!");
    }

    tick(){};
    render(ctx){}

    renderDebug(ctx){
        ctx.fillStyle = "blue";
        ctx.fillRect(this.renderX - (this.width / 2), this.renderY - (this.height / 2), this.width, this.height);
    }
}