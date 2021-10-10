




var navbar = document.querySelector("nav");
var navbarlink1 = document.getElementById("navlink1");
var navbarlink2 = document.getElementById("navlink2");
var navbarlink3 = document.getElementById("navlink3");
var navbarlink4 = document.getElementById("navlink4");
var navbarlink5 = document.getElementById("navlink5");
var navbarbutton = document.getElementById("join-button");
var navbarbuttontext = document.getElementById("join-button-text");

window.onscroll = function () {
  // pageYOffset or scrollY
  if (window.pageYOffset > 200) {
    navbar.classList.add("scrolled");
    navbarlink1.classList.add("scroll");
    navbarlink2.classList.add("scroll");
    navbarlink3.classList.add("scroll");
    navbarlink4.classList.add("scroll");
    navbarlink5.classList.add("scroll");
    navbarbutton.classList.add("scroll");
    navbarbuttontext.classList.add("scroll");
  } else {
    navbar.classList.remove("scrolled");
    navbarlink1.classList.remove("scroll");
    navbarlink2.classList.remove("scroll");
    navbarlink3.classList.remove("scroll");
    navbarlink4.classList.remove("scroll");
    navbarlink5.classList.remove("scroll");
    navbarbutton.classList.remove("scroll");
    navbarbuttontext.classList.remove("scroll");
  }
};
