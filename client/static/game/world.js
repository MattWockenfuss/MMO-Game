export class World{ 
    constructor(handler){
        this.handler = handler;
        this.worldData = null;
        this.worldWidth = null;


    }
    tick(){

    }
    render(ctx){
        let size = 64;
        if(this.worldData != null){
            for(let row = 0; row < (this.worldData.length / this.worldWidth); row++){
                for(let x = 0; x < this.worldWidth; x++){
                    let id = this.worldData[(row * this.worldWidth) + x]
                    if (this.handler.AM.get(this.worldData[(row * this.worldWidth) + x])) ctx.drawImage(this.handler.AM.get(id), x * size, row * size, size, size)
                    
                }
            }
        }
    }
    setWorldData(data){
        //okay so we can set the world data in this function, everything about it
        for(const key of Object.keys(data)){
            console.log(`${key} : ${data[key]}`)
        }
        //AQIDBAUGBwgICAECAgICAgICBwcBAQEBAQQEBAcHAQEBBgYGBgQDAwEBAQYGBgYEAwM= is the world data right now
        console.log("Trying to decode world data!")
        //okay
        var decoded = atob(data["world-data"]);
        console.log(decoded);
        var bytes = new Int8Array(decoded.length);
        for(let i = 0; i < decoded.length; i++){
            //console.log(decoded.charCodeAt(i));
            bytes[i] = decoded.charCodeAt(i);
        }
        console.log("setting class vars")
        this.worldData = bytes;
        this.worldWidth = data["world-width"]
        //console.log(`${decoded}`);
        //console.log(`${bytes}`);
        //console.log(`World width = ${data['world-width']}`)
        //okay now we have the data stores in bytes array
    }
    printWorldData(){
        console.log("in the print function!")
        for(let row = 0; row < (this.worldData.length / this.worldWidth); row++){
            //now we get and print the row
            let builderString = "";
            for(let x = 0; x < this.worldWidth; x++){
                builderString += this.worldData[(row * this.worldWidth) + x] + " ";
            }
            console.log(builderString);
        }
    }
}