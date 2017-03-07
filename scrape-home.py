"""Scrape the home page/test because I'm supposed to share this."""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pprint


BASE_URL = 'http://dogtime.com/dog-breeds'


def main():
    """Main."""
    breed_urls = get_breed_urls(BASE_URL)

    dogs = {}
    for breed_url in breed_urls:
        breed, characteristics = get_dog_and_characteristics(breed_url)
        dogs[breed] = characteristics

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(dogs)


def get_breed_urls(url):
    """Get all breeds URLs from the base URL."""
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    group = soup.find("div", "group with-image-mobile-only")

    all_breeds = group.find_all("a", "post-title", href=True)

    breed_urls = []
    for breed in all_breeds:
        url = breed["href"]
        breed_urls.append(url)

    return breed_urls


def get_dog_and_characteristics(url):
    """Get a given dog's characteristics."""
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    dog_breed = soup.find("h1").string
    characteristics_box = soup.find_all("div", "characteristics-ratings")

    dog_characteristics = {}

    for div in characteristics_box:
        main_characteristics = div.find_all("div", "parent-characteristic")

    for char in main_characteristics:

        char_name = char.find("span", "item-trigger-title").string.strip()
        char_rating = int(char.find("span", "star").attrs['class'][-1][-1:])

        dog_characteristics[char_name] = {}  # create dictionary for this breed
        children = {}  # and for its child characteristics

        # find the children - make sure it isn't another parent characteristic
        while(True):
            if (type(char.next_sibling) != type(char)) or (
                    'parent-characteristic' in char.next_sibling.attrs['class']
            ):
                break

            # get the name and rating of the child characteristic
            sub_char_name = char.next_sibling.find(
                "span", "item-trigger-title").string
            sub_char_rating = int(char.next_sibling.find(
                "span", "star").string)

            # place name + rating into the child dictionary
            children[sub_char_name] = sub_char_rating
            char = char.next_sibling

        dog_characteristics[char_name]['rating'] = char_rating
        dog_characteristics[char_name]['children'] = children

    return (dog_breed, dog_characteristics)


if __name__ == "__main__":
    main()
