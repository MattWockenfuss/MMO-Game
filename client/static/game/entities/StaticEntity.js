import { Entity } from "./Entity.js";

export class StaticEntity extends Entity{
    constructor(handler, entityData){
        super(handler, entityData.x, entityData.y, 10, 6);
        
        this.UUID = entityData.UUID;
        this.type = entityData.type;
        this.level = entityData.level;
        this.health = entityData.health;
        console.log(`NEW Static@${this.type} at (${this.x}, ${this.y}), UUID: ${this.UUID}`);
    }
    
    tick(){
        this.renderX = this.x - this.handler.world.xOffset;
        this.renderY = this.y - this.handler.world.yOffset;
    }

    render(ctx){
        ctx.fillStyle = "blue";
        ctx.fillRect(this.renderX, this.renderY, this.width, this.height);

        ctx.fillStyle = "black";
        ctx.font = "bold 20px monospace";
        ctx.fillText(this.type, this.renderX, this.renderY - 5);
    }
}