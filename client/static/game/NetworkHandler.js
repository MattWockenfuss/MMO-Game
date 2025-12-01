export default class NetworkHandler{
    constructor(handler, ipport){
        this.handler = handler;
        this.ws = new WebSocket(`ws://${ipport}/`);
        this.inbound = [];

        this._switchingClose = false;


        
        this.ws.onopen = () => {
            console.log("Connected to World Server!");
        }
        this.ws.onclose = (event) => {
            const isSwitchClose = event.code === 4001 || event.reason.startsWith("Switching");

            console.log("[NetworkHandler] onclose", event.code, event.reason, "switchingClose =", this._switchingClose);
            if(!this._switchingClose && !isSwitchClose && this.handler != null){
                this.handler.game.stop(event);
            }
        }
        this.ws.onmessage = (event) => {
            //console.log(event.data);
            try {
                const packet = JSON.parse(event.data);
                //console.log(`${packet.type} : ${JSON.stringify(packet.data)}`);
                this.inbound.push(packet);
            } catch (error){
                console.error("[ERROR] Reading Packet => " + event.data);
                console.error(`->    ${error}`);
            }
        }
        this.ws.onerror = (event) => {
            console.error(`[ERROR] ${event}`);
        }

    }


    close(code = 1000, reason = 'Client Quit'){
        this._switchingClose = false;
        console.log("[NetworkHandler] switchclose called, readyState =", this.ws.readyState);
        try {
            this.ws.close(code, reason);
        } catch {
            console.log(`ERROR TRYING TO CLOSE SOCKET`);
        }
    }

    switchclose(){
        this._switchingClose = true;
        //this function is called to close the current websocket so we can open another as we are switching worlds
        try {
            this.ws.close(1000, 'Switching Server!');
        } catch {
            console.log(`ERROR TRYING TO CLOSE SOCKET`);
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