$(document).ready(function () {
    console.log("ready!");

    function convertName(name) {
        var replaced = name.split(' ').join('+');
        return replaced;
    }

    $('.tip').tipr();

    var list = ["e.g. researches natural language processing", "e.g. researched plant breeding", "e.g. is a pioneer", "e.g. worked at NASA", "e.g. is a Cornell professor", "e.g. researched cancer", "e.g. won the Nobel Prize", "e.g. makes video games", "e.g. is a French physicist", "e.g. is a lesbian", "e.g. invented the compiler", "e.g. worked during World War II", "e.g. is an American computer scientist", "e.g. is an entrepreneur", "e.g. was born in New York City", "e.g. does research on group theory", "e.g. worked at IBM", "e.g. was an inventor"],
        r = Math.floor(Math.random() * list.length);
    $('#input').prop('placeholder', list[r]);
});