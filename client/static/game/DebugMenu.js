/*
    What are this objects reponsibilities?
    well it renders our debug screen? toggle with F4 or something?
    
    - draws the debug info from, like mouseX and mouseY, xOffset, etc... game loop
    - draws the onHover for tiles, like their outline, animation frame, etc...
    - draws the WAILIA thing for both tiles, and entities and presumably other things in the future

*/

import { OtherPlayer } from "./entites/OtherPlayer.js";
import { Player } from "./entites/player.js";
import { Tile } from "./Tile.js";


export class DebugMenu {
    constructor(handler){
        this.handler = handler;
    }

    tick(){

    }
    render(ctx, ticks){
        ctx.fillStyle = "black";
        ctx.font = " 20px monospace";


        let gap = 20;
        ctx.fillStyle = 'rgba(255, 255, 255, 0.55)';
        ctx.fillRect(0, 0, 220, (11 * gap) + 8);

        ctx.fillStyle = "black";
        //ctx.fillText("Ticks: " + this.ticks, 8, 8 + (1 * gap));
        ctx.fillText("Ticks: " + ticks, 8, 8 + (2 * gap));
        //ctx.fillText("st: " + (this.st).toFixed(1), 8, 8 + (3 * gap));
        
        if(this.handler.player !== null && this.handler.player !== undefined){
            ctx.fillText("x: " + (this.handler.player.x).toFixed(1), 8, 8 + (5 * gap));
            ctx.fillText("y: " + (this.handler.player.y).toFixed(1), 8, 8 + (6 * gap));
        }
        if(this.handler.world !== null && this.handler.world !== undefined){
            if(this.handler.world.xOffset !== null && this.handler.world.yOffset !== undefined){
                ctx.fillText("xOffset: " + (this.handler.world.xOffset).toFixed(1), 8, 8 + (7 * gap));
                ctx.fillText("yOffset: " + (this.handler.world.yOffset).toFixed(1), 8, 8 + (8 * gap));
            }
        }

        ctx.fillText("mouseX: " + (this.handler.IM.mouseX).toFixed(1), 8, 8 + (9 * gap));
        ctx.fillText("mouseY: " + (this.handler.IM.mouseY).toFixed(1), 8, 8 + (10 * gap));

        

        // if(Tile.tileWidth != null){
        //     let tileX = Math.trunc((this.handler.world.xOffset + this.handler.IM.mouseX) / Tile.tileWidth);
        //     let tileY = Math.trunc((this.handler.world.yOffset + this.handler.IM.mouseY) / Tile.tileWidth);

        //     ctx.fillText(`${tileX}, ${tileY}`, this.handler.IM.mouseX, this.handler.IM.mouseY);
        // }

        // if(this.handler.IM.down.has("leftMouseBTN")){
        //     console.log("canvas.width:", this.canvas.width, "canvas.height:", this.canvas.height);
        //     console.log("canvas.style.width:", this.canvas.style.width, "canvas.style.height:", this.canvas.style.height);
        //     console.log("devicePixelRatio:", window.devicePixelRatio);
        // }

        //ctx.fillStyle = "yellow";
        //ctx.fillRect(this.handler.IM.mouseX, this.handler.IM.mouseY, 2, 2);
        

        let mouseX = this.handler.world.xOffset + this.handler.IM.mouseX;
        let mouseY = this.handler.world.yOffset + this.handler.IM.mouseY;
        
        //alright, so we are hovering over a tile, lets render some tile data
        ctx.fillStyle = "#E6E6FA";
        let CANVAS_WIDTH = 1500;
        let CANVAS_HEIGHT = 640;
        let width = 300;
        let height = 120;
        ctx.fillRect(CANVAS_WIDTH - width, 0, width, height);
        ctx.lineWidth = 2;
        ctx.fillStyle = "black";
        ctx.strokeRect(CANVAS_WIDTH - width + 1, 0 + 1, width - 2, height - 2);
        //alright, draw the properties of this tile



        //alright now we want to check for entities, first loop through all of them, check for hover
        for(const entity of this.handler.EM.entities){
            //console.log(`${entity.x} < ${mouseX} < ${entity.x + entity.width}`);
            if(entity.x < mouseX && mouseX < (entity.x + entity.width)){
                if(entity.y < mouseY && mouseY < (entity.y + entity.height)){
                    entity.renderDebug(ctx);

                    ctx.font = "16px monospace";
                    ctx.fillStyle = "black";
                    //alright now render entity properties
                    ctx.fillText(`EntityType: ${entity.constructor.name}`, CANVAS_WIDTH - width + 4, 18 + (gap * 0));
                    ctx.fillText(`(x,y): (${entity.x},${entity.y})`, CANVAS_WIDTH - width + 4, 18 + (gap * 1));
                    if(entity instanceof OtherPlayer || entity instanceof Player){
                        ctx.fillText(`Name: ${entity.username}`, CANVAS_WIDTH - width + 4, 18 + (gap * 2));
                        ctx.fillText(`Color: ${entity.color}`, CANVAS_WIDTH - width + 4, 18 + (gap * 3));
                        if(entity instanceof OtherPlayer){
                            ctx.fillText(`SessID: ${entity.session_id}`, CANVAS_WIDTH - width + 4, 18 + (gap * 4));
                        }
                    }
                    return;
                }
            }
        
        }

        if(this.handler.world.worldData != null){
            //alright now lets move the render world wailia to here
            let tileX = Math.trunc(mouseX / Tile.tileWidth);
            let tileY = Math.trunc(mouseY / Tile.tileWidth);
            //console.log(`Checking ${tileX}, ${tileY}`);

            let id = this.handler.world.worldData[tileY * this.handler.world.worldWidth + tileX];
            let tile = this.handler.world.tileMap.get(id);

            let renderX = (tileX * Tile.tileWidth) - this.handler.world.xOffset;
            let renderY = (tileY * Tile.tileWidth) - this.handler.world.yOffset;
            tile.renderDebug(ctx, renderX, renderY);

            ctx.font = "16px monospace";
            ctx.fillStyle = "black";

            ctx.fillText(`name: ${tile.name}`, CANVAS_WIDTH - width + 4, 18 + (gap * 0));
            ctx.fillText(`(x,y): (${tileX},${tileY})`, CANVAS_WIDTH - width + 4, 18 + (gap * 1));
            ctx.fillText(`ID: ${tile.ID}`, CANVAS_WIDTH - width + 4, 18 + (gap * 2));
            ctx.fillText(`isSolid: ${tile.isSolid}`, CANVAS_WIDTH - width + 4, 18 + (gap * 3));
            ctx.fillText(`loreBlurb: ${tile.loreBlurb}`, CANVAS_WIDTH - width + 4, 18 + (gap * 4));
        }

    }
}
