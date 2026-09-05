// Carrousel photo réutilisable : fonctionne pour toutes les sections .hero-slider
// présentes sur la page (page d'accueil + en-têtes des autres pages).
(function () {
    function initSlider(root) {
        var slides = root.querySelectorAll('.hero-slide');
        var dotsWrap = root.parentElement.querySelector('.hero-dots');
        var dots = dotsWrap ? dotsWrap.querySelectorAll('.hero-dot') : [];
        var prevBtn = root.parentElement.querySelector('.hero-arrow.prev');
        var nextBtn = root.parentElement.querySelector('.hero-arrow.next');
        var current = 0;
        var timer = null;
        var AUTOPLAY_MS = 6000;

        if (!slides.length) return;

        function show(index) {
            slides[current].classList.remove('active');
            if (dots[current]) dots[current].classList.remove('active');
            current = (index + slides.length) % slides.length;
            slides[current].classList.add('active');
            if (dots[current]) dots[current].classList.add('active');
        }
        function next() { show(current + 1); }
        function prev() { show(current - 1); }
        function restartAutoplay() {
            if (timer) clearInterval(timer);
            if (slides.length > 1) timer = setInterval(next, AUTOPLAY_MS);
        }

        if (prevBtn) prevBtn.addEventListener('click', function () { prev(); restartAutoplay(); });
        if (nextBtn) nextBtn.addEventListener('click', function () { next(); restartAutoplay(); });
        dots.forEach(function (dot, i) {
            dot.addEventListener('click', function () { show(i); restartAutoplay(); });
        });

        restartAutoplay();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.hero-slider').forEach(initSlider);
    });
})();
