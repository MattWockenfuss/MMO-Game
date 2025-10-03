export class InputManager {

    constructor(handler) {
        this.handler = handler;
        this.down = new Set();
       //okay so we have a set of keys currently pressed
    }

    attachListeners(canvas, on){
        on(window, 'keydown', (e) => {this.down.add(e.code);})
        on(window, 'keyup', (e) => {this.down.delete(e.code);})
    }


}

