// Simple-Jekyll-Search
// https://github.com/christian-fei/Simple-Jekyll-Search

(function(){
  // Getyour DOM elements
  var searchInput = document.getElementById('search-input');
  var searchResults = document.getElementById('search-results');
  var jsonData = [];
  var index;

  // Fetch the search data
  fetch('{{ "/assets/json/search.json" | relative_url }}')
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      jsonData = data;
      // Initialize Lunr.js
      index = lunr(function () {
        this.ref('url');
        this.field('title', { boost: 10 });
        this.field('content');

        jsonData.forEach(function (doc) {
          this.add(doc);
        }, this);
      });
    });

  // Handle search input
  searchInput.addEventListener('keyup', function (e) {
    var query = e.target.value;
    if (query === '') {
      searchResults.style.display = 'none';
      return;
    }

    var results = index.search(query);
    displayResults(results);
  });

  // Display search results
  function displayResults(results) {
    if (results.length) {
      searchResults.style.display = 'block';
      var output = '<ul>';
      results.forEach(function(result) {
        var item = jsonData.find(function(item) {
          return item.url === result.ref;
        });
        output += '<li><a href="' + item.url + '">' + item.title + '</a></li>';
      });
      output += '</ul>';
      searchResults.innerHTML = output;
    } else {
      searchResults.style.display = 'none';
    }
  }

  // Hide results when clicking outside
  document.addEventListener('click', function(e) {
    if (!searchResults.contains(e.target) && e.target !== searchInput) {
      searchResults.style.display = 'none';
    }
  });

})(); 