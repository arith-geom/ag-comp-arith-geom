(() => {
  const dialog = document.querySelector('#site-search-dialog');
  const input = document.querySelector('#site-search-input');
  const results = document.querySelector('#site-search-results');
  const status = document.querySelector('#site-search-status');
  const close = document.querySelector('.site-search-close');
  const openers = Array.from(document.querySelectorAll('[data-site-search-open]'));
  if (!dialog || !input || !results || !status || !close || !openers.length) return;

  let documents;
  let lastOpener;
  const typeIcons = {
    Page: 'fa-compass',
    Member: 'fa-user',
    Publication: 'fa-book-open',
    Teaching: 'fa-chalkboard-teacher',
    Research: 'fa-flask',
    Links: 'fa-link',
  };
  const normalize = (value) => String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase()
    .replace(/\s+/g, ' ')
    .trim();

  const indexUrl = window.prefixBase ? window.prefixBase('/search-index.json') : '/search-index.json';
  const loadIndex = async () => {
    if (documents) return documents;
    const response = await fetch(indexUrl, { credentials: 'same-origin' });
    if (!response.ok) throw new Error(`Search index returned ${response.status}`);
    const entries = await response.json();
    documents = entries.map((entry) => ({
      ...entry,
      searchable: normalize(`${entry.title} ${entry.type} ${entry.text}`),
    }));
    return documents;
  };

  const resultLink = (entry) => {
    const item = document.createElement('li');
    const link = document.createElement('a');
    const icon = document.createElement('span');
    const content = document.createElement('span');
    const headingRow = document.createElement('span');
    const heading = document.createElement('span');
    const type = document.createElement('span');
    const excerpt = document.createElement('span');

    item.className = 'site-search-result';
    link.href = window.prefixBase ? window.prefixBase(entry.url) : entry.url;
    icon.className = 'site-search-result-icon';
    icon.setAttribute('aria-hidden', 'true');
    const iconGlyph = document.createElement('i');
    iconGlyph.className = `fas ${typeIcons[entry.type] || 'fa-file'}`;
    icon.append(iconGlyph);
    content.className = 'site-search-result-content';
    headingRow.className = 'site-search-result-heading';
    heading.className = 'site-search-result-title';
    heading.textContent = entry.title;
    type.className = 'site-search-result-type';
    type.textContent = entry.type;
    excerpt.className = 'site-search-result-excerpt';
    excerpt.textContent = entry.text.length > 150 ? `${entry.text.slice(0, 147)}…` : entry.text;
    headingRow.append(heading, type);
    content.append(headingRow);
    if (entry.text) content.append(excerpt);
    link.append(icon, content);
    item.append(link);
    return item;
  };

  const renderEmptyState = () => {
    const item = document.createElement('li');
    item.className = 'site-search-empty';
    item.innerHTML = '<i class="fas fa-search" aria-hidden="true"></i><strong>No matching pages</strong><span>Try a person, topic, publication title, or course.</span>';
    results.append(item);
  };

  const search = async () => {
    const query = input.value.trim();
    results.replaceChildren();
    if (!query) {
      status.textContent = 'Start typing to search the site.';
      return;
    }

    const terms = normalize(query).split(' ').filter(Boolean);
    try {
      const entries = await loadIndex();
      const matches = entries
        .filter((entry) => terms.every((term) => entry.searchable.includes(term)))
        .slice(0, 12);
      matches.forEach((entry) => results.append(resultLink(entry)));
      if (!matches.length) renderEmptyState();
      status.textContent = matches.length
        ? `${matches.length} ${matches.length === 1 ? 'result' : 'results'}`
        : 'No results found.';
    } catch (_error) {
      status.textContent = 'Search is temporarily unavailable. Please try again.';
    }
  };

  const openSearch = (opener) => {
    const sidebar = opener.closest('.sidebar-nav');
    const navToggle = document.querySelector('.nav-toggle');
    if (sidebar) {
      sidebar.classList.remove('is-open');
      sidebar.setAttribute('aria-hidden', 'true');
      document.querySelector('.sidebar-overlay')?.classList.remove('is-active');
      navToggle?.setAttribute('aria-expanded', 'false');
      navToggle?.setAttribute('aria-label', 'Open navigation');
    }
    lastOpener = sidebar && navToggle ? navToggle : opener;
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    input.focus();
    loadIndex().catch(() => {});
  };

  openers.forEach((opener) => opener.addEventListener('click', () => openSearch(opener)));
  close.addEventListener('click', () => dialog.close());
  input.addEventListener('input', search);
  input.addEventListener('search', search);
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => lastOpener?.focus());
  document.addEventListener('keydown', (event) => {
    const target = event.target;
    const isTyping = target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target?.isContentEditable;
    if (event.key === 'Escape' && dialog.open) {
      event.preventDefault();
      dialog.close();
      return;
    }
    if ((event.key === '/' && !isTyping) || (event.key.toLocaleLowerCase() === 'k' && (event.ctrlKey || event.metaKey))) {
      event.preventDefault();
      openSearch(openers[0]);
    }
  });
})();
