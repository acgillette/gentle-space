import requests
from bs4 import BeautifulSoup, SoupStrainer
import markovify
import random
import re

BASE_URL = "https://solarsystem.nasa.gov/planets/"
planets = ["mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"]
pages = []
sappho = open("sappho.txt").read()

only_p_tags = SoupStrainer("p")

def construct_planet(planet):
    url = BASE_URL + planet + "/in-depth"
    page = requests.get(url)
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')
        for elem in soup.find_all('div', class_="wysiwyg_content"):
            elem.text.replace("Kid-Friendly", "")
            return elem.text.encode("utf-8")

def construct_poem(text1, text2, times):
    sentences = []
    generator_a = markovify.Text(text1, state_size=2)
    generator_b = markovify.Text(text2, state_size=2)
    combined = markovify.combine([generator_a, generator_b], [0.8,0.2])
    for i in range(times):
        sentence = combined.make_sentence()
        sentence = sentence.replace("Kid-Friendly", "")
        sentence = re.sub("^[MDCLXVI]+$", "", sentence)
        sentence = re.sub("^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,9})$", "", sentence)
        sentence = re.sub(" \d+", "", sentence)
        sentences.append(sentence)
    return sentences

planet = random.choice(planets)
planet_txt = construct_planet(planet)
print("******************")
print("A POEM FOR " + planet.upper())
print("*******************")
poem = construct_poem(planet_txt, sappho, 4)

for line in poem:
    print(line)




