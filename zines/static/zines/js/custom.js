$(document).ready(function() {

    // update publish value before submitting
    $('#publish').click(function(e) {
        e.preventDefault();
        $('#id_published').val("True");
        publish();
    });
    $('#unpublish').click(function(e) {
        e.preventDefault();
        $('#id_published').val("False");
        publish();
    });

    // #editor
    $('div.label').removeClass('show');
    $('#editor').hover(function() {
        $('div.label').addClass('show');
    }, function() {
        $('div.label').removeClass('show');
    });

    // search
    $('#search').click(function(e) {
        e.preventDefault();
        $('#search input[type=text]').addClass('show');
        $('#search input[type=text').focus();
    });
    $('#search input[type=text').blur(function(e) {
        $('#search input[type=text]').removeClass('show');
    });
});