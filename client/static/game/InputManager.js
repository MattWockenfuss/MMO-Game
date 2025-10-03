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
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;
            //console.log(`Mouse down Button ${e.button} ${e.offsetX},${e.offsetY} `)
        });
        on(canvas, 'mouseup',(e) => {
            if(e.button == 0) this.down.delete("leftMouseBTN");
            if(e.button == 1) this.down.delete("rightMouseBTN");
            if(e.button == 2) this.down.delete("middleMouseBTN");
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;
            //console.log(`Mouse up Button ${e.button} ${e.offsetX},${e.offsetY} `)
        });
        on(canvas, 'mousemove',(e) => {
            //console.log(`Mouse move Button ${e.button} ${e.offsetX},${e.offsetY} `)
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;
        });
    }


}

