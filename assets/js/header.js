document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.querySelector('.nav-toggle');
  const sidebarNav = document.querySelector('.sidebar-nav');
  const sidebarOverlay = document.querySelector('.sidebar-overlay');
  const sidebarClose = document.querySelector('.sidebar-close');

  function openSidebar() {
    sidebarNav.classList.add('is-open');
    sidebarOverlay.classList.add('is-active');
  }

  function closeSidebar() {
    sidebarNav.classList.remove('is-open');
    sidebarOverlay.classList.remove('is-active');
  }

  if (navToggle) {
    navToggle.addEventListener('click', openSidebar);
  }
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }
  if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
  }
});
