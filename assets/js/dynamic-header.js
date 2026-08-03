document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.header-main');
  if (!header) return;

  let lastScrollTop = 0;
  let ticking = false;
  const delta = 5;
  const headerHeight = header.offsetHeight;

  const updateHeader = () => {
    const st = window.pageYOffset || document.documentElement.scrollTop;

    if (Math.abs(lastScrollTop - st) <= delta) {
      ticking = false;
      return;
    }

    if (st > lastScrollTop && st > headerHeight) {
      header.classList.add('header--hidden');
    } else {
      header.classList.remove('header--hidden');
    }

    lastScrollTop = Math.max(st, 0);
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });
});
