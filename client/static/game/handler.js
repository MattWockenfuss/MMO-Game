export class Handler {
    constructor(){

    }
    init(networkhandler, player, world, entityManager, inputManager, assetManager, debugMenu){
        this.net = networkhandler;
        this.player = player;
        this.world = world;
        this.EM = entityManager;
        this.IM = inputManager;
        this.AM = assetManager;
        this.debug = debugMenu;
    }
}