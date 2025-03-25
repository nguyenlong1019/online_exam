let currentIndex = 0;

function showSlide(index) {
    const slides = document.querySelectorAll(".slide");
    slides.forEach(slide => {
        slide.classList.remove("active");
    });

    slides[index].classList.add("active");
}

function nextSlide() {
    const slides = document.querySelectorAll('.slide');
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
}

function prevSlide() {
    const slides = document.querySelectorAll('.slide');
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
}

showSlide(currentIndex);