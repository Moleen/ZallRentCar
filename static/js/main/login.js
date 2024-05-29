document.getElementById('showRegister').addEventListener('click', function () {
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('registerForm').classList.add('active');
});

document.getElementById('showLogin').addEventListener('click', function () {
    document.getElementById('registerForm').classList.remove('active');
    document.getElementById('loginForm').classList.add('active');
});

$('#form-register').on('submit', function(){
    $('#reg_button').attr('disabled','disabled');
    $.ajax({
        url : '/reg',
        type : 'post',
        data : {
            "username" : $('#reg_username').val(),
            "email" : $('#reg_email').val(),
            "password" : $('#reg_password').val(),
            "phone" : $('#reg_phone').val()
        },
        success : function(data){
            alert(data['username']);
            window.location.replace('/')
        }
    })
})

$("#reg_phone").inputmask({'placeholder':""});