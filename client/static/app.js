import NetworkHandler from "./game/NetworkHandler.js";
import gameloop from "./GameLoop.js";

console.log("Loaded app.js")







const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();//prevents the sending the user to /submitLogin and sending it to backend
    //also the auto transfer to new page
    
    const ipport = form.ipport.value;

    const data = {
        "username": form.username.value,
        "password": form.password.value,
        "color": form.color.value
        };

    //alright so we can accept user input, now what do we want to do
    //send it to the world server for now, or straight to the data server?, and transfer the user to the game if they get approved?

    console.log(data);
    const net = new NetworkHandler(ipport);
    await net.waitForOpen();
    console.log("sending");
    net.send("login", data);
    //alright, now what, well, we need to wait until we receive the login verified packet, and if so, read the world data, otherwise, close the connection and we can try again
    
    const reply = await net.waitForLoginVerify(m => m.data.auth === 'ok' || m.data.auth === 'fail', 5000);
    console.log(`REPLY:    ${JSON.stringify(reply)}`);

    const game = document.getElementById("game");
    const loginForm = document.getElementById("login");

    if (reply.data.auth === 'ok') {
        //then move to world server(hide login)
        //start game loop and read world
        console.log("Authentication Successful: Logging In!");
        game.hidden = false;
        loginForm.hidden = true;

        //alright, now we need to start the game loop, passing through the
        //network handler
        gameloop.init(net, form.username.value, form.color.value);
        
    } else {
        //Say login was unsuccessful and hopefully why
    }



});