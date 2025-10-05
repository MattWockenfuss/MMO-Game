import { OtherPlayer } from "./entites/OtherPlayer.js";

export class EntityManager{
    constructor(handler){
        this.handler = handler;
        this.entities = [];
    }
    tick(){
        for(const entity in this.entities){
            entity.tick();
        }
    }
    render(ctx){
        for(const entity in this.entities){
            entity.render(ctx);
        }
    }

    addEntity(entity){
        this.entities.push(entity);
        console.log("Entity Added!");
    }
    removeEntity(index){
        console.log(`Removing Entities[${index} which is ${typeof(this.entities[index])}]`);
        this.entities.splice(index, 1); //removes the indexth element O(n)
    }
    getEntity(index){
        return this.entities[index];
    }
    getPlayerBySessionID(session_id){
        for(let i = 0; i < this.entities.length; i++){
            if(this.entities[i] instanceof OtherPlayer){
                //console.log(`Comparing ${this.entities[i].session_id} ===? ${session_id}`)
                if(this.entities[i].session_id === session_id){
                    //console.log(`Player in list! ${this.entities[i].session_id}`);
                    return this.entities[i];
                }
            }
        }
        return null;
    }
    getPlayerIndexBySessionID(session_id){
        const idx = this.entities.findIndex(e => e.session_id == session_id);
        return idx;
    }
}