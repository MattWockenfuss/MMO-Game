export class AssetManager{
    constructor(handler){
        this.handler = handler;
        this.images  = new Map();

        //this.loadAllFromServer();
    }

    async loadAllFromServer(){
        //this function reads from the assets index at the server
        const res = await fetch("/static-index")
        //console.log(`STATIC LIST: ${res}`);
        const resJSON = await res.json();
        console.log(resJSON);


        const loadPromises = Object.entries(resJSON).map(async ([name, url]) => {
            console.log(`ATTEMPTING TO LOAD '${name}' from '${url}'`);
            const img = await this.loadImage(name, url);
            //this.images.set(name, img);//store in the map
        });

        await Promise.all(loadPromises);
    }

    loadImage(name, url){
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.images.set(name, img);
                resolve(img);
            };
            img.onerror = () => reject(new Error(`Failed to load ${url}`));
            img.src = url;
        });
    }

    get(name){
        return this.images.get(name);
    }


}