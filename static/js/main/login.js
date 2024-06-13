//login js


$(document).ready(function () {
    $("#reg_phone").inputmask({ 'placeholder': "" });
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
$('#form-login').on('submit', function(e){
    e.preventDefault();
    redirect = $('#login_button').attr('data-redirect')

    // redirect default
    if (redirect == ''){
        redirect = '/';
    }
    $('#login_button').attr('disabled',true);
    $.ajax({
        url : '/login',
        type : 'post',
        data : {
            "username" : $('#login_username').val(),
            "password" : $('#login_password').val(),
        },
        success : function(response){
            if(response['result']  == 'success'){
                $.cookie("tokenMain", response["token"], { path: "/" });
                localStorage.setItem('login','true')
                window.location.replace(redirect)
            }else{
                toastr.warning(response['msg'])
                $('#login_button').attr("disabled",false);
                return false
            }
        },
        error: function (xhr, status, error) { // Ketika permintaan gagal
            console.error(xhr.responseText); // Menampilkan pesan error di konsol
            alert('Terjadi kesalahan saat proses login.'); // Menampilkan pesan kesalahan kepada pengguna
        }
    })
})

// registrasi
$('#form-register').on('submit', function (e) {
    e.preventDefault();
    $('#reg_button').attr('disabled', true);
    $.ajax({
        url: '/register',
        type: 'post',
        data: {
            "username": $('#reg_username').val(),
            "email": $('#reg_email').val(),
            "password": $('#reg_password').val(),
            "phone": $('#reg_phone').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie("token", response["token"], { path: "/" });
                window.location.replace('/')
            } else {
                alert(response['msg']);
                $('#reg_button').removeAttr("disabled");
                return false
            }
        }
    })
})

