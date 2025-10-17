// assets/js/footer.js

document.addEventListener('DOMContentLoaded', function() {
  const backToTopButton = document.getElementById('back-to-top');

  if (backToTopButton) {
    // Show or hide the button based on scroll position
    const toggleBackToTopButton = () => {
      if (window.scrollY > 300) { // Show button after scrolling 300px
        backToTopButton.classList.add('show');
      } else {
        backToTopButton.classList.remove('show');
      }
    };

    // Smooth scroll to top when the button is clicked
    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    };

    // Add event listeners
    window.addEventListener('scroll', toggleBackToTopButton);
    backToTopButton.addEventListener('click', scrollToTop);

    // Initial check in case the page is already scrolled down
    toggleBackToTopButton();
  }
});