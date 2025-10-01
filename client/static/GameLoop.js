console.log("Loading GameLoop.js!");

import { Handler } from "./game/handler.js";
import { Player } from "./game/player.js";
import { World } from "./game/world.js";
import { EntityManager } from "./game/EntityManager.js";
import { InputManager } from "./game/InputManager.js";
import { AssetManager } from "./game/AssetManager.js";
import { PacketHandler } from "./game/PacketHandler.js";



class GameEngine{
    init(networkhandler, myname, mycolor){
        //first create a handler for everyone to use, passing in net
        this.handler = new Handler();
        let player = new Player(this.handler, myname, mycolor);
        let world = new World(this.handler);
        let entityManager = new EntityManager(this.handler);
        let inputManager = new InputManager(this.handler);
        let assetManager = new AssetManager(this.handler);
        this.handler.init(networkhandler, player, world, entityManager, inputManager, assetManager);
        
        this.PH = new PacketHandler(this.handler);


        //now lets try loading the images
        const loadingAssets = this.handler.AM.loadAll();
        loadingAssets.then(() => {
            this.startGame();
        });
    }
    startGame(){
        this.canvas = document.getElementById("myCanvas");
        this.ctx = this.canvas.getContext("2d");
        
        const centerCanvas = () => {
            const s = this.canvas.style;
            s.position = "absolute";
            s.left = "50%";
            s.right = "50%";
            s.transform = "translate(-50%, -50%)";
        }

        const resizeFix = () => {
            const cssW = 1500;
            const cssH = 640;
            const ratio = Math.max(1, window.devicePixelRatio || 1);

            this.canvas.style.width = cssW + "px";
            this.canvas.style.height = cssH + "px";

            this.canvas.width = Math.round(cssW * ratio);
            this.canvas.height = Math.round(cssH * ratio);

            this.ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
            this.ctx.imageSmoothingEnabled = false;  //because we have pixel art

        };

        window.addEventListener("resize", () => {
            centerCanvas();
            resizeFix();
        });

        centerCanvas();
        resizeFix();

        this.st = 0;
        this.timer3 = 0;

        this.targetTPS = 60;
        this.MSPT = 1000 / this.targetTPS;

        this.tickTimer = 0;
        this.ticksLastSecond = 0;


        this.ticks = 0;
        this.dt = 0;
        this.swt = false;

        this.last = performance.now();  //current time in ms
        this.gameLoopFunction = this.gameLoop.bind(this);
        requestAnimationFrame(this.gameLoopFunction);
    }


    tick(){
        this.PH.processInbound();

        this.handler.player.tick();
        this.handler.world.tick();
        this.handler.EM.tick();
    }

    render(){
        this.ctx.fillStyle = "white";
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.handler.world.render(this.ctx);
        this.handler.EM.render(this.ctx);
        this.handler.player.render(this.ctx);

        this.ctx.fillStyle = "black";
        this.ctx.font = "bold italic 24px Comic Sans MS";
        this.ctx.font = " 20px monospace";


        let gap = 20;
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
        this.ctx.fillRect(0, 0, 220, (7 * gap) + 8);

        this.ctx.fillStyle = "black";
        this.ctx.fillText("Ticks: " + this.ticks, 8, 8 + (1 * gap));
        this.ctx.fillText("TicksLastSecond: " + this.ticksLastSecond, 8, 8 + (2 * gap));
        this.ctx.fillText("tickTimer: " + this.tickTimer.toFixed(1), 8, 8 + (3 * gap));
        this.ctx.fillText("dt: " + this.dt.toFixed(1), 8, 8 + (4 * gap));
        this.ctx.fillText("st: " + this.st.toFixed(1), 8, 8 + (5 * gap));
        this.ctx.fillText("timer3: " + this.timer3.toFixed(1), 8, 8 + (6 * gap));


        

    }


    gameLoop(now){
        this.dt = now - this.last;  //time since last frame in ms
        //okay how would i solve this problem?
        //okay so i know about how often i want them to activate, every MSPT

        this.st += this.dt;
        this.timer3 += this.dt;

        this.tickTimer = Math.min(this.tickTimer += this.dt, this.MSPT * 4); // so we can at most be behind 4 ticks that it will try and catch up quickly

        if(this.tickTimer > this.MSPT){
            this.tick();
            this.ticks++;
            this.tickTimer -= this.MSPT;
        }

        this.last = now;
        
        
        if(this.st > 1000){
            // on second timer
            this.swt = !this.swt;
            this.st = 0;
            this.ticksLastSecond = this.ticks;
            this.ticks = 0;
        }

        
        this.render();
        
        this.dt = 0;
        requestAnimationFrame(this.gameLoopFunction);
    }
}



const game = new GameEngine();
export default game;




