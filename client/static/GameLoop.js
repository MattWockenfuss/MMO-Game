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
        this._rafID = 0;
        this._listeners = [];
        this._trackedSocket = null;
        this._onSocketClose = null;
        this._dead = false;

        this.handler = new Handler();
        
        let player = new Player(this.handler, myname, mycolor);
        let world = new World(this.handler);
        let entityManager = new EntityManager(this.handler);
        let inputManager = new InputManager(this.handler);
        let assetManager = new AssetManager(this.handler);

        this.handler.init(networkhandler, player, world, entityManager, inputManager, assetManager);
        
        //now lets try loading the images
        const loadingAssets = assetManager.loadAll();
        loadingAssets.then(() => {
            this.startGame();
        });

        this.PH = new PacketHandler(this.handler);
        this.net = networkhandler;
        this._unsubscribeNetworkClose?.()
        this._unsubscribeNetworkClose = this.net.subscribeOnClose((e) => {
            this.stop();
            let msgBox = document.getElementById("msg");
            msgBox.style.visibility = "visible";
            msgBox.textContent = `${e.code} ${e.reason}`;
        });



    }
    on = (el, ev, cb, opts) => {
        el.addEventListener(ev, cb, opts);
        this._listeners.push([el, ev, cb, opts]);
        //el = element, ev = event, cb = callback, and opts = options
        console.log(`Now Tracking "${el}.${ev} and calling ${cb}"`);
        return cb;
    }
    offAll(){
        for(const [el, ev, cb, opts] of this._listeners){
            el.removeEventListener(ev, cb, opts);
        }
        this._listeners.length = 0;
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

        this.on(window, "resize", (e) => {
            centerCanvas();
            resizeFix();
        });
        this.handler.IM.attachListeners(this.canvas, this.on);

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
        this._rafID = requestAnimationFrame(this.gameLoopFunction);
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }


    tick(){
        this.PH.processInbound();

        this.handler.player.tick();
        this.handler.world.tick();
        this.handler.EM.tick();
    }

    render(){
        if (!this.ctx || !this.canvas) return;

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
        //this.ctx.fillText("Ticks: " + this.ticks, 8, 8 + (1 * gap));
        this.ctx.fillText("TicksLastSecond: " + this.ticksLastSecond, 8, 8 + (2 * gap));
        this.ctx.fillText("st: " + (this.st).toFixed(1), 8, 8 + (3 * gap));
        
        if(this.handler.player !== null && this.handler.player !== undefined){
            this.ctx.fillText("x: " + (this.handler.player.x).toFixed(1), 8, 8 + (5 * gap));
            this.ctx.fillText("y: " + (this.handler.player.y).toFixed(1), 8, 8 + (6 * gap));
        }
        if(this.handler.world !== null && this.handler.world !== undefined){
            if(this.handler.world.xOffset !== null && this.handler.world.yOffset !== undefined){
                this.ctx.fillText("xOffset: " + (this.handler.world.xOffset).toFixed(1), 8, 8 + (7 * gap));
                this.ctx.fillText("yOffset: " + (this.handler.world.yOffset).toFixed(1), 8, 8 + (8 * gap));
            }
        }

        this.ctx.fillText("mouseX: " + (this.handler.IM.mouseX).toFixed(1), 8, 8 + (9 * gap));
        this.ctx.fillText("mouseY: " + (this.handler.IM.mouseY).toFixed(1), 8, 8 + (10 * gap));


        //this.ctx.fillText("timer3: " + this.timer3.toFixed(1), 8, 8 + (6 * gap));
        //this.ctx.fillText("tickTimer: " + this.tickTimer.toFixed(1), 8, 8 + (3 * gap));
        //this.ctx.fillText("dt: " + this.dt.toFixed(1), 8, 8 + (4 * gap));

        

    }


    gameLoop(now){
        if(this._dead) return;

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
        this._rafID = requestAnimationFrame(this.gameLoopFunction);
    }

    stop = () => {
        /*
            This is the stop game function, we stop the animation frame, close all of the eventListeners we have attached as we were keeping track of them
            and keep track of a private variable _dead which
        */
        const game = document.getElementById("game");
        const loginFormDiv = document.getElementById("login");
        const loginForm = document.getElementById("loginForm");

        game.hidden = true;
        loginFormDiv.hidden = false;
        loginForm.reset();


        //now for the killing
        if(this._dead) return;
        this._dead = true;

        this._unsubscribeNetworkClose?.();
        this._unsubscribeNetworkClose = null;

        if(this._rafID){
            cancelAnimationFrame(this._rafID);
            this._rafID = 0;
        }
        this.offAll();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx = null;
        this.canvas = null;
        this.handler = null;
        console.log(`STOPPED GAME LOOP!!!!!!!!!!!!`);
    }

}



const game = new GameEngine();
export default game;




