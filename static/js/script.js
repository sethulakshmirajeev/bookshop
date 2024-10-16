
document.addEventListener('DOMContentLoaded', function () {
  const searchForm = document.querySelector('.search-form');
  const loginForm = document.querySelector('.login-form-container');
  const closeLoginBtn = document.querySelector('#close-login-btn');
  const loginUrl = "{% url 'login' %}"; // Correctly process Django URL

  // Log to verify the close button exists
  if (closeLoginBtn) {
    console.log('Close button found');
  } else {
    console.log('Close button not found');
  }

  // Toggle search form
  const searchBtn = document.querySelector('#search-btn');
  if (searchBtn && searchForm) {
    searchBtn.onclick = () => {
      searchForm.classList.toggle('active');
    };
  }

  // Toggle login form
  const loginBtn = document.querySelector('#login-btn');
  if (loginBtn && loginForm) {
    loginBtn.onclick = () => {
      loginForm.classList.toggle('active');
    };
  }

  // Close login form
  if (closeLoginBtn && loginForm) {
    closeLoginBtn.addEventListener('click', () => {
      console.log('Close button clicked'); // For debugging
      loginForm.classList.remove('active');
    });
  }

  // Hide forms on scroll
  window.onscroll = () => {
    if (searchForm) {
      searchForm.classList.remove('active');
    }
    const header2 = document.querySelector('.header .header-2');
    if (header2) {
      if (window.scrollY > 80) {
        header2.classList.add('active');
      } else {
        header2.classList.remove('active');
      }
    }
  };

  // Set header state on load
  window.onload = () => {
    const header2 = document.querySelector('.header .header-2');
    if (header2) {
      if (window.scrollY > 80) {
        header2.classList.add('active');
      } else {
        header2.classList.remove('active');
      }
    }
  };

  // Redirect to login if not authenticated
  const isAuthenticated = document.body.getAttribute('data-authenticated') === 'true';
  const loginRedirectElements = document.querySelectorAll('.icons a, .navbar a, .content a, .content form.d-inline, .box a, .quick-link-home, .quick-link-shop, .quick-link-about, .quick-link-contact');

  loginRedirectElements.forEach(element => {
    element.addEventListener('click', function (event) {
      if (!isAuthenticated) {
        event.preventDefault();
        if (loginForm) {
          loginForm.classList.add('active'); // Show the login form
        }
        window.history.pushState({}, '', loginUrl); // Change the URL to the login URL
      }
    });
  });
});
//Redirect to login if not authenticated
// document.addEventListener('DOMContentLoaded', function () {
//   const isAuthenticated = "{{ request.user.is_authenticated|yesno:'true,false' }}";
//   const loginRedirectElements = document.querySelectorAll('.icons a, .navbar a');

//   loginRedirectElements.forEach(element => {
//       element.addEventListener('click', function (event) {
//           if (isAuthenticated === 'false') {
//               event.preventDefault();
//               window.location.href = "{% url 'login' %}";
//           }
//       });
//   });
// });

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