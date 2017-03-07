"""Scrape the home page/test because I'm supposed to share this."""

from bs4 import BeautifulSoup
from urllib.request import urlopen


BASE_URL = 'http://dogtime.com/dog-breeds'


def main():
    """Main."""
    html = urlopen(BASE_URL).read()
    soup = BeautifulSoup(html, "lxml")
    breed_urls = get_breed_urls(soup)
    print(breed_urls[:5])


def get_breed_urls(soup):
    """Get all breeds URLs from the base URL."""
    group = soup.find("div", "group with-image-mobile-only")

    all_breeds = group.find_all("a", "post-title", href=True)

    breed_urls = []
    for breed in all_breeds:
        url = breed["href"]
        breed_urls.append(url)

    return breed_urls


if __name__ == "__main__":
    main()
