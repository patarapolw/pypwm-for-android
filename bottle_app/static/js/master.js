$(function(){
    toastr.options = {
      "closeButton": false,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-bottom-center",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
    }

    $('#masterPassword').keydown(function(event) {
        if(event.keyCode == 13){
            $.post('/createVault', {"masterPassword": $(this).val()}, function(data){
                if(data === '0'){
                    toastr["error"]("Wrong password!")
                } else if(data === '1') {
                    window.location.href = '/showcase'
                } else {
                    console.log(data);
                }
            });
        }
    });
});
