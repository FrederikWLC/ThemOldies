
function message(status, shake=false, id="") {
  if (shake) {
    $("#"+id).effect("shake", {direction: "right", times: 2, distance: 8}, 250);
  } 
  document.getElementById("feedback").innerHTML = status;
  $("#feedback").show().delay(2000).fadeOut();
}
  
 $(document).on("click", "#register-button", function() {
   console.log("REGISTER");
    $.post({
      type: "POST",
      url: "/register",
      data: {"username": $("#register-user").val(), 
             "password": $("#register-pass").val(), 
             "email": $("#register-mail").val()},
      success(response) {
        var status = JSON.parse(response)["status"];
        if (status === "Successfully registered") { location.reload(); }
        else{message(status, true, "register-box");}
      }
    });
  });

    $(document).on("click", "#login-button", function() {
      console.log("LOGIN");
    $.post({
      type: "POST",
      url: "/login",
      data: {"username": $("#login-user").val(), 
             "password": $("#login-pass").val()},
      success(response) {
          var status = JSON.parse(response)["status"];
          if (status === "Successfully logged in") { location.reload(); }
          else{message(status, true, "login-box");}
          

    }});
  });