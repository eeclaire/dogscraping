## Set up a virtual environment
`virtualenv venv`
`. venv/bin/activate`

## Imports
`pip install beautifulsoup4`
`pip install lxml

#### urllib2
urllib2 has been split across urllib.request and urllib.error (https://docs.python.org/2/library/urllib2.html)


# Doing it

#### Methods
* `urlopen(url).read()`
* `BeautifulSoup(html, format)`

```
from bs4 import BeautifulSoup
from urllib.request import urlopen

BASE_URL = 'http://dogtime.com/dog-breeds'

html = urlopen(BASE_URL).read()
print(html)
```
Returns the full html of the page. It's overwhelming.


#### Methods
* `BeautifulSoup.find()`
* `BeautifulSoup.findAll()`

```
all_letters = group.findAll("div", "group-letter")
for div in all_letters:
    print(div)

print(len(all_letters))
```


* `Tag["href"]`