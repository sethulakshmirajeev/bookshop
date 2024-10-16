document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.querySelector('.search-form');
    const loginForm = document.querySelector('.login-form-container');
    const searchBtn = document.querySelector('#search-btn');
    const wishlistIcon = document.querySelector('.fa-heart');
    const cartIcon = document.querySelector('.fa-shopping-cart');
    const loginBtn = document.querySelector('#login-btn');
    const logoutBtn = document.querySelector('#logout-btn');
    const closeLoginBtn = document.querySelector('#close-login-btn');

    // Sample flag to indicate if the user is logged in (this should ideally be set dynamically from your server)
    let loggedIn = false; // Change this based on actual login status

    // Function to update the visibility of elements based on login status
    function updateUI() {
        if (loggedIn) {
            searchForm.style.display = 'block';
            wishlistIcon.style.display = 'inline';
            cartIcon.style.display = 'inline';
            loginBtn.style.display = 'none';
            logoutBtn.style.display = 'inline';
        } else {
            searchForm.style.display = 'none';
            wishlistIcon.style.display = 'none';
            cartIcon.style.display = 'none';
            loginBtn.style.display = 'inline';
            logoutBtn.style.display = 'none';
        }
    }

    // Update UI on page load
    updateUI();

    // Event listeners
    searchBtn.onclick = () => {
        searchForm.classList.toggle('active');
    };

    loginBtn.onclick = () => {
        loginForm.classList.toggle('active');
    };

    closeLoginBtn.onclick = () => {
        loginForm.classList.remove('active');
    };

    logoutBtn.onclick = () => {
        // Handle logout logic here
        loggedIn = false; // Set loggedIn to false or update this flag based on actual logout logic
        updateUI();
    };

    window.onscroll = () => {
        searchForm.classList.remove('active');
        if (window.scrollY > 80) {
            document.querySelector('.header .header-2').classList.add('active');
        } else {
            document.querySelector('.header .header-2').classList.remove('active');
        }
    };

    window.onload = () => {
        if (window.scrollY > 80) {
            document.querySelector('.header .header-2').classList.add('active');
        } else {
            document.querySelector('.header .header-2').classList.remove('active');
        }
    };

    var swiper = new Swiper(".books-slider", {
        loop: true,
        centeredSlides: true,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
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
        spaceBetween: 10,
        loop: true,
        centeredSlides: true,
        autoplay: {
            delay: 2000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
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
});
