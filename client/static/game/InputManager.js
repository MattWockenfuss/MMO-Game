export class InputManager {

    constructor(handler) {
        this.handler = handler;
        this.down = new Set();
       //okay so we have a set of keys currently pressed

        document.addEventListener('keydown', (e) => {
            //console.log(`Keydown: ${e.key} ${e.keyCode} ${e.code}`);
            this.down.add(e.code);
        });

        document.addEventListener('keyup', (e) => {
            //console.log(`Keydown: ${e.key} ${e.keyCode} ${e.code}`);
            this.down.delete(e.code);
        });




    }
}

