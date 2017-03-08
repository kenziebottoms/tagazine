function initQuill() {
    var quill = new Quill('#quill', {
        theme: 'snow'
    });
    $('.ql-editor').focus(function() {
        console.log('focus');
        $('.ql-toolbar').addClass('active');
        $('.ql-container').addClass('active');
    });
    $('.ql-editor').blur(function() {
        console.log('focus');
        $('.ql-toolbar').removeClass('active');
        $('.ql-container').removeClass('active');
    });
}
function updateQuillHiddenInput(hiddenInputID) {
    $input = $('#'+hiddenInputID);
    $input.val($('#quill>div')[0].innerHTML);
}
function addTag(value, label) {
    if ($('#tag_list .tag[data-id='+value+']').length == 0) {
        $('#tag_list').append('<a class="tag" data-id="'+value+'">'+label+'</a>');
    }
}
function updateTags() {
    // tags field
    var tags = []
    $('#tag_list .tag').each(function() {
        tags.push($(this).data('id'));
    });
    $('#id_tags').val(tags);
    console.log(tags);
}