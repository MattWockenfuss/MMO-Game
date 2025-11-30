export class State {
    constructor(handler){
        this.handler = handler;
    }

    tick(){};
    render(ctx){}
}