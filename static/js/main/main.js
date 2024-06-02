function logout(){
    $.removeCookie('token');
    window.location.replace('/')
}