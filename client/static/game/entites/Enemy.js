import { Entity } from "./Entity.js";


export class Enemy extends Entity{
    constructor(handler, enemyData){             //enemyData is literally just an 'object' in JS
        super(handler, enemyData.x, enemyData.y, 40, 40)
        
        
        console.log(enemyData);
        this.UUID = enemyData.UUID;
        this.type = enemyData.type;
        this.level = enemyData.level;
        this.health = enemyData.health;
        this.attack = enemyData.attack;
        this.attackSpeed = enemyData.attackSpeed;
        this.dodgeChance = enemyData.dodgeChance;
        this.criticalChance = enemyData.criticalChance;
        this.movementSpeed = enemyData.movementSpeed;
        this.visionRadius = enemyData.visionRadius;
        this.size = enemyData.size;
        this.width *= this.size;
        this.height *= this.size;
        this.movementType = enemyData.movementType;
    }

    tick(){
        this.renderX = this.x - this.handler.world.xOffset;
        this.renderY = this.y - this.handler.world.yOffset;
    }
    render(ctx){
        ctx.fillStyle = "red";
        ctx.fillRect(this.renderX, this.renderY, this.width, this.height);

        ctx.fillStyle = "black";
        ctx.font = "bold 20px monospace";
        ctx.fillText(this.type, this.renderX, this.renderY - 5);
    }


}