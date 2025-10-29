/*
    What are this objects reponsibilities?
    well it renders our debug screen? toggle with F4 or something?
    
    - draws the debug info from, like mouseX and mouseY, xOffset, etc... game loop
    - draws the onHover for tiles, like their outline, animation frame, etc...
    - draws the WAILIA thing for both tiles, and entities and presumably other things in the future

*/

import { Enemy } from "./entities/Enemy.js";
import { OtherPlayer } from "./entities/OtherPlayer.js";
import { Player } from "./entities/player.js";
import { Tile } from "./Tile.js";


export class DebugMenu {
    constructor(handler){
        this.handler = handler;
    }

    tick(){

    }
    render(ctx, ticks){
        if(!this.handler.CM.controls.get('TOGGLEDEBUG').toggled()) return;

        let CANVAS_WIDTH = this.handler.GAME_WIDTH;  //probably should fix this, soon TM
        let CANVAS_HEIGHT = this.handler.GAME_HEIGHT;
        //console.log(`${CANVAS_WIDTH} x ${CANVAS_HEIGHT}`);

        if(this.handler.world == null) return;
        if(this.handler.world.xOffset == null) return;
        if(this.handler.player == null) return;



        let mouseX = this.handler.world.xOffset + this.handler.IM.mouseX;
        let mouseY = this.handler.world.yOffset + this.handler.IM.mouseY;
        
        ctx.fillStyle = "black";
        ctx.font = " 20px monospace";
        
        /*
                I dont love this implementation, lots of copy/paste, but it currently works
                come back later
        
        */

        let gap = 21;
        ctx.fillStyle = 'rgba(255, 255, 223, 0.55)';
        ctx.fillRect(0, 0, 220, (11 * gap) + 8);

        ctx.fillStyle = "black";
        ctx.fillText("Ticks: " + ticks, 8, 8 + (2 * gap));

        ctx.fillText(`Player: (${(this.handler.player.x).toFixed(1)},${(this.handler.player.y).toFixed(1)})`,                   8, 8 + (5 * gap));
        ctx.fillText(`Offset: (${(this.handler.world.xOffset).toFixed(1)},${(this.handler.world.yOffset).toFixed(1)})`,         8, 8 + (6 * gap));
        ctx.fillText(`Mouse: (${(this.handler.IM.mouseX).toFixed(1)},${(this.handler.IM.mouseY).toFixed(1)})`,                  8, 8 + (7 * gap));
        ctx.fillText(`MseAdj: (${(mouseX).toFixed(1)},${(mouseY).toFixed(1)})`,                                                 8, 8 + (8 * gap));
        
        let tileX = Math.trunc((this.handler.world.xOffset + this.handler.IM.mouseX) / Tile.tileWidth);
        let tileY = Math.trunc((this.handler.world.yOffset + this.handler.IM.mouseY) / Tile.tileWidth);


        ctx.fillText(`Mouse (Tile): (${tileX},${tileY})`,                                                                      8, 8 + (9 * gap));
        



        for(const entity of this.handler.EM.entities){
            //console.log(`${entity.x} < ${mouseX} < ${entity.x + entity.width}`);
            if(entity.x < mouseX && mouseX < (entity.x + entity.width)){
                if(entity.y < mouseY && mouseY < (entity.y + entity.height)){
                    entity.renderDebug(ctx);
                    ctx.fillStyle = "black";
                    ctx.font = " 20px monospace";
                    


                    if(entity instanceof OtherPlayer || entity instanceof Player){
                        //We want to make the box larger depending on the entity type
                        let width = 300;
                        let height = gap * 6;
                        ctx.fillStyle = 'rgba(255, 255, 223, 0.55)';
                        ctx.fillRect(CANVAS_WIDTH - width, 0, width, height);
                        ctx.lineWidth = 2;
                        ctx.fillStyle = "black";
                        ctx.strokeRect(CANVAS_WIDTH - width + 1, 0 + 1, width - 2, height - 2);

                        ctx.fillText(`EntityType: ${entity.constructor.name}`,                  CANVAS_WIDTH - width + 4, 18 + (gap * 0));
                        ctx.fillText(`(x,y): (${entity.x.toFixed(1)},${entity.y.toFixed(1)})`,  CANVAS_WIDTH - width + 4, 18 + (gap * 1));
                        ctx.fillText(`w x h: ${entity.width} x ${entity.height}`,               CANVAS_WIDTH - width + 4, 18 + (gap * 2));
                        ctx.fillText(`Name: ${entity.username}`,                                CANVAS_WIDTH - width + 4, 18 + (gap * 3));
                        ctx.fillText(`Color: ${entity.color}`,                                  CANVAS_WIDTH - width + 4, 18 + (gap * 4));
                        if(entity instanceof OtherPlayer){
                            ctx.fillText(`SessID: ${entity.session_id}`,                        CANVAS_WIDTH - width + 4, 18 + (gap * 5));
                        }
                    }else if(entity instanceof Enemy){
                        let width = 300;
                        let height = gap * 18 + 10;
                        ctx.fillStyle = 'rgba(255, 255, 223, 0.55)';
                        ctx.fillRect(CANVAS_WIDTH - width, 0, width, height);
                        ctx.lineWidth = 2;
                        ctx.fillStyle = "black";
                        ctx.strokeRect(CANVAS_WIDTH - width + 1, 0 + 1, width - 2, height - 2);

                        ctx.fillText(`EntityType: ${entity.constructor.name}`,                  CANVAS_WIDTH - width + 4, 18 + (gap * 0));
                        ctx.fillText(`(x,y): (${entity.x.toFixed(1)},${entity.y.toFixed(1)})`,  CANVAS_WIDTH - width + 4, 18 + (gap * 1));
                        ctx.fillText(`w x h: ${entity.width} x ${entity.height}`,               CANVAS_WIDTH - width + 4, 18 + (gap * 2));
                        ctx.fillText(`UUID ${entity.UUID}`,                                     CANVAS_WIDTH - width + 4, 18 + (gap * 6));
                        ctx.fillText(`Type: ${entity.type}`,                                    CANVAS_WIDTH - width + 4, 18 + (gap * 7));
                        ctx.fillText(`Level: ${entity.level}`,                                  CANVAS_WIDTH - width + 4, 18 + (gap * 8));
                        ctx.fillText(`Health: ${entity.health}`,                                CANVAS_WIDTH - width + 4, 18 + (gap * 9));
                        ctx.fillText(`AttackDMG: ${entity.attack}`,                             CANVAS_WIDTH - width + 4, 18 + (gap * 10));
                        ctx.fillText(`AttackSPD: ${entity.attackSpeed}`,                        CANVAS_WIDTH - width + 4, 18 + (gap * 11));
                        ctx.fillText(`dodge: ${entity.dodgeChance}`,                            CANVAS_WIDTH - width + 4, 18 + (gap * 12));
                        ctx.fillText(`critical: ${entity.criticalChance}`,                      CANVAS_WIDTH - width + 4, 18 + (gap * 13));
                        ctx.fillText(`movementSPD: ${entity.movementSpeed}`,                    CANVAS_WIDTH - width + 4, 18 + (gap * 14));
                        ctx.fillText(`VisionRadius: ${entity.visionRadius}`,                    CANVAS_WIDTH - width + 4, 18 + (gap * 15));
                        ctx.fillText(`Size: ${entity.size}`,                    CANVAS_WIDTH - width + 4, 18 + (gap * 16));
                        ctx.fillText(`movementType: ${entity.movementType}`,                    CANVAS_WIDTH - width + 4, 18 + (gap * 17));
                    }
                    return; //we return so we dont do the tile below this
                }
            }
        
        }

        if(this.handler.world.worldData != null){
            let width = 300;
            let height = gap * 5 + 10;
            ctx.fillStyle = 'rgba(255, 255, 223, 0.55)';
            ctx.fillRect(CANVAS_WIDTH - width, 0, width, height);
            ctx.lineWidth = 2;
            ctx.fillStyle = "black";
            ctx.strokeRect(CANVAS_WIDTH - width + 1, 0 + 1, width - 2, height - 2);


            let tileX = Math.trunc(mouseX / Tile.tileWidth);
            let tileY = Math.trunc(mouseY / Tile.tileWidth);
            //console.log(`Checking ${tileX}, ${tileY}`);

            let id = this.handler.world.worldData[tileY * this.handler.world.worldWidth + tileX];
            let tile = this.handler.world.tileMap.get(id);

            let renderX = (tileX * Tile.tileWidth) - this.handler.world.xOffset;
            let renderY = (tileY * Tile.tileWidth) - this.handler.world.yOffset;
            tile.renderDebug(ctx, renderX, renderY);

            ctx.fillStyle = "black";
            ctx.font = " 20px monospace";

            // let isSolidT = this.handler.world.isTileSolid(mouseX, mouseY);
            // ctx.fillText(`${isSolidT}`, mouseX, mouseY);

            ctx.fillText(`name: ${tile.name}`, CANVAS_WIDTH - width + 4, 18 + (gap * 0));
            ctx.fillText(`(x,y): (${tileX},${tileY})`, CANVAS_WIDTH - width + 4, 18 + (gap * 1));
            ctx.fillText(`ID: ${tile.ID}`, CANVAS_WIDTH - width + 4, 18 + (gap * 2));
            ctx.fillText(`isSolid: ${tile.isSolid}`, CANVAS_WIDTH - width + 4, 18 + (gap * 3));
            ctx.fillText(`loreBlurb: ${tile.loreBlurb}`, CANVAS_WIDTH - width + 4, 18 + (gap * 4));
        }

    }
}
