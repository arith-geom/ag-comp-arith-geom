// Minimal PagesCMS bridge for local editing triggers
(function(){
  window.PagesCMS = window.PagesCMS || {};
  const metaRepo = document.querySelector('meta[name="repository-url"]');
  const metaBranch = document.querySelector('meta[name="repository-branch"]');
  window.PagesCMS.config = {
    repoUrl: metaRepo ? metaRepo.getAttribute('content') : '',
    branch: metaBranch ? metaBranch.getAttribute('content') : 'main'
  };
  window.PagesCMS.open = function(){
    const url = 'https://app.pagescms.org';
    window.open(url, '_blank', 'noopener');
  };
  window.PagesCMS.refresh = function(){
    // For static Jekyll sites, local refresh means reloading the page
    // In production, rely on CI build completing after commit
    if (typeof location !== 'undefined') {
      location.reload();
    }
  };
})();


