

$(document).ready(function () {
    $("#reg_phone").inputmask({'placeholder':""});
    $('#showRegister').click(function () {
        $('#loginForm').hide();
        $('#registerForm').show();
    });
    $('#showLogin').click(function () {
        $('#registerForm').hide();
        $('#loginForm').show();
    });
});
// login




// registrasi
$('#form-register').on('submit', function(e){
    e.preventDefault();
    $('#reg_button').attr('disabled',true);
    $.ajax({
        url : '/register',
        type : 'post',
        data : {
            "username" : $('#reg_username').val(),
            "email" : $('#reg_email').val(),
            "password" : $('#reg_password').val(),
            "phone" : $('#reg_phone').val()
        },
        success : function(response){
            if(response['result']  == 'success'){
                $.cookie("token", response["token"], { path: "/" });
                
                window.location.replace('/')
            }else{
                toastr.warning(response['msg'])
                $('#reg_button').removeAttr("disabled");
                return false
            }
        }
    })
})

