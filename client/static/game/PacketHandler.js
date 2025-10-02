import { OtherPlayer } from "./entites/OtherPlayer.js";

export class PacketHandler{
    constructor(handler){
        this.handler = handler;
        this.packetMap = {
            move:           (data) => this.onMove(data),
            login:          (data) => this.onLogin(data),
            world:          (data) => this.onWorld(data),
            onOtherPlayer:  (data) => this.onOtherPlayer(data),
            Disconnect:     (data) => this.onDisconnect(data)
        }

    }
    
    processInbound(){
        for(const packet of this.handler.net.inbound) {
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
        this.handler.EM.addEntity(new OtherPlayer(data.x, data.y, data.session_id, data.username, data.color));
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
        this.handler.world.printWorldData();
    }
    onOtherPlayer(data){
        console.log(data.username);
        console.log(data.x);
        console.log(data.y);
        console.log(data.session_id);
        console.log(data.color);

        this.handler.EM.addEntity(new OtherPlayer(data.x, data.y, data.session_id, data.username, data.color));
    }
    onDisconnect(data){
        //{"type": "Disconnect", "data": {"session_id": "2vYQJ6OP", "code": 1000, "reason": "Kicked by Console!"}}
        this.handler.EM.removeEntity(this.handler.EM.getPlayerIndexBySessionID(data.session_id));
    }
}