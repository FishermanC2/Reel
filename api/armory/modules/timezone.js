/*
Module to retrieve timezone of the hooked browser
*/

(function getTimezone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
})()