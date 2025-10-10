export class AssetManager{
    constructor(handler){
        this.handler = handler;
        this.images  = new Map();
        this.toLoad = 
        [
            {name: 1, url: "./static/assets/grass.png"},
            {name: 2, url: "./static/assets/sand.png"},
            {name: 3, url: "./static/assets/stone-floor.png"},
            {name: 4, url: "./static/assets/stone-wall.png"},
            {name: 5, url: "./static/assets/void.png"},
            {name: 6, url: "./static/assets/darker-blue.png"},
            {name: 7, url: "./static/assets/wood-floor.png"},
            {name: 8, url: "./static/assets/wood-wall.png"},
            {name: 9, url: "./static/assets/desert-stone-wall.png"},
            {name: 10, url: "./static/assets/sand-noisy.png"},
            {name: 11, url: "./static/assets/sand-quarry.png"},
            {name: 12, url: "./static/assets/sand-wave.png"},
        ]

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

    async loadAll(){
        const promises = this.toLoad.map(item => this.loadImage(item.name, item.url));
        await Promise.all(promises);
        return this;
    }

    get(name){
        return this.images.get(name);
    }


}