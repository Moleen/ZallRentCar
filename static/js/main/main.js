function logout(){
    window.location.replace('/')
    $.removeCookie('token');
}