import { Enemy } from "./entities/Enemy.js";
import { StaticEntity } from "./entities/StaticEntity.js";
import { OtherPlayer } from "./entities/OtherPlayer.js";
import { GAMESTATE } from "../GameLoop.js";
import NetworkHandler from "./NetworkHandler.js";


export class PacketHandler{
    constructor(handler){
        this.handler = handler;
        this.packetMap = {
            move:           (data) => this.move(data),
            login:          (data) => this.login(data),
            login_res:      (data) => this.login_res(data),
            world:          (data) => this.world(data),
            playerLOGIN:    (data) => this.playerLOGIN(data),
            playerLOGOUT:   (data) => this.playerLOGOUT(data),
            enemy:          (data) => this.enemy(data),
            static:         (data) => this.static(data),
            switch_execute: (data) => this.switch_execute(data)
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

    async switch_execute(data){
        let worldserverIP = data.IP;
        let coords = data.CoordsTo;
        console.log(`We are going to switch worlds to ${worldserverIP} at ${coords[0]}, ${coords[1]}`);

        this.handler.state = GAMESTATE.LOADING;
        this.handler.net.switchclose();
        //alright now for the fun stuff, we want to create a new network handler, open a connection with the new server, 
        //wait for connection, upon login, 

        //then we were authenticated!, lets connect to the world server!
        

        let newServer = new NetworkHandler(this.handler, worldserverIP);
        await newServer.waitForOpen();
        this.handler.net = newServer;

        this.handler.player.x = coords[0];
        this.handler.player.y = coords[1];
        

        var p = {
            "username": this.handler.player.username,
            "color": this.handler.player.color,
            "x": coords[0],
            "y": coords[1]
        }


        //we also need to clear all of the entities except for us.
        this.handler.EM.clearAllExceptPlayer();

        console.log(p)
        this.handler.net.send("login", p);
        this.handler.state = GAMESTATE.PLAYING;



    }

    login_res(data){
        //console.log(data);

        //so we have logged into the server, they sent back what kind of server we are connected to!
        console.log(data.nameID);
        this.handler.world.nameID = data.nameID;
    }

    login(data){
        //this packet is the login of other players
        this.handler.EM.addEntity(new OtherPlayer(this.handler, data.x, data.y, data.session_id, data.username, data.color));
        this.handler.state = GAMESTATE.PLAYING;
    }
    authenticate(data){
        console.log(`LOGINVERIFY: ${data}`);
    }

    static(data){
        //console.log(`STATIC ENTITY: ${data}`);
        //This packet is used when first loading into the game to fill the world with static entities
        
        for(let UUID in data){
            console.log(this.handler.world.staticsRegistry);
            console.error(`${UUID} => ${JSON.stringify(data[UUID])}`);
            //also attach the data from the statics dict
            let codename = data[UUID]['type'];
            console.log(codename);
            let entityDict = this.handler.world.staticsRegistry[codename];
            console.log(`Size: ${entityDict.size[0]}, ${entityDict.size[1]}`);

            this.handler.EM.addEntity(new StaticEntity(this.handler, data[UUID], entityDict));
        }
    }

    move(data){
        //this is the move of other players
        console.log(data);
        //console.log(data.session_id);
        const player = this.handler.EM.getPlayerBySessionID(data.UUID);
        if(player != null){
            player.x = data.x;
            player.y = data.y;
        }
    }

    world(data){
        this.handler.world.setWorldData(data);
        //this.handler.world.printWorldData();
    }
    playerLOGIN(data){
        // console.log(data.username);
        // console.log(data.x);
        // console.log(data.y);
        // console.log(data.session_id);
        // console.log(data.color);
        this.handler.EM.addEntity(new OtherPlayer(this.handler, data.x, data.y, data.session_id, data.username, data.color));
    }
    enemy(data){
        //console.log(data)
        for(let uuid in data){
            this.handler.EM.addEntity(new Enemy(this.handler, data[uuid]));
        }
    }
    playerLOGOUT(data){
        //{"type": "Disconnect", "data": {"session_id": "2vYQJ6OP", "code": 1000, "reason": "Kicked by Console!"}}
        this.handler.EM.removeEntity(this.handler.EM.getPlayerIndexBySessionID(data.session_id));
    }
}