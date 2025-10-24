import { Control } from "./Control.js";
import { ToggleControl } from "./ToggleControl.js";

export class ControlManager {
    /*
        The Control manager is going to maintain a giant list of controls and through the handler you will be able to query them
        You will also be able to change the controls to your liking
    
    */
    constructor(handler){
        this.handler = handler;

        this.controls = new Map();
        
        this.controls.set('LEFT',    new Control(handler,                'LEFT',         'KeyA'));
        this.controls.set('UP',      new Control(handler,                'UP',           'KeyW'));
        this.controls.set('DOWN',    new Control(handler,                'DOWN',         'KeyS'));
        this.controls.set('RIGHT',   new Control(handler,                'RIGHT',        'KeyD'));

        this.controls.set('TOGGLEDEBUG',   new ToggleControl(handler,    'TOGGLEDEBUG',  'KeyF'));
    }

    tick(){
       for(const [controlName, controlObject] of this.controls){
            controlObject.tick();
       }
    }
}