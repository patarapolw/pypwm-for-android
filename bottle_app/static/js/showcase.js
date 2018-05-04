$(function(){
    $('#save').click(function(event) {
        $.post('/saveAll');
    });

    $('#logout').click(function(event) {
        window.location.href = '/logout';
    })

    $('#newCategory').keydown(function(event) {
        if(event.keyCode == 13){
            loadPassword($(this).val());
        }
    });
});

function loadPassword(key){
    window.location.href = '/password/' + key;
}
