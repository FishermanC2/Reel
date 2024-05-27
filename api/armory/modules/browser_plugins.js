/*
Module to return installed browser plugins for assessing vulnerablities
*/

(function getBrowserPlugins() {
    let plugins = [];
    for (let i = 0; i < navigator.plugins.length; i++) {
        plugins.push(navigator.plugins[i].name);
    }
    return plugins.join(', ');
})()