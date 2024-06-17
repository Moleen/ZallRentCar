//login js

$(document).ready(function () {
  $("#reg_phone").inputmask({ placeholder: "" });
  $("#showRegister").click(function () {
    $("#loginForm").hide();
    $("#registerForm").show();
  });
  $("#showLogin").click(function () {
    $("#registerForm").hide();
    $("#loginForm").show();
  });
});

// login
$("#form-login").on("submit", function (e) {
  e.preventDefault();
  redirect = $("#login_button").attr("data-redirect");
  username = $("#login_username").val();
  pw = $("#login_password").val();
  // redirect default
  if (redirect == "") {
    redirect = "/";
  }
  $("#login_button").attr("disabled", true);
  $.ajax({
    url: "/login",
    type: "post",
    data: {
      username: username,
      password: pw,
    },
    success: function (response) {
      if (response["result"] == "success") {
        $.cookie("tokenMain", response["token"], { path: "/" });
        localStorage.setItem("login", "true");
        window.location.replace(redirect);
      } else {
        toastr.warning(response["msg"]);
        $("#login_button").attr("disabled", false);
        return false;
      }
    },
    error: function (xhr, status, error) {
      // Ketika permintaan gagal
      console.error(xhr.responseText); // Menampilkan pesan error di konsol
      alert("Terjadi kesalahan saat proses login."); // Menampilkan pesan kesalahan kepada pengguna
    },
  });
});

// registrasi
$("#form-register").on("submit", function (e) {
  e.preventDefault();
  $("#reg_button").attr("disabled", true);
  $.ajax({
    url: "/register",
    type: "post",
    data: {
      username: $("#reg_username").val(),
      email: $("#reg_email").val(),
      password: $("#reg_password").val(),
      phone: $("#reg_phone").val(),
    },
    success: function (response) {
        $("#username_status").removeClass("text-danger text-success");
        $("#pw_status").removeClass("text-danger text-success");
        $("#email_status").removeClass("text-danger text-success");
        $("#phone_status").removeClass("text-danger text-success");

      if (response["result"] == "success") {
        $.cookie("tokenMain", response["token"], { path: "/" });
        localStorage.setItem("login", "true");
        window.location.replace(redirect);

      } else if (response["result"] == "ejected") {
        $("#username_status").text(response["msg"]);
        $("#username_status").addClass("text-danger");
        $("#reg_button").attr("disabled", false);

      } else if (response["result"] == "ejectedPW") {
        $("#pw_status").text(response["msg"]);
        $("#pw_status").addClass("text-danger");
        $("#reg_button").attr("disabled", false);

      } else if (response["result"] == "ejectedEmail") {
        $("#email_status").text(response["msg"]);
        $("#email_status").addClass("text-danger");
        $("#reg_button").attr("disabled", false);

      } else if (response["result"] == "ejectedPhone") {
        $("#phone_status").text(response["msg"]);
        $("#phone_status").addClass("text-danger");
        $("#reg_button").attr("disabled", false);
      }
    },
  });
});

// cek username
$("#reg_username").on("change", function () {
  $.ajax({
    url: "/api/check_username",
    type: "post",
    data: {
      username: $("#reg_username").val(),
    },
    success: function (response) {
      $("#username_status").removeClass("text-success text-danger");
      if (response["result"] == "available") {
        $("#username_status").text("Username available");
        $("#username_status").addClass("text-success");
      } else if (response["result"] == "ejected") {
        $("#username_status").text(response["msg"]);
        $("#username_status").addClass("text-danger");
      }
    },
  });
});
