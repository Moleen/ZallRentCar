function change_username_admin(username) {
  $("#btn-change_username_admin").attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/settings/change_username",
    data: {
      username: username,
      new_username: $("#new_username").val(),
    },
    success: function (response) {
      if (response["result"] == "success") {
        $.removeCookie("tokenDashboard");
        $.cookie("tokenDashboard", response["token"], { path: "/" });
        window.location.reload();
      } else if (response["result"] == "failed") {
        $("#helpId").text(response["msg"]);
        $("#helpId").addClass("text-danger");
        $("#helpId").removeClass("text-muted");
        $("#btn-change_username_admin").attr("disabled", false);
      }
    },
  });
}

function change_email(username) {
  $("#btn_email").attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/settings/change_email",
    data: {
      mtd : 'add_email',
      username: username,
      new_email: $("#new_email").val(),
    },
    success: function (response) {
      if (response["result"] == "success") {;
        window.location.reload();
      } else if (response["result"] == "failed") {
        $("#helpId_email").text(response["msg"]);
        $("#helpId_email").addClass("text-danger");
        $("#helpId_email").removeClass("text-muted");
        $("#btn_email").attr("disabled", false);
      }
    },
  });
}
function add_email(username) {
  $("#btn_email").attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/settings/change_email",
    data: {
      mtd : 'add_email',
      username: username,
      new_email: $("#new_email").val(),
    },
    success: function (response) {
      if (response["result"] == "success") {;
        window.location.reload();
      } else if (response["result"] == "failed") {
        $("#helpId_email").text(response["msg"]);
        $("#helpId_email").addClass("text-danger");
        $("#helpId_email").removeClass("text-muted");
        $("#btn_email").attr("disabled", false);
      }
    },
  });
}
function send_verif(username) {
  $("#btn_email").attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/settings/change_email",
    data: {
      mtd : 'send_verif',
      username: username,
    },
    success: function (response) {
      console.log(response);
      if (response["result"] == "success") {;
        window.location.reload();
      } else if (response["result"] == "gagal") {
        toastr.error(response['msg']);
        $("#btn_email").attr("disabled", false);
      }
    },
  });
}
function verif(username) {
  $("#btn_email").attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/settings/change_email",
    data: {
      mtd : 'verif',
      username: username,
      kode : $('#kode').val()
    },
    success: function (response) {
      console.log(response);
      if (response["result"] == "success") {;
        window.location.reload();
      } else if (response["result"] == "gagal") {
        toastr.error(response['msg']);
        $("#btn_email").attr("disabled", false);
      }
    },
  });
}


