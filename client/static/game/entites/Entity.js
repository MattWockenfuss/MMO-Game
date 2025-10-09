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
            let tileRectsArray = [];
            
            //add the first and last points, because we must alway check at least the top and bottom no matter what
            let sxP = this.x + this.width + xMove;
            let syP = this.y;

            let exP = this.x + this.width + xMove;
            let eyP = this.y + this.height;

            //now check if the distance between them is less than tw, if it is just add the first one
            let distance = this.height; //the distance between the top and bottom
            let yIndex = 1;
            let tx = Math.trunc(sxP / tw);
            let ty = Math.trunc(syP / tw);
            
            let t = this.handler.world.getTileAtWorldCoords(tx, ty);
            tileRectsArray.push({
                ID: t.ID,
                x: tx,
                y: ty
            });

            while(distance > tw){
                //then we want to add another tile
                let tx = Math.trunc(sxP / tw);
                let ty = Math.trunc((syP + (yIndex * tw)) / tw);
                let t = this.handler.world.getTileAtWorldCoords(tx, ty);
                tileRectsArray.push({
                    ID: t.ID,
                    x: tx,
                    y: ty
                });
                distance -= tw;
                yIndex++;
            }
            //now check if our height is already included
            let found = false;
            tx = Math.trunc(exP / tw);
            ty = Math.trunc(eyP / tw);
            
            for(let t of tileRectsArray){
                if(t.x == tx && t.y == ty) found = true;
            }
            if(!found){
                let t = this.handler.world.getTileAtWorldCoords(tx, ty);
                tileRectsArray.push({
                    ID: t.ID,
                    x: tx, 
                    y: ty
                });
            }

            //alright so we have an array list of all of the tiles to check for collisiom
            //its not super efficient but it is cleaner, revisit in a few weeks probs
            //we can definitely come up with a better algorithm for generating the list of tiles
            //right now we loop through the whole thing and add the last one if its not there
            //probably fine for performance because in reality our entites won't be that big but still
            
            for(const tr of tileRectsArray){
                let renderX = tr.x * tw - this.handler.world.xOffset;
                let renderY = tr.y * tw - this.handler.world.yOffset;
                ctx.fillStyle = "red";
                ctx.lineWidth = 3;
                ctx.strokeRect(renderX, renderY, tw, tw);
                ctx.fillStyle = 'Black';
                ctx.fillText(this.handler.world.tileMap.get(tr.ID).isSolid + "", renderX + 4, renderY + 10);
            }

            //now what? how do do actual collision? well loop through the tiles, and if they are solid, dont let us through
            
            let earliestWall = xMove;
            console.log(`Earliest Wall: ${earliestWall}`);
            for(const tr of tileRectsArray){
                if(this.handler.world.getTileByID(tr.ID).isSolid){
                    //for every solid wall we are checking, if distance to wall is less than xMove
                    //then set xMove equal to that distance
                    //since we are moving right, distance = wall - player
                    let dx = (tr.x * tw) - (this.x + this.width);
                    if(dx < earliestWall) earliestWall = dx;
                }
            }
            //so now earliestWall is now the closest solid object
            console.log(`Earliest Wall AFTER: ${earliestWall}`);
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