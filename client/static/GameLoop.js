console.log("Loading GameLoop.js!");

import { Handler } from "./game/handler.js";
import { Player } from "./game/entities/player.js";
import { World } from "./game/world.js";
import { EntityManager } from "./game/EntityManager.js";
import { InputManager } from "./game/input/InputManager.js";
import { AssetManager } from "./game/AssetManager.js";
import { PacketHandler } from "./game/PacketHandler.js";
import { DebugMenu } from "./game/DebugMenu.js";
import { ControlManager } from "./game/input/ControlManager.js";
import { LoadingState } from "./game/states/LoadingState.js";
import { GamestateState } from "./game/states/GamestateState.js";

export const GAMESTATE = {
    PLAYING: "Playing",
    LOADING: "Loading"
}


class GameEngine{
    init(networkhandler, myname, mycolor){
        this.handler = new Handler();
        
        networkhandler.handler = this.handler;

        let player = new Player(this.handler, myname, mycolor);
        let world = new World(this.handler);
        let entityManager = new EntityManager(this.handler);
        let inputManager = new InputManager(this.handler);
        let controlManager = new ControlManager(this.handler);
        let assetManager = new AssetManager(this.handler);
        let debugMenu = new DebugMenu(this.handler);
        let PH = new PacketHandler(this.handler);

        this.GamestateState = new GamestateState(this.handler);
        this.LoadingState = new LoadingState(this.handler);
        
        this.handler.init(this, networkhandler, player, world, entityManager, inputManager, controlManager, PH, assetManager, debugMenu);
        this.handler.EM.addEntity(player);    

        this._rafID = 0;
        this._listeners = [];
        this._dead = false;

        this.canvas = document.getElementById("myCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.st = 0;  //second timer
        this.targetTPS = 60;
        this.MSPT = 1000 / this.targetTPS;
        this.tickTimer = 0;
        this.ticksLastSecond = 0;
        this.ticks = 0;
        this.dt = 0;


        const centerCanvas = () => {
            const s = this.canvas.style;
            s.position = "fixed";
            s.left = "50%";
            s.top = "50%";
            s.transform = "translate(-50%, -50%)";
        }

        const resizeFix = () => {
            const cssW = Math.floor(window.innerWidth  * 1);
            const cssH = Math.floor(window.innerHeight * 1);
            this.canvas.style.width  = cssW + "px";
            this.canvas.style.height = cssH + "px";

            const dPRRAW = window.devicePixelRatio || 1
            const dPR = Math.max(1 , Math.round(dPRRAW));
            
            this.canvas.width = cssW * dPR;
            this.canvas.height = cssH * dPR;

            this.ctx.setTransform(dPR, 0, 0, dPR, 0, 0);
            this.ctx.imageSmoothingEnabled = false;  //because we have pixel art
            

            //we have to tell the handler that we changed size
            this.handler.updateSize(cssW, cssH);
            console.log(`NEW DPR ${dPRRAW} adj:${dPR}`);
            console.log(`cssW x cssH ${cssW} x ${cssH}`);
            console.log(`canvasWidth x canvasHeight ${this.canvas.width} x ${this.canvas.height}`);
        };
        this.on(window, "resize", (e) => {
            centerCanvas();
            resizeFix();
        });

        centerCanvas();
        resizeFix();
        this.handler.IM.attachListeners(this.canvas, this.on);



        //now lets try loading the images
        const loadingAssets = assetManager.loadAllFromServer();
        loadingAssets.then(() => {
            console.log("Done Loading Assets!");
            this.handler.state = GAMESTATE.PLAYING;

            this.last = performance.now();
            this.gameLoopFunction = this.gameLoop.bind(this);
            this._rafID = requestAnimationFrame(this.gameLoopFunction);
        });


    }
    on = (el, ev, cb, opts) => {
        el.addEventListener(ev, cb, opts);
        this._listeners.push([el, ev, cb, opts]);
        //el = element, ev = event, cb = callback, and opts = options
        //console.log(`Now Tracking "${el}.${ev} and calling ${cb}"`);
        return cb;
    }
    offAll(){
        for(const [el, ev, cb, opts] of this._listeners){
            el.removeEventListener(ev, cb, opts);
        }
        this._listeners.length = 0;
    }


    tick(){
        switch(this.handler.state){
            case GAMESTATE.LOADING:
                this.LoadingState.tick();
                break;
            case GAMESTATE.PLAYING:
                this.GamestateState.tick();
                break;
        }

    }
    render(){
        if (!this.ctx || !this.canvas) return;

        this.ctx.fillStyle = "black";
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);


        switch(this.handler.state){
            case GAMESTATE.LOADING:
                this.LoadingState.render(this.ctx);
                break;
            case GAMESTATE.PLAYING:
                this.GamestateState.render(this.ctx, this.ticksLastSecond)
                break;
        }

    }


    gameLoop(now){
        if(this._dead) return;

        this.dt = now - this.last;  //time since last frame in ms
        this.st += this.dt;

        this.tickTimer = Math.min(this.tickTimer += this.dt, this.MSPT * 4); // so we can at most be behind 4 ticks that it will try and catch up quickly

        if(this.tickTimer > this.MSPT){
            this.tick();
            this.ticks++;
            this.tickTimer -= this.MSPT;
        }
        this.last = now;
        if(this.st > 1000){
            this.st = 0;
            this.ticksLastSecond = this.ticks;
            this.ticks = 0;
        }
        this.render();
        
        this.dt = 0;
        this._rafID = requestAnimationFrame(this.gameLoopFunction);
    }

    stop = (e) => {
        /*
            This is the stop game function, we stop the animation frame, close all of the eventListeners we have attached as we were keeping track of them
            and keep track of a private variable _dead which
        */
        const game = document.getElementById("game");
        const loginPage = document.getElementById("loginPage");
        const loginForm = document.getElementById("loginForm");

        game.hidden = true;
        loginPage.hidden = false;
        loginForm.reset();


        //now for the killing
        if(this._dead) return;
        this._dead = true;

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

        let msgBox = document.getElementById("msg");
        msgBox.style.visibility = "visible";
        msgBox.textContent = `${e.code} ${e.reason}`;
    }

}



const game = new GameEngine();
export default game;




