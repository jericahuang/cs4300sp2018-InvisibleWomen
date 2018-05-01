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

    var list = ["e.g. worked at NASA", "e.g. is a Cornell professor", "e.g. researched cancer", "e.g. won the Nobel Prize", "e.g. makes video games", "e.g. is a French physicist", "e.g. is a lesbian"],
        r = Math.floor(Math.random() * list.length);
    $('#input').prop('placeholder', list[r]);
});