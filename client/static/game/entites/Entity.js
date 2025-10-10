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
        let renderDebug = true;
        /*
            This function takes in xMove and yMove of the calling entity, combined with their hitbox and the world, it figures out
            if they are allowed to move where they are, if so let them move, if not, snap to world. If the calling entity is an instance 
            of the player, then we also want to send to the world server that we are moving.

            Every entity has an x, y, width, and height (square hitbox) and height.
        */
        
        //alright whats the first thing we do with collision
        //well we have to split up xMove and yMove into positive and negative

        if(xMove > 0){
            let tw = Tile.tileWidth;
            
            const top = this.y;
            const bottom = this.y + this.height;
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
            //we are moving left, don't include width
            this.x += xMove;
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