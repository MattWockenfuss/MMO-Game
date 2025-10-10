import { Tile } from "../Tile.js";

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

    handleCollisions(ctx, xMove, yMove){
        let renderDebug = false;
        let tw = Tile.tileWidth;
        //This is substracted from our width and height when searching for rectangles so they we dont check below us
        //when trying to move right, it was causing snapping glitches to tiles, set it to 0 and try it!
        const EPS = 1e-6;

        /*
            This function takes 
        */

        if(xMove > 0){
            const top = this.y;
            const bottom = this.y + this.height - EPS;
            const startX = this.x + this.width + xMove;

            let tx = Math.trunc(startX / tw);
            let tyS = Math.trunc(top / tw);
            let tyE = Math.trunc(bottom / tw);

            let earliestWall = xMove;

            for(let ty = tyS; ty <= tyE; ty++){
                console.log(`Collision Cycle: ${tyS}->${ty}->${tyE}`);
                //get the tile at these coords
                let t = this.handler.world.getTileAtWorldCoords(tx, ty);
                if(!t) return;
                
                if(renderDebug){
                    let renderX = tx * tw - this.handler.world.xOffset;
                    let renderY = ty * tw - this.handler.world.yOffset;
                    ctx.fillStyle = "red";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(renderX, renderY, tw, tw);
                    ctx.fillStyle = 'Black';
                    ctx.fillText(t.isSolid + "", renderX + 4, renderY + 10);
                }

                if(t.isSolid){
                    let dx = (tx * tw) - (this.x + this.width);
                    if(dx < earliestWall) earliestWall = dx;
                }
            }

            this.x += earliestWall;

        }else if(xMove < 0){
            const top = this.y;
            const bottom = this.y + this.height - EPS;
            const startX = this.x + xMove;

            let tx = Math.trunc(startX / tw);
            let tyS = Math.trunc(top / tw);
            let tyE = Math.trunc(bottom / tw);

            let earliestWall = xMove;//this is negative

            for(let ty = tyS; ty <= tyE; ty++){
                console.log(`Collision Cycle: ${tyS}->${ty}->${tyE}`);
                //get the tile at these coords
                let t = this.handler.world.getTileAtWorldCoords(tx, ty);
                if(!t) return;
                
                if(renderDebug){
                    let renderX = tx * tw - this.handler.world.xOffset;
                    let renderY = ty * tw - this.handler.world.yOffset;
                    ctx.fillStyle = "red";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(renderX, renderY, tw, tw);
                    ctx.fillStyle = 'Black';
                    ctx.fillText(t.isSolid + "", renderX + 4, renderY + 10);
                }

                if(t.isSolid){
                    //(tx + 1) * tw = the tiles RIGHT edge
                    let dx = ((tx + 1) * tw) - this.x;
                    if(dx > earliestWall) earliestWall = dx;
                }
            }

            this.x += earliestWall;
        }

        if(yMove > 0){
            //moving down
            const left = this.x;
            const right = this.x + this.width - EPS;
            const startY = this.y + this.height + yMove;

            let ty = Math.trunc(startY / tw);
            let txS = Math.trunc(left / tw);
            let txE = Math.trunc(right / tw);

            let earliestWall = yMove;

            for(let tx = txS; tx <= txE; tx++){
                console.log(`Collision Cycle: ${txS}->${tx}->${txE}`);
                //get the tile at these coords
                let t = this.handler.world.getTileAtWorldCoords(tx, ty);
                if(!t) return;
                
                if(renderDebug){
                    let renderX = tx * tw - this.handler.world.xOffset;
                    let renderY = ty * tw - this.handler.world.yOffset;
                    ctx.fillStyle = "red";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(renderX, renderY, tw, tw);
                    ctx.fillStyle = 'Black';
                    ctx.fillText(t.isSolid + "", renderX + 4, renderY + 10);
                }

                if(t.isSolid){
                    let dy = (ty * tw) - (this.y + this.height);
                    if(dy < earliestWall) earliestWall = dy;
                }
            }

            this.y += earliestWall;
        }else if(yMove < 0){
            //moving up
            const left = this.x;
            const right = this.x + this.width - EPS;
            const startY = this.y + yMove;

            let ty = Math.trunc(startY / tw);
            let txS = Math.trunc(left / tw);
            let txE = Math.trunc(right / tw);

            let earliestWall = yMove;

            for(let tx = txS; tx <= txE; tx++){
                console.log(`Collision Cycle: ${txS}->${tx}->${txE}`);
                //get the tile at these coords
                let t = this.handler.world.getTileAtWorldCoords(tx, ty);
                if(!t) return;
                
                if(renderDebug){
                    let renderX = tx * tw - this.handler.world.xOffset;
                    let renderY = ty * tw - this.handler.world.yOffset;
                    ctx.fillStyle = "red";
                    ctx.lineWidth = 3;
                    ctx.strokeRect(renderX, renderY, tw, tw);
                    ctx.fillStyle = 'Black';
                    ctx.fillText(t.isSolid + "", renderX + 4, renderY + 10);
                }

                if(t.isSolid){
                    let dy = ((ty + 1) * tw) - this.y;
                    if(dy > earliestWall) earliestWall = dy;
                }
            }

            this.y += earliestWall;
        }


    }

    #rectsCollide(r1, r2){
        /*
            Given 2 rectangles with properties x, y, width and height,
            this function returns whether or not they overlap.

            Split into 4 statements they check
                is r1's leftside left of r2's right
                is r1's rightside right of r2's left
                is r1's top above r2's bottom
                is r1's bottom below r2's top

            essentially, if 2 rects are overlapping (colliding) than all 4 of these must be true
        */
        return (
            r1.x <= r2.x + r2.width &&
            r1.x + r1.width >= r2.x &&
            r1.y <= r2.y + r2.height &&
            r1.y + r1.height >= r2.y
        );
    }


}