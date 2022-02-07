---
permalink: /assets/js/search.js
---

(function() {
    function displaySearchResults(results, store) {
        var searchResults = document.getElementById('search-results');
        var searchCounter = document.getElementById('search-count');

        if (results.length) {
            var appendString = '';
            for (var i = 0; i < results.length; i++) {
                var item = store[results[i].ref];
                console.log(item, item.content.length);

                var content = item.content.substring(0, 120);
                if (item.content.length > 120) content += "..."

                appendString += `
                <div class="row d-flex">
                    <div class="col-12 col-sm-4 col-md-3 d-flex align-items-center p-2">
                        <img class="m-1 img-fluid img-thumbnail align-self-center serach-img mx-auto my-auto" src="{{ site.baseurl }}/${item.thumb}" alt="Result Item Image">
                    </div>
                    <div class="col-12 col-sm-8 col-md-9 d-flex align-items-center">
                        <div class="container">
                            <a href="${item.url}" class="text-decoration-none">
                                <h5>${item.title}</h5>
                            </a>
                            <p>
                                ${content}
                                <a href="${item.url}" class="text-decoration-none text-link me-2">Read More  &rarr;</a>
                            </p>
                        </div>
                    </div>
                </div>
            `;

            }
            searchResults.innerHTML = appendString;
            searchCounter.innerHTML = `About ${results.length} results`;
        } else {
            searchResults.innerHTML = '&nbsp;';
            searchCounter.innerHTML = 'No results found';
        }
    }

    function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split('&');

        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split('=');
            if (pair[0] === variable) {
                return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
            }
        }
    }

    var searchTerm = getQueryVariable('query');
    if (searchTerm) {
        document.getElementById('search-box').setAttribute("value", searchTerm.trim());

        // Initalize lunr with the fields it will be searching on. I've given title
        // a boost of 10 to indicate matches on this field are more important.
        var idx = lunr(function () {
            this.field('id');
            this.field('title', { boost: 10 });
            this.field('categories', { boost: 5 });
            this.field('tags', { boost: 5 });
            this.field('content');
        });

        const url = '{% link assets/js/zzzz-search-data.json %}';
        $.getJSON(url, function(data) {

            // console.log(data);

            for (var key in data) { // Add the data to lunr
                idx.add({
                    'id': key,
                    'title': data[key].title,
                    'doc': data[key].doc,
                    'thumbnail': data[key].thumbnail_url,
                    'content': data[key].content
                });

                var results = idx.search(searchTerm); // Get lunr to perform a search
                displaySearchResults(results, data); // We'll write this in the next section
            }
        });


    }
})();
