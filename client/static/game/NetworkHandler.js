export default class NetworkHandler{
    constructor(ipport){
        this.ws = new WebSocket(`ws://${ipport}/`);
        this.inbound = [];
        this._closeSubscribers = new Set();

        this._onWSClose = (e) => {
            for(const cb of this._closeSubscribers){
                cb(e);
            }
        }
        
        this.ws.onopen = () => {
            console.log("Connected to World Server!");
        }
        this.ws.onmessage = (event) => {
            //console.log(event.data);
            try {
                const packet = JSON.parse(event.data);
                //console.log(`${packet.type} : ${JSON.stringify(packet.data)}`);
                //handlers[packet.type](packet.data);
                //put on queue
                this.inbound.push(packet);
            } catch (error){
                console.error("[ERROR] Reading Packet => " + event.data);
                console.error(`->    ${error}`);
            }
        }
        this.ws.onerror = (event) => {
            console.error("[ERROR] ")
        }
        this.ws.onclose = (event) => {
            this._onWSClose(event);



            //in here 'transfer' back to login page, stop game loop, etc..., reset everything
            //display the reason on screen
        }
    }
    subscribeOnClose(cb){
        this._closeSubscribers.add(cb);
        // return an unsubscribe if we want? this is a crazy pattern i need to think about this
        return () => this._closeSubscribers.delete(cb);
    }
    close(code = 1000, reason = 'Client Quit'){
        try {
            this.ws.close(code, reason);
        } catch {
            console.log(`ERROR TRYING TO CLOSE SOCKET ${code}, ${reason}`);
        }
    }
    waitForOpen(timeout = 2000){
        if(this.ws.readyState === WebSocket.OPEN) return Promise.resolve();
        
        /* 
            If Socket is open, return
            Wait upto timeout, if socket opens or errors during that time, say so then.
            Otherwise, at timeout, return timeout
        
        
        */


        return new Promise((resolve, reject) => {
            const onOpen = () => { cleanup(); resolve(); };
            const onError = (e) => { cleanup(); reject(e); };
            const onTimeout = () => { cleanup(); reject(new Error('WS open timeout')); };

            const cleanup = () => {
            this.ws.removeEventListener('open', onOpen);
            this.ws.removeEventListener('error', onError);
            clearTimeout(t);
            };

            this.ws.addEventListener('open', onOpen, { once: true });
            this.ws.addEventListener('error', onError, { once: true });
            const t = setTimeout(onTimeout, timeout);
        });
    }
    waitForLoginVerify(predicate = () => true, timeout = 2000){
        /* 
            Okay so we have established a connection to the server, wait for a reply of type loginVerify, if its not that, add to the inbound queue just incase
            something weird happens
        */
        
        return new Promise((resolve, reject) => {
            const onMessage = (e) => {
                let msg = e.data;
                if (typeof msg === 'string') {
                    try { msg = JSON.parse(msg); } catch { return; }
                }
                if (predicate(msg)) cleanup(resolve, msg);
            }

            const onError  = () => cleanup(reject, new Error('WS error'));
            const onClose  = (ev) => cleanup(reject, new Error(`WS closed ${ev.code} ${ev.reason||''}`));
            const onTimeout = () => cleanup(reject, new Error('WS wait timeout'));

            const cleanup = (fn, val) => {
                this.ws.removeEventListener('message', onMessage);
                this.ws.removeEventListener('error', onError);
                this.ws.removeEventListener('close', onClose);
                clearTimeout(t);
                fn(val);
            };

            this.ws.addEventListener('message', onMessage);
            this.ws.addEventListener('error', onError, { once:true });
            this.ws.addEventListener('close', onClose, { once:true });
            const t = setTimeout(onTimeout, timeout);
        });


    }
    send(type, data){
        const p = {
            "type": type,
            "data": data
        }
        this.ws.send(JSON.stringify(p));
    }

}