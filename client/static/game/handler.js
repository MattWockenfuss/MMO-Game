import { GAMESTATE } from "../GameLoop.js";

export class Handler {
    constructor(){

    }
    init(networkhandler, player, world, entityManager, inputManager, controlManager, assetManager, debugMenu){
        this.state = GAMESTATE.LOADING
        this.net = networkhandler;
        this.player = player;
        this.world = world;
        this.EM = entityManager;
        this.IM = inputManager;
        this.CM = controlManager;
        this.AM = assetManager;
        this.debug = debugMenu;
        this.GAME_WIDTH = 1500;
        this.GAME_HEIGHT = 640;
    }
    updateSize(width, height){
        this.GAME_WIDTH = width;
        this.GAME_HEIGHT = height;
    }
}