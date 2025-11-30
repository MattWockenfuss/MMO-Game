import { State } from "./State.js";

export class GamestateState extends State {
    constructor(handler){
        super(handler);
    }

    tick(){
        this.handler.PH.processInbound();
        this.handler.CM.tick();
        this.handler.world.tick();
        this.handler.EM.tick();
    }
    render(ctx, ticksLastSecond){
        this.handler.world.render(ctx);
        this.handler.EM.render(ctx);
        this.handler.debug.render(ctx, ticksLastSecond);
    }
}