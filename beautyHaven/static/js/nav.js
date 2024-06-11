let currentIndex = 0;
const slides = document.querySelectorAll('.carousel-inner img');

function updateSlides() {
    slides.forEach((slide, index) => {
        slide.classList.remove('active');
        slide.style.zIndex = index === currentIndex ? 2 : 1;
        if (index === currentIndex) {
            slide.classList.add('active');
        }
    });
}

function nextSlide() {
    slides[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % slides.length;
    slides[currentIndex].classList.add('active');
}

function previousSlide() {
    slides[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    slides[currentIndex].classList.add('active');
}

window.addEventListener('scroll', function() {
    var header = document.getElementById('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});
