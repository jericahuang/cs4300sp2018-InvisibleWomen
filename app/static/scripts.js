$(document).ready(function () {
    console.log("ready!");

    function convertName(name) {
        var replaced = name.split(' ').join('+');
        return replaced;
    }

    $("button").click(function () {
        $("#bottomcorner").fadeOut();
    });

    $('.tip').tipr();
});