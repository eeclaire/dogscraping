"""Scrape the home page/test because I'm supposed to share this."""

from bs4 import BeautifulSoup
from urllib.request import urlopen

import pprint
import psycopg2
import psycopg2.extras

from psycopg2.extras import Json


BASE_URL = 'http://dogtime.com/dog-breeds'


def main():
    """Main."""
    breed_urls = get_breed_urls(BASE_URL)

    dogs = {}
    for breed_url in breed_urls:
        breed, characteristics = get_dog_and_characteristics(breed_url)
        insert_breed_into_db(breed, characteristics)
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


def get_child_characteristics(characteristic):
    """Get the child characteristics following a parent characteristic."""
    children = {}
    parent_class = 'parent-characteristic'

    # find the children - make sure it isn't another parent characteristic
    while(True):
        if (type(characteristic.next_sibling) != type(characteristic)) or (
                parent_class in characteristic.next_sibling.attrs['class']):
            return children

        # get the name and rating of the child characteristic
        child_characteristic_name = characteristic.next_sibling.find(
            "span", "item-trigger-title").string
        child_characteristic_rating = int(characteristic.next_sibling.find(
            "span", "star").string)

        # place name + rating into the child dictionary
        children[child_characteristic_name] = child_characteristic_rating
        characteristic = characteristic.next_sibling


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

        children = get_child_characteristics(char)

        dog_characteristics[char_name]['rating'] = char_rating
        dog_characteristics[char_name]['children'] = children

    return (dog_breed, dog_characteristics)


def insert_breed_into_db(dog_breed, dog_characteristics):
    """Insert the breed and its characteristics into the dog db."""
    conn = psycopg2.connect("dbname=dogsdb host=localhost user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""insert into dogbreeds (breed,
                                       adaptability,
                                       adaptability_rating,
                                       all_around_friendliness,
                                       all_around_friendliness_rating,
                                       health_grooming,
                                       health_grooming_rating,
                                       trainability,
                                       trainability_rating,
                                       exercise_needs,
                                       exercise_needs_rating)
                                      values (%s, %s, %s, %s, %s, %s,
                                              %s, %s, %s, %s, %s)
                """, (dog_breed,
                      Json(dog_characteristics['Adaptability']['children']),
                      dog_characteristics['Adaptability']['rating'],
                      Json(dog_characteristics['All Around Friendliness']['children']),
                      dog_characteristics['All Around Friendliness']['rating'],
                      Json(dog_characteristics['Health Grooming']['children']),
                      dog_characteristics['Health Grooming']['rating'],
                      Json(dog_characteristics['Trainability']['children']),
                      dog_characteristics['Trainability']['rating'],
                      Json(dog_characteristics['Exercise Needs']['children']),
                      dog_characteristics['Exercise Needs']['rating'])
                )

    # Make the changes persistent in the database and end communications
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
