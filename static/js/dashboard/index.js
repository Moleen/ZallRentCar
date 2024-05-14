function logout() {
    $.removeCookie('token', { path: '/' });
    window.location.reload()
}