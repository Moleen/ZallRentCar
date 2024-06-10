
function logout(){
    Swal.fire({
        position: "top",
        text: "Anda yakin untuk logout?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes",
      }).then((result) => {
        if (result.isConfirmed) {
            $.removeCookie('token');
            localStorage.setItem('logout','true')
            window.location.replace('/')
        } 
      });
}

$(document).ready(function(){
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
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
    };
    $('[data-target="currency"]').each(function(){
        $(this).text(new Intl.NumberFormat("id",{
            style:'currency',
            currency:"IDR",
            maximumFractionDigits:0
        }).format(parseInt($(this).text())))
    })

// ALERT SETELAH LOGOUT
    if(localStorage.getItem('logout') == 'true'){
        toastr.success('Berhasil logout');
        localStorage.removeItem('logout')
    }
// ALERT SETELAH LOGIN
    if(localStorage.getItem('login') == 'true'){
        toastr.success('Berhasil Login');
        localStorage.removeItem('login')
    }
})