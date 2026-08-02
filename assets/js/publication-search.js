(() => {
  const form = document.querySelector('.publication-search');
  const input = document.querySelector('#publication-search-input');
  const grid = document.querySelector('#publication-grid');
  const count = document.querySelector('#publication-result-count');
  const clear = document.querySelector('.publication-search-clear');
  const empty = document.querySelector('.publication-search-empty');

  if (!form || !input || !grid || !count || !clear || !empty) return;

  const cards = Array.from(grid.querySelectorAll(':scope > .publication-card'));
  const normalize = (value) => value
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
  const searchable = new Map(cards.map((card) => [card, normalize(card.textContent || '')]));

  const updateUrl = (query) => {
    const url = new URL(window.location.href);
    if (query) url.searchParams.set('q', query);
    else url.searchParams.delete('q');
    window.history.replaceState({}, '', `${url.pathname}${url.search}${url.hash}`);
  };

  const filter = () => {
    const query = input.value.trim();
    const terms = normalize(query).split(' ').filter(Boolean);
    let visible = 0;

    cards.forEach((card) => {
      const matches = terms.every((term) => searchable.get(card).includes(term));
      card.hidden = !matches;
      if (matches) visible += 1;
    });

    count.textContent = `${visible} ${visible === 1 ? 'publication' : 'publications'}`;
    clear.hidden = !query;
    empty.hidden = visible !== 0;
    updateUrl(query);
  };

  form.addEventListener('submit', (event) => event.preventDefault());
  input.addEventListener('input', filter);
  input.addEventListener('search', filter);
  clear.addEventListener('click', () => {
    input.value = '';
    filter();
    input.focus();
  });

  const initialQuery = new URL(window.location.href).searchParams.get('q');
  if (initialQuery) {
    input.value = initialQuery;
    filter();
  }
})();
