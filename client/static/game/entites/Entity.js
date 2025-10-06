export class Entity {
    constructor(handler, x, y, width, height){
        /*
            All entities have an x, y, width and height
            For rendering and polling purposes, all entities have their x and y starting at the top left of themselves,
            NOT their center
        
        
        */
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
        ctx.fillRect(this.renderX, this.renderY, this.width, this.height);
    }
}