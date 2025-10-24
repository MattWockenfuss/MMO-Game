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
        
        //here we are going to define all of our controls
        this.controls.set('LEFT',    new Control(handler,                'LEFT',         'KeyA'));
        this.controls.set('UP',      new Control(handler,                'UP',           'KeyW'));
        this.controls.set('DOWN',    new Control(handler,                'DOWN',         'KeyS'));
        this.controls.set('RIGHT',   new Control(handler,                'RIGHT',        'KeyD'));
        
        this.controls.set('TOGGLEDEBUG',   new ToggleControl(handler,    'TOGGLEDEBUG',  'KeyF'));
    }

    tick(){
        /*
            Alright, so we have a map of controls and from the input manager we have a set of keys that are down
            we want each of the Controls to check for their key and update themself
        */
       for(const [controlName, controlObject] of this.controls){
            controlObject.tick();
       }
    }
}