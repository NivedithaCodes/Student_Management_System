// ===== JavaScript for Popup =====
document.addEventListener("DOMContentLoaded", function () {
    const loginBtn = document.getElementById("btn-login");
    const loginBtn2 = document.getElementById("btn-login2");
    const loginPopup = document.getElementById("loginPopup");
    const signupPopup = document.getElementById("signupPopup");
  
    // Open login popup from navbar
    if (loginBtn) {
      loginBtn.addEventListener("click", function () {
        loginPopup.style.display = "flex";
      });
    }
  
    // Open login popup from home section button
    if (loginBtn2) {
      loginBtn2.addEventListener("click", function () {
        loginPopup.style.display = "flex";
      });
    }
  
    // Global function for closing popup
    window.closePopup = function (id) {
      document.getElementById(id).style.display = "none";
    };
  
    // Global function for switching popup
    window.switchPopup = function (closeId, openId) {
      document.getElementById(closeId).style.display = "none";
      document.getElementById(openId).style.display = "flex";
    };
  
    // Close popup when clicking outside
    window.onclick = function (event) {
      const popups = [loginPopup, signupPopup];
      popups.forEach((popup) => {
        if (event.target === popup) popup.style.display = "none";
      });
    };
  });
 s  