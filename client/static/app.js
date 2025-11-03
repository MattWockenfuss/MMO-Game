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





const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    //prevents the sending the user to /submitLogin and sending it to backend
    //also the auto transfer to new page
    
    const ipport = form.choices.value;

    const data = {
        "username": form.username.value,
        "password": form.password.value,
        "color": form.color.value
        };

    //alright so we can accept user input, now what do we want to do
    //send it to the world server for now, or straight to the data server?, and transfer the user to the game if they get approved?
    
    //alright so we need to change this to first connect to comms server, and then if authenticated, close, and open another connection with world server
    //so we need the world server to know that the player is authenticated, and we also need all of the world servers to keep session keeps synced (2 players on different
    //worlds cant have the same UUID)



    /*
        okay, so the player connects to the comms server, says their username, password and color.
        comms server: sends data server player stuff, waits for response
        data server: checks database.
        comms server: receives authentication from dataserver
        comms server: generates a UUID for them, and stores it in a list of players, also a 16 temp password
        comms server: sends the player starting world and position, also its 16 digit temp password
        comms server: sends the appropriate world the username and 16 digit temp password, so the world server knows
        player: recieves data, closes websocket with comms server, connects to the IP given by the comms server and sends its temp-password
    
    
    
    
    */




    console.log(data);
    const net = new NetworkHandler(ipport);
    await net.waitForOpen();
    //console.log("sending");
    net.send("login", data);
    //alright, now what, well, we need to wait until we receive the login verified packet, and if so, read the world data, otherwise, close the connection and we can try again
    
    const reply = await net.waitForLoginVerify(m => m.data.auth === 'ok' || m.data.auth === 'fail', 5000);
    console.log(JSON.stringify(reply));

    const game = document.getElementById("game");
    const loginPage = document.getElementById("loginPage");

    if (reply.data.auth === 'ok') {
        //then move to world server(hide login)
        //start game loop and read world
        console.log("Authentication Successful: Logging In!");
        game.hidden = false;
        loginPage.hidden = true;

        //alright, now we need to start the game loop, passing through the
        //network handler
        gameloop.init(net, form.username.value, form.color.value);
        
    } else {
        //Say login was unsuccessful and hopefully why
    }



});