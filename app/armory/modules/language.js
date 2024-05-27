/*
Module to return language of the hooked browser
*/

(function getLanguage() {
    return navigator.language || navigator.userLanguage; 
})()