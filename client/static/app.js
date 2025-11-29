import NetworkHandler from "./game/NetworkHandler.js";
import gameloop from "./GameLoop.js";

console.log("Loaded app.js")

const colorInput = document.querySelector('.color');
const colorValue = document.getElementById('cv');

function updateColor() {
    colorValue.textContent = colorInput.value;
    colorValue.style.color = colorInput.value;
}

colorInput.addEventListener('input', updateColor);

updateColor();






const ipinput = document.querySelector('.ippicker');
const ipbox = document.getElementById('customServer');


function toggleCustom() {
    const ipport = form.choices.value;
    if (ipport === 'Custom') {
        ipbox.style.display = 'inline-block';
    } else {
        ipbox.style.display = 'none';
    }
}
ipinput.addEventListener('input', toggleCustom);


const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    //prevents the sending the user to /submitLogin and sending it to backend
    //also the auto transfer to new page
    
    let ipport = form.choices.value;

    if (ipport === 'Custom') {
        ipport = ipbox.value;
    }
    console.log(`IPPORT: ${ipport}`);
    const data = {
        "username": form.username.value,
        "password": form.password.value
    };
    //alright we want to send this to the comms server? so 
    console.log(data);
    
    const commsWS = new NetworkHandler(ipport);
    await commsWS.waitForOpen();
    commsWS.send("AUTH_REQ", data);

    const AUTH_REP = await commsWS.waitForLoginVerify(m => m.data.AUTH === 'AUTH_OK' || m.data.AUTH === 'AUTH_FAILED', 5000);
    console.log(JSON.stringify(AUTH_REP));
    //We have recieved a reply from the comms server! we are either authenticated or we arent, if we are we got an IP to connect to
    //lets close the old connection!

    commsWS.close();



    //okay
    if (AUTH_REP.data.AUTH === 'AUTH_OK'){
        //then we were authenticated!, lets connect to the world server!
        let worldserverIP = AUTH_REP.data.IP;

        const worldServerWS = new NetworkHandler(worldserverIP);
        await worldServerWS.waitForOpen();
        
        //we want to send the world server our data, username and color

        var p = {
            "username": form.username.value,
            "color": form.color.value
        }
        console.log(p)
        worldServerWS.send("login", p);

        game.hidden = false;
        loginPage.hidden = true;
        
        gameloop.init(worldServerWS, form.username.value, form.color.value);

    }else{
        //then let them know they failed authentication!
    }


    
    // const net = new NetworkHandler(ipport);
    // await net.waitForOpen();

    // //console.log("sending");
    // net.send("login", data);
    // //alright, now what, well, we need to wait until we receive the login verified packet, and if so, read the world data, otherwise, close the connection and we can try again
    
    // const reply = await net.waitForLoginVerify(m => m.data.auth === 'ok' || m.data.auth === 'fail', 5000);
    // console.log(JSON.stringify(reply));

    // const game = document.getElementById("game");
    // const loginPage = document.getElementById("loginPage");

    // if (reply.data.auth === 'ok') {
    //     //then move to world server(hide login)
    //     //start game loop and read world
    //     console.log("Authentication Successful: Logging In!");
    //     

    //     //alright, now we need to start the game loop, passing through the
    //     //network handler
    //     
        
    // } else {
    //     //Say login was unsuccessful and hopefully why
    // }



});