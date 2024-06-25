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

$("#lupa_password").on("click", function () {
  $.ajax({
    url: "/forgot_pass",
    type: "post",
    data: {
      from: "admin",
    },
    success: function (response) {
      if (response["result"] == "success") {
        alert("Password reset link has been sent to your email");
      } else {
        alert("Failed to send password reset link");
      }
    },
  });
});

