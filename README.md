# Set up

### Create a virtual environment
`virtualenv venv`  
`. venv/bin/activate`  

### Imports
`pip install beautifulsoup4`  
`pip install lxml`  

##### urllib2
urllib2 has been split across urllib.request and urllib.error (https://docs.python.org/2/library/urllib2.html)


# Doing it

#### Method(s)
* `urlopen(url).read()`

```
from urllib.request import urlopen

BASE_URL = 'http://dogtime.com/dog-breeds'

html = urlopen(BASE_URL).read()
print(html)
```
Returns the full html of the page the url leads to, but as bytes. It's a lot to look at, and it's basically just text.


#### Method(s)
* `BeautifulSoup(html, parser)`

```
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "lxml")
```
Creating a BeautifulSoup object will make the returned text easier to parse. In order to do this, we need a [parser](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser). Here I decided to use lxml.


#### Method(s)
* `BeautifulSoup.find()`
* `BeautifulSoup.find_all()`

```
group = soup.find("div", "group with-image-mobile-only")
all_breeds = group.find_all("a", "post-title", href=True)
all_letters = soup.findAll("div", "group-letter")
```
These are the two base methods to help find html elements using their tags and attributes. From there [you can build up and use more refined search methods.](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree)


* `Tag["href"]`