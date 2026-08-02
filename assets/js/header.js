document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.querySelector('.nav-toggle');
  const sidebarNav = document.querySelector('.sidebar-nav');
  const sidebarOverlay = document.querySelector('.sidebar-overlay');
  const sidebarClose = document.querySelector('.sidebar-close');

  if (!navToggle || !sidebarNav || !sidebarOverlay || !sidebarClose) {
    return;
  }

  function openSidebar() {
    sidebarNav.classList.add('is-open');
    sidebarOverlay.classList.add('is-active');
    sidebarNav.setAttribute('aria-hidden', 'false');
    navToggle.setAttribute('aria-expanded', 'true');
    navToggle.setAttribute('aria-label', 'Close navigation');
    sidebarClose.focus();
  }

  function closeSidebar() {
    sidebarNav.classList.remove('is-open');
    sidebarOverlay.classList.remove('is-active');
    sidebarNav.setAttribute('aria-hidden', 'true');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'Open navigation');
    navToggle.focus();
  }

  navToggle.addEventListener('click', () => {
    if (sidebarNav.classList.contains('is-open')) closeSidebar();
    else openSidebar();
  });
  sidebarOverlay.addEventListener('click', closeSidebar);
  sidebarClose.addEventListener('click', closeSidebar);
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && sidebarNav.classList.contains('is-open')) {
      closeSidebar();
    }
  });
});
