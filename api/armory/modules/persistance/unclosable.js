/*
Making the page the browser was hooked from unclosable using infinite `Are you sure you want to close this page` popups.
*/

(function makeUnclosable() {
    /*

    var unclosable_script = document.createElement('script');
    unclosable_script.type = 'text/javascript';
    var code = 'alert("hello world!");';
    unclosable_script.appendChild();
    document.head.appendChild(my_awesome_script);
    */
    function confirmExit() {
        return "You have attempted to leave this page. Are you sure?";
    }
    window.onbeforeunload = confirmExit
})()