let navbar = document.querySelector('.header .navbar');
let accountBox = document.querySelector('.header .account-box');

document.querySelector('#menu-btn').onclick = () =>{
    navbar.classList.toggle('active');
    accountBox.classList.remove('active');

}

document.querySelector('#user-btn').onclick = () =>{
    accountBox.classList.toggle('active');
    navbar.classList.remove('active');

}

window.onscroll = () =>{
    navbar.classList.remove('active');
    accountBox.classList.remove('active');

}

var swiper = new Swiper(".books-slider", {
    loop: true,
    centeredSlides: true,
    autoplay:{
        delay:2000,
        disableOnInterection: false,
    },

    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      1024: {
        slidesPerView: 3,
      },
    },
  });

  var swiper = new Swiper(".featured-slider", {
    spaceBetween:10,
    loop: true,
    centeredSlides: true,
    autoplay:{
        delay:2000,
        disableOnInterection: false,
    },
    Navigation:{
        nextE1: ".swiper-button-next",
        prevE1: ".swiper-button-prev",
    },
    
    breakpoints: {
      0: {
        slidesPerView: 1,
      },
      450: {
        slidesPerView: 2,
      },
      768: {
        slidesPerView: 3,
      },
      1024: {
        slidesPerView: 4,
      },
    },
  });