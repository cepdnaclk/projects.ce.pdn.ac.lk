---
permalink: /assets/js/search.js
---

(function (window, document) {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var config = window.ALGOLIA_CONFIG || {};
    var placeholderRegex = /PLACEHOLDER/i;
    var hasValidConfig =
      config.appId &&
      config.searchApiKey &&
      config.indexName &&
      !placeholderRegex.test(config.appId) &&
      !placeholderRegex.test(config.searchApiKey) &&
      !placeholderRegex.test(config.indexName);

    var selectors = {
      form: "[data-algolia-search-form]",
      input: "[data-algolia-search-input]",
      help: "[data-algolia-search-help]",
    };

    var resultsElement = document.getElementById("algolia-search-results");
    var statusElement = document.getElementById("algolia-search-status");
    var loaderElement = document.getElementById("algolia-search-loader");
    var countElement = document.getElementById("algolia-search-count");
    var paginationWrapper = document.getElementById("algolia-search-pagination");
    var paginationList = paginationWrapper ? paginationWrapper.querySelector("ul") : null;
    var modalElement = document.getElementById("algoliaSearchModal");
    var queryParam = new URLSearchParams(window.location.search).get("query");
    var hitsPerPage = 8;
    var allHits = [];
    var currentPage = 0;
    var currentQuery = "";

    function getForms() {
      return Array.prototype.slice.call(document.querySelectorAll(selectors.form));
    }

    function getInputs() {
      return Array.prototype.slice.call(document.querySelectorAll(selectors.input));
    }

    function getHelpers() {
      return Array.prototype.slice.call(document.querySelectorAll(selectors.help));
    }

  function setHelpers(message, isError) {
    getHelpers().forEach(function (element) {
      element.classList.remove("d-none");
      element.classList.toggle("text-danger", Boolean(isError));
      element.textContent = message;
    });
  }

  function clearHelpers() {
    getHelpers().forEach(function (element) {
      element.classList.add("d-none");
      element.classList.remove("text-danger");
      element.textContent = "";
    });
  }

  function setQueryForAllInputs(query) {
    getInputs().forEach(function (input) {
      input.value = query;
    });
  }

  function setLoading(isLoading) {
    if (!loaderElement) {
      return;
    }

    loaderElement.classList.toggle("d-none", !isLoading);
    if (isLoading && resultsElement) {
      resultsElement.innerHTML = "";
    }
  }

  function updateStatus(message, isError) {
    if (!statusElement) {
      return;
    }

    statusElement.classList.toggle("text-danger", Boolean(isError));
    statusElement.textContent = message;
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function validUrl(value) {
    if (!value || value === "#") {
      return "";
    }
    return value;
  }

  function chooseDescription(hit) {
    var snippet =
      hit._snippetResult &&
      hit._snippetResult.description &&
      hit._snippetResult.description.value;
    return snippet || escapeHtml(hit.description || "No description available.");
  }

  function resultBadge(text, className) {
    return '<span class="badge ' + className + '">' + escapeHtml(text) + "</span>";
  }

  function buildBadges(hit) {
    var badges = [];
    if (hit.category_title) {
      badges.push(resultBadge(hit.category_title, "badge-primary"));
    }
    if (hit.category_code) {
      badges.push(resultBadge(hit.category_code.toUpperCase(), "badge-dark"));
    }

    (hit.tags || []).slice(0, 4).forEach(function (tag) {
      badges.push(resultBadge(tag, "badge-secondary"));
    });

    return badges.length
      ? '<div class="algolia-result-badges mb-2">' + badges.join("") + "</div>"
      : "";
  }

  function buildPeopleSummary(label, people) {
    if (!people || !people.length) {
      return "";
    }
    return (
      '<p class="small text-muted mb-2"><strong>' +
      escapeHtml(label) +
      ":</strong> " +
      escapeHtml(people.slice(0, 4).join(", ")) +
      "</p>"
    );
  }

  function buildActionButtons(hit) {
    var actions = [];
    var actionMap = [
      { label: "Project", url: validUrl(hit.project_url), className: "btn-primary" },
      { label: "Page", url: validUrl(hit.page_url), className: "btn-outline-primary" },
      { label: "Repository", url: validUrl(hit.repo_url), className: "btn-outline-secondary" },
      { label: "API", url: validUrl(hit.api_url), className: "btn-outline-dark" },
    ];

    actionMap.forEach(function (action) {
      if (!action.url) {
        return;
      }
      actions.push(
        '<a class="btn btn-sm ' +
          action.className +
          '" href="' +
          escapeHtml(action.url) +
          '">' +
          escapeHtml(action.label) +
          "</a>"
      );
    });

    return actions.length
      ? '<div class="algolia-result-actions mt-3">' + actions.join("") + "</div>"
      : "";
  }

  function buildHitHtml(hit) {
    var title =
      (hit._highlightResult && hit._highlightResult.title && hit._highlightResult.title.value) ||
      escapeHtml(hit.title || "Untitled project");
    var resultUrl =
      validUrl(hit.result_url || hit.project_url || hit.page_url || hit.repo_url || hit.api_url) ||
      "#";
    var image = validUrl(hit.thumbnail_url) || "{{ '/assets/images/crest.png' | relative_url }}";

    return (
      '<div class="list-group-item">' +
      '<div class="d-flex algolia-result-card">' +
      '<img class="algolia-result-thumb" src="' +
      escapeHtml(image) +
      '" alt="' +
      escapeHtml(hit.title || "Project result") +
      '">' +
      '<div class="flex-grow-1">' +
      '<a class="text-decoration-none" href="' +
      escapeHtml(resultUrl) +
      '"><h5 class="mb-2">' +
      title +
      "</h5></a>" +
      buildBadges(hit) +
      '<p class="mb-2">' +
      chooseDescription(hit) +
      "</p>" +
      buildPeopleSummary("Team", hit.team_names || []) +
      buildPeopleSummary("Supervisors", hit.supervisor_names || []) +
      buildActionButtons(hit) +
      "</div></div></div>"
    );
  }

  function renderPagination(totalResults, pageIndex) {
    if (!paginationWrapper || !paginationList) {
      return;
    }

    var totalPages = Math.ceil(totalResults / hitsPerPage);
    if (totalPages <= 1) {
      paginationWrapper.classList.add("d-none");
      paginationList.innerHTML = "";
      return;
    }

    var items = [];

    function addButton(label, page, disabled, active) {
      var classNames = ["page-item"];
      if (disabled) {
        classNames.push("disabled");
      }
      if (active) {
        classNames.push("active");
      }
      items.push(
        '<li class="' +
          classNames.join(" ") +
          '"><button class="page-link" type="button" data-page="' +
          page +
          '">' +
          label +
          "</button></li>"
      );
    }

    addButton("Prev", Math.max(pageIndex - 1, 0), pageIndex === 0, false);
    for (var index = 0; index < totalPages; index += 1) {
      addButton(String(index + 1), index, false, index === pageIndex);
    }
    addButton("Next", Math.min(pageIndex + 1, totalPages - 1), pageIndex === totalPages - 1, false);

    paginationList.innerHTML = items.join("");
    paginationWrapper.classList.remove("d-none");
  }

  function renderPage(pageIndex) {
    if (!resultsElement) {
      return;
    }

    currentPage = pageIndex;
    var start = pageIndex * hitsPerPage;
    var pageHits = allHits.slice(start, start + hitsPerPage);
    resultsElement.innerHTML = pageHits.map(buildHitHtml).join("");

    if (!pageHits.length) {
      updateStatus('No results found for "' + currentQuery + '".');
      if (countElement) {
        countElement.textContent = "";
      }
      if (paginationWrapper) {
        paginationWrapper.classList.add("d-none");
      }
      return;
    }

    updateStatus(
      'Showing ' +
        pageHits.length +
        " of " +
        allHits.length +
        ' results for "' +
        currentQuery +
        '".'
    );
    if (countElement) {
      countElement.textContent =
        "Page " + (pageIndex + 1) + " of " + Math.ceil(allHits.length / hitsPerPage);
    }
    renderPagination(allHits.length, pageIndex);
  }

  function showModal() {
    if (window.jQuery && modalElement) {
      window.jQuery(modalElement).modal("show");
    }
  }

  function performSearch(query) {
    if (!hasValidConfig || !window.algoliasearch) {
      return;
    }

    var client = window.algoliasearch(config.appId, config.searchApiKey);
    var index = client.initIndex(config.indexName);
    currentQuery = query;
    clearHelpers();
    setQueryForAllInputs(query);
    setLoading(true);
    updateStatus('Searching for "' + query + '"...');
    showModal();

    index
      .search(query, {
        hitsPerPage: 100,
        attributesToSnippet: ["description:20"],
        highlightPreTag: "<mark>",
        highlightPostTag: "</mark>",
      })
      .then(function (response) {
        allHits = Array.isArray(response.hits) ? response.hits : [];
        setLoading(false);
        renderPage(0);
      })
      .catch(function (error) {
        setLoading(false);
        updateStatus("Search failed. Please try again later.", true);
        if (window.console) {
          console.error("Algolia search error", error);
        }
      });
  }

    if (!getForms().length) {
      return;
    }

    if (!hasValidConfig) {
      setHelpers(
        "Search is currently unavailable. Configure ALGOLIA_APP_ID and ALGOLIA_SEARCH_API_KEY to enable it.",
        true
      );
      return;
    }

    getForms().forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var input = form.querySelector(selectors.input);
        var query = input ? input.value.trim() : "";
        if (!query) {
          updateStatus("Enter a search term to begin.");
          return;
        }
        performSearch(query);
      });
    });

    if (paginationList) {
      paginationList.addEventListener("click", function (event) {
        var button = event.target.closest("button[data-page]");
        if (!button) {
          return;
        }

        var page = Number(button.getAttribute("data-page"));
        if (Number.isNaN(page) || page === currentPage) {
          return;
        }
        renderPage(page);
      });
    }

    if (queryParam) {
      setQueryForAllInputs(queryParam);
      performSearch(queryParam);
    }
  });
})(window, document);
