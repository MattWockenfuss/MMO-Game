import { State } from "./State.js";

export class LoadingState extends State {
    constructor(handler){
        super(handler);
    }

    tick(){

    }
    render(ctx){
        ctx.fillStyle = "blue";
        ctx.fillRect(0, 0, this.handler.GAME_WIDTH, this.handler.GAME_HEIGHT);
    }
}