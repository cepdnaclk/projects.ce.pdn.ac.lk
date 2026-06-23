[![Build and Deploy - Daily](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/daily-build.yml/badge.svg?branch=main)](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/daily-build.yml)
[![Build and Deploy - Weekly](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/weekly-build.yml/badge.svg?branch=main)](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/weekly-build.yml)
[![Algolia Search Index](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/algolia-index.yml/badge.svg?branch=main)](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/algolia-index.yml)
[![GitHub Pages](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/cepdnaclk/projects.ce.pdn.ac.lk/actions/workflows/pages/pages-build-deployment)

# projects.ce.pdn.ac.lk

This is the repository contains the source code for [https://projects.ce.pdn.ac.lk](https://projects.ce.pdn.ac.lk). The site is built by Jekyll Builder and hosted on GitHub pages

## Update the site

Student projects on [github.com/cepdnaclk](https://github.com/cepdnaclk) can be added to this site using the python script found in the root folder. Run following instructions to run the script and make a pull request to the repository.

```bash
# Create a virtual environment and install the required dependencies
python3 -m venv .venv
source .venv/bin/activate

# Install the required dependencies and run the script
pip install requests

# Move into the python scripts folder
cd ./python_scripts/

# Re-index the repositories and update the site
python index_repositories.py

# Build and aggregate the Projects index
python dynamic_data.py

# Update the latest and popular projects sections
python projects_latest.py
python projects_popular.py
```

## Build Instructions

Currently, the site is built by GitHub itself once there is a pull request to the _main_ branch.

If you are interested in build the site in a local environment, info on how to build can be found in [projects.ce.pdn.ac.lk/docs/deployment](https://projects.ce.pdn.ac.lk/docs/deployment). You can also use _setup.sh_ and _run.sh_ bash scripts in the folder, _/scripts_.

## Algolia Search

The site search now uses Algolia instead of the old static Lunr JSON flow.

### Required configuration

Configure these values before enabling the search UI or running the indexer:

```bash
ALGOLIA_APP_ID=<algolia-application-id>
ALGOLIA_SEARCH_API_KEY=<algolia-search-only-api-key>
ALGOLIA_ADMIN_API_KEY=<algolia-admin-api-key>
```

GitHub Actions configuration:

- Add `ALGOLIA_APP_ID` as a repository variable.
- Add `ALGOLIA_ADMIN_API_KEY` as a repository secret.
- If your Pages build injects environment variables, also provide `ALGOLIA_SEARCH_API_KEY`.

For the current branch-based GitHub Pages build, replace the placeholder values in `_config.yml`
with the public search-only values. Do not place the admin API key in the repository.

### Local indexing and tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
cd python_scripts
python algolia_index.py
```

The indexer fetches `https://api.ce.pdn.ac.lk/projects/v1/all/`, validates the payload, logs fetch,
transform, diff, upsert, delete, and failure stages, then syncs the configured Algolia index.

## Contact Info

If you have any doubt about implementation or need to report a bug or a suggestion, please feel free to contact one of them.

### Coordinator

- Prof. Roshan Ragel (<a href="mailto:roshanr@eng.pdn.ac.lk ">roshanr@eng.pdn.ac.lk </a>)

### Developers

- Nuwan Jaliyagoda (<a href="mailto:nuwanjaliyagoda@eng.pdn.ac.lk">nuwanjaliyagoda@eng.pdn.ac.lk</a> <a href="https://github.com/NuwanJ" target="_blank">GitHub: @NuwanJ</a> )
- Akila Karunanayake (<a href="mailto:e17154@eng.pdn.ac.lk">e17154@eng.pdn.ac.lk</a> | <a href="https://github.com/Akilax0" target="_blank">GitHub: @Akilax0</a> ) </li>

### Contribute

If you are willing to contribute to improving this website, please feel free to contact Prof. Roshan Ragel ([roshanr@eng.pdn.ac.lk](mailto:roshanr@eng.pdn.ac.lk))
