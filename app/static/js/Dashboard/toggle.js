// showing and hiding of sidebar 

$(document).ready(function(){
  
  const sideMenu = document.querySelector("aside");
  const menuBtn = document.querySelector("#menu-btn");
  const closeBtn = document.querySelector("#close-btn");

  menuBtn.addEventListener('click', () => {
     sideMenu.style.display = 'block';
  });
  
  closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
  })

  $(window).resize(function() {
    if ($(window).width() >= 600) {
      $(menuBtn).hide();
      $(sideMenu).show();
    } else {
      $(menuBtn).show();
      $(sideMenu).hide();
    }
  });

});