window.addEventListener("scroll", function(){

  var header = document.querySelector("header");
  header.classList.toggle("sticky", window.scrollY > 0);
})

// MENU TOGGLE 

function toggleMobileNavigation() {
    var element = document.getElementById("mobile-navigation");

    if (element.classList.contains("mobile-navigation__open")) {
      element.classList.remove("mobile-navigation__open");
    } else {
      element.classList.add("mobile-navigation__open");
    }
  }