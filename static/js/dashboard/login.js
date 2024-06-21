function loginDashboard() {
  var username = $("input[name=username]").val();
  var password = $("input[name=password]").val();
  if (password == "" && username == "") {
    alert("Please enter your password and username");
  } else if (password == "") {
    alert("Please enter your password");
  } else {
    $.ajax({
      url: "/dashboard-login",
      type: "POST",
      data: {
        username: username,
        password: password,
      },
      success: function (response) {
        if (response["result"] == "success") {
          alert(`status  :${response["result"]} login berhasil`);
          $.cookie("tokenDashboard", response["token"], { path: "/" });
          window.location.replace("/dashboard");
        } else {
          alert("login gagal");
        }
      },
    });
  }
}

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // ID pengguna
  console.log('Nama: ' + profile.getName()); // Nama lengkap pengguna
  console.log('Email: ' + profile.getEmail()); // Email pengguna
  // Di sini Anda dapat menambahkan logika untuk menangani respons dari Google Sign-In
}
