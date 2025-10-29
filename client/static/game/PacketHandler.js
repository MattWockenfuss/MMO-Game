import { Enemy } from "./entities/Enemy.js";
import { StaticEntity } from "./entities/StaticEntity.js";
import { OtherPlayer } from "./entities/OtherPlayer.js";

export class PacketHandler{
    constructor(handler){
        this.handler = handler;
        this.packetMap = {
            move:           (data) => this.onMove(data),
            login:          (data) => this.onLogin(data),
            world:          (data) => this.onWorld(data),
            onOtherPlayer:  (data) => this.onOtherPlayer(data),
            Disconnect:     (data) => this.onDisconnect(data),
            Enemy:          (data) => this.onEnemy(data),
            StaticEntity:   (data) => this.onStaticEntity(data),
            loginVerify:    (data) => this.onLoginVerify(data)
        }

    }
    
    processInbound(){
        for(const packet of this.handler.net.inbound) {
            console.log(packet.data);
            const handler = this.packetMap[packet.type];
            if(handler){
                handler(packet.data);
            }else{
                console.warn(`[PacketHandler] Unhandled Packet Type "${packet.type}"`);
            }
        }
        this.handler.net.inbound.length = 0;
    }


    onLogin(data){
        //this packet is the login of other players
        this.handler.EM.addEntity(new OtherPlayer(this.handler, data.x, data.y, data.session_id, data.username, data.color));
    }
    onLoginVerify(data){
        console.log(`LOGINVERIFY: ${data}`);
    }

    onStaticEntity(data){
        console.log(`STATIC ENTITY: ${data}`);
        //This packet is used when first loading into the game to fill the world with static entities
        
        for (const [key, value] of Object.entries(data)){
            //console.log(`${key}, ${value}`);
            console.log(value.type);
            console.log(value.UUID);
            console.log(`(${value.x}, ${value.y})`);
            console.log(value.level);
            console.log(value.health);
            this.handler.EM.addEntity(new StaticEntity(this.handler, value));
        }



    }

    onMove(data){
        //this is the move of other players
        //console.log(data);
        //console.log(data.session_id);
        const player = this.handler.EM.getPlayerBySessionID(data.session_id);
        if(player != null){
            player.x = data.x;
            player.y = data.y;
        }
    }

    onWorld(data){
        this.handler.world.setWorldData(data);
        //this.handler.world.printWorldData();
    }
    onOtherPlayer(data){
        // console.log(data.username);
        // console.log(data.x);
        // console.log(data.y);
        // console.log(data.session_id);
        // console.log(data.color);

        this.handler.EM.addEntity(new OtherPlayer(this.handler, data.x, data.y, data.session_id, data.username, data.color));
    }
    onEnemy(data){
        console.log(data)
        for(let uuid in data){
            this.handler.EM.addEntity(new Enemy(this.handler, data[uuid]));
        }
    }
    onDisconnect(data){
        //{"type": "Disconnect", "data": {"session_id": "2vYQJ6OP", "code": 1000, "reason": "Kicked by Console!"}}
        this.handler.EM.removeEntity(this.handler.EM.getPlayerIndexBySessionID(data.session_id));
    }
}