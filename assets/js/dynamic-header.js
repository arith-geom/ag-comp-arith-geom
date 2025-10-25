document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.header-main');
  let lastScrollTop = 0;
  const delta = 5;
  const headerHeight = header.offsetHeight;

  window.addEventListener('scroll', () => {
    const st = window.pageYOffset || document.documentElement.scrollTop;

    // Make sure they scroll more than delta
    if (Math.abs(lastScrollTop - st) <= delta) {
      return;
    }

    if (st > lastScrollTop && st > headerHeight) {
      // Scroll Down
      header.classList.add('header--hidden');
    } else {
      // Scroll Up
      header.classList.remove('header--hidden');
    }

    lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
  }, false);
});