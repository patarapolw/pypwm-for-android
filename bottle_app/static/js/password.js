$(function(){
    $('#newPassword').click(function(event) {
        $.post('/newPassword', {'name': $('#name').val()}, function(data){
            if(data !== '0'){
                $('#password').val(data.password);
                $('#note').text(data.note);
            } else {
                window.location.href = '/';
            }
        })
    });

    $('.lastKey').on('input', function(){
        var $thisVal = $(this).val();
        if($thisVal !== ''){
            $('.lastValue').attr('disabled', false).attr('name', $thisVal);
        } else {
            $('.lastValue').attr('disabled', true).removeAttr('name');
        }
    })

    $('.lastValue').keydown(function(event) {
        if(event.keyCode == 13){
            $('.newKey').removeClass('lastKey');
            $('.newValue').removeClass('lastValue');
            $('#newItems').append('<div class="row mt-3"><div class="row"><input type="text" placeholder="New key" class="newKey lastKey form-control"/></div><div class="row"><input type="text" class="newValue lastValue form-control" disabled/></div>');
        }
    });

    $('#save').click(function(){
        $.post('/saveOne', $('#passwordForm').serialize());
    })

    $('#reset').click(function(){
        $('#newItems').html('<div class="row mt-3"><div class="row"><input type="text" placeholder="New key" class="newKey lastKey form-control"/></div><div class="row"><input type="text" class="newValue lastValue form-control" disabled/></div>');
    })

    $('#delete').click(function(){
        $.post('/deleteOne', {name: $('#name').val()});
    });

    $('#exit').click(function(event) {
        window.location.href = '/showcase';
    });

    $('.oldKey').each(function(index, el) {
        $(this).text(toTitleCase($(this).text()));
    });
});

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
