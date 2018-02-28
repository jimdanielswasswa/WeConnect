## WeConnect
WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with. 


### User Interface On GitHub Pages:
[WeConnect](https://jimdanielswasswa.github.io/WeConnect/)

### Badges:
[![Build Status](https://travis-ci.org/jimdanielswasswa/WeConnect.svg?branch=master)](https://travis-ci.org/jimdanielswasswa/WeConnect)

[![Build Status](https://travis-ci.org/jimdanielswasswa/WeConnect.svg?branch=develop)](https://travis-ci.org/jimdanielswasswa/WeConnect)

[![Build Status](https://travis-ci.org/jimdanielswasswa/WeConnect.svg?branch=feature%2Fapiv1_branch)](https://travis-ci.org/jimdanielswasswa/WeConnect)

[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)

[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)


### Enviroment Setup For The API
```
virtualenv venv
source venv/bin/activate
cd api/v1/
pip install -r requirements.txt
```

### Windows Configurations For The API:
```
SET FLASK_APP=run.py
SET FLASK_CONFIG=development
```
### Mac OS Configurations For The API:
```
export FLASK_APP=run.py
export FLASK_CONFIG=development
```

### Running Tests:
```
nosetests api/v1/api/tests/tests_auth_endpoints.py
nosetests api/v1/api/tests/tests_business_endpoints.py
```
