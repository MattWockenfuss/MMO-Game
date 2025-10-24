export class ToggleControl {
    /*
        What does every ToggleControl have? a name, a key code? and wether it is toggled
    
    */
    constructor(handler, name, keyCode){
        this.handler = handler;

        this.name = name;
        this.keyCode = keyCode;
        this.alreadyCounted = false;
        this.isToggled = false;
    }

    setKeyCode(keyCode){
        this.keyCode = keyCode;
    }

    tick(){

        if(this.handler.IM.down.has(this.keyCode)){
            if(!this.alreadyCounted){
                if(!this.isToggled){
                    this.isToggled = true;
                    this.alreadyCounted = true;
                }else{
                    this.isToggled = false;
                    this.alreadyCounted = true;
                }
            }
        }else{
            this.alreadyCounted = false;
        }
    }

    toggled(){
        return this.isToggled;
    }

}