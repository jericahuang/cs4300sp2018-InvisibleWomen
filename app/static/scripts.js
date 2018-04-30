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

    var list = ["e.g. worked at NASA", "e.g. found a cure", "e.g. is a Cornell professor", "e.g. researched cancer", "e.g. won the Nobel Prize", "e.g. makes video games", "e.g. is a French physicist"],
        r = Math.floor(Math.random() * list.length);
    $('#input').prop('placeholder', list[r]);

    
});