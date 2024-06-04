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


// Login//
$(document).ready(function () {
    // Fungsi untuk menangani submit form login
    $('#form-login').on('submit', function (e) {
        e.preventDefault(); // Mencegah form untuk melakukan submit secara default

        // Mengambil nilai email dan password dari input
        var email = $('#loginEmail').val();
        var password = $('#loginPassword').val();

        // Mengirim data login ke server menggunakan AJAX
        $.ajax({
            url: '/login', // URL endpoint untuk login
            type: 'post', // Metode HTTP POST
            data: {
                "email": email, // Menggunakan "email" sebagai nama variabel
                "password": password
            },
            success: function (response) { // Ketika permintaan berhasil
                if (response['token']) { // Jika token diterima dari server
                    window.location.replace('/'); // Mengarahkan pengguna ke halaman utama
                } else { // Jika token tidak diterima dari server
                    alert('Login gagal. Harap coba lagi.'); // Menampilkan pesan kesalahan umum
                }
            },
            error: function (xhr, status, error) { // Ketika permintaan gagal
                console.error(xhr.responseText); // Menampilkan pesan error di konsol
                alert('Terjadi kesalahan saat proses login.'); // Menampilkan pesan kesalahan kepada pengguna
            }
        });
    });
});



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

