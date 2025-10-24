export class Control {
    /*
        What does every control have? a name, a list of key codes, and whether it is pressed or not
    
    */
    constructor(handler, name, keyCode){
        this.handler = handler;

        this.name = name;
        this.keyCode = keyCode;
        this.isPressed = false;
    }

    tick(){
        if(this.handler.IM.down.has(this.keyCode)){
            this.isPressed = true;
        }else{
            this.isPressed = false;
        }
    }

    setKeyCode(keyCode){
        this.keyCode = keyCode;
    }

    down(){
        return this.isPressed;
    }

}