function logout(){
    window.location.replace('/')
    $.removeCookie('token');
}

$(document).ready(function(){
    $('[data-target="currency"]').each(function(){
        $(this).text(new Intl.NumberFormat("id",{
            style:'currency',
            currency:"IDR",
            maximumFractionDigits:0
        }).format(parseInt($(this).text())))
    })
})