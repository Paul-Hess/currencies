# Currency Flask Demo

### run tests
* add api key at $HOME/.currency-api-key.txt for api.currencyapi.com
* add api key at $HOME/.apilayer-api-key.txt for api.apilayer.com/currency_data
* pip install -r requirements.txt
* python -m pytest -v

### build and run
* add api key at $HOME/.currency-api-key.txt for api.currencyapi.com
* add api key at $HOME/.apilayer-api-key.txt for api.apilayer.com/currency_data
* docker-compose up

### considerations
* use https://python-poetry.org/ for locked dependency management
* add pylint, formatter
* restructure/org files
* moar test
* DRY some things up
* error handling and 4XX/5XX level HTTP responses
