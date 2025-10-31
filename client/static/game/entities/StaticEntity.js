import { Entity } from "./Entity.js";

export class StaticEntity extends Entity{
    constructor(handler, entityData, entityDict){
        super(handler, entityData.x, entityData.y, entityDict.size[0], entityDict.size[1]);
        console.error(`ENTITY DATA: ${entityData}`);
        this.UUID = entityData.UUID;
        this.codename = entityData.type;
        this.level = entityData.level;
        this.health = entityData.health;

        

        console.log(`NEW Static@${this.type} at (${this.x}, ${this.y}), UUID: ${this.UUID}`);
    }
    
    tick(){
        this.renderX = this.x - this.handler.world.xOffset;
        this.renderY = this.y - this.handler.world.yOffset;
    }

    render(ctx){
        // ctx.fillStyle = "blue";
        // ctx.fillRect(this.renderX, this.renderY, this.width, this.height);
        ctx.drawImage(this.handler.AM.get(this.codename), this.renderX, this.renderY, this.width, this.height);

        ctx.fillStyle = "black";
        ctx.font = "bold 20px monospace";
        ctx.fillText(this.handler.world.staticsRegistry[this.codename].name, this.renderX, this.renderY - 5);
    }
}