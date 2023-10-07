// function to show password
function showPassword() {
    var x = document.getElementById("password");
    if (x.type == "password") {
        x.type = "text";
        document.getElementById("passCheckbox").checked = true;
    } else {
        x.type = "password";
        document.getElementById("passCheckbox").checked = false;
    }
    var y = document.getElementById("signUpPassword");
    if (y.type == "password") {
        y.type = "text";
        document.getElementById("signUpPassCheckbox").checked = true;
    } else {
        y.type = "password";
        document.getElementById("signUpPassCheckbox").checked = false;
    }
}

// Function to give warning for vaild password and if password are not macthing after clicking submit button
$(function validatePassword() {
    $("#btnSubmit").click(function validatePassword() {
        var password = $("#signUpPassword").val();
        var passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[~!@#$%^&*()\-_=+{};:,<.>\/?]).{8,20}$/;
        if (passwordRegex.test(password)) {
            return true;
        }
        else{
            alert("Password must contain at least 1 capital letter,1 small letter, 1 number \nand 1 special character ([~!@#$%^&*()\-_=+{};:,<.>\/?]) and length must be between 8 to 20.");
            return false
        }
    });
});


// Show signIn tab
function showSignInTab() {
    $("#signUpBox").fadeOut("slow", function () {
        $("#signInBox").fadeIn("slow");
    });
}

// Show SignUp tab
function showSignUpTab() {
    $("#signInBox").fadeOut("slow", function () {
        $("#signUpBox").fadeIn("slow");
    });
}