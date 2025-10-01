export class Handler {
    constructor(){

    }
    init(networkhandler, player, world, entityManager, inputManager, assetManager){
        this.net = networkhandler;
        this.player = player;
        this.world = world;
        this.EM = entityManager;
        this.IM = inputManager;
        this.AM = assetManager;
    }
}