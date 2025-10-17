export class InputManager {

    constructor(handler) {
        this.handler = handler;
        this.down = new Set();
       //okay so we have a set of keys currently pressed
       //these are relative to the canvas, only way to do it reliably i feel
       this.mouseX = 0;
       this.mouseY = 0;
    }

    attachListeners(canvas, on){
        on(window, 'keydown', (e) => {this.down.add(e.code);});
        on(window, 'keyup', (e) => {this.down.delete(e.code);});
        on(canvas, 'mousedown',(e) => {
            if(e.button == 0) this.down.add("leftMouseBTN");
            if(e.button == 1) this.down.add("rightMouseBTN");
            if(e.button == 2) this.down.add("middleMouseBTN");
            let {x, y} = this._getMouseOnCanvas(e, canvas);
            this.mouseX = x;
            this.mouseY = y;
            //console.log(`Mouse down Button ${e.button} ${e.offsetX},${e.offsetY} `)
        });
        on(canvas, 'mouseup',(e) => {
            if(e.button == 0) this.down.delete("leftMouseBTN");
            if(e.button == 1) this.down.delete("rightMouseBTN");
            if(e.button == 2) this.down.delete("middleMouseBTN");
            let {x, y} = this._getMouseOnCanvas(e, canvas);
            this.mouseX = x;
            this.mouseY = y;
            //console.log(`Mouse up Button ${e.button} ${e.offsetX},${e.offsetY} `)
        });
        on(canvas, 'mousemove',(e) => {
            //console.log(`Mouse move Button ${e.button} ${e.offsetX},${e.offsetY} `)
            let {x, y} = this._getMouseOnCanvas(e, canvas);
            this.mouseX = x;
            this.mouseY = y;
        });
    }


    // Use this in your InputManager
    _getMouseOnCanvas(e, canvas) {
        const rect = canvas.getBoundingClientRect();

        const cssX = e.clientX - rect.left;
        const cssY = e.clientY - rect.top;

        const scaleX = this.handler.GAME_WIDTH / rect.width;
        const scaleY = this.handler.GAME_HEIGHT / rect.height;

        let x = cssX * scaleX;
        let y = cssY * scaleY;

        return { x, y };
    }


}

