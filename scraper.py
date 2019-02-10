import requests
from bs4 import BeautifulSoup, SoupStrainer
import markovify
import random
import re
import gzip, json

BASE_URL = "https://solarsystem.nasa.gov/planets/"
planets = ["mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "dwarf-planets/haumea", "dwarf-planets/pluto", "dwarf-planets/makemake", "dwarf-planets/ceres", "dwarf-planets/eris", ]
pages = []
sappho = open("sappho.txt").read()
rilke = open("rilke.txt").read()
sea = open("sea.txt").read()
poets = [sappho, rilke, sea]

only_p_tags = SoupStrainer("p")

def clean_sentence(txt):
    txt = txt.replace("kid-friendly", "")
    txt = txt.replace("Kid-Friendly", "")
    txt = txt.replace("\n", " ")
    txt = txt.replace(".", " ")
    txt = txt.replace("?", " ")
    txt = re.sub("^[MDCLXVI]+$", "", txt)
    txt = re.sub("^[0-9]", "", txt)
    txt = re.sub("^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,9})$", "", txt)
    txt = re.sub(" \d+", "", txt)
    return txt

class SentencesByChar(markovify.Text):
    def word_split(self, sentence):
        return list(sentence)
    def word_join(self, words):
        return "".join(words)

class SentencesByCharNewline(markovify.NewlineText):
    def word_split(self, sentence):
        return list(sentence)
    def word_join(self, words):
        return "".join(words)


def construct_planet(planet):
    url = BASE_URL + planet + "/in-depth"
    page = requests.get(url)
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')
        for elem in soup.find_all('div', class_="wysiwyg_content"):
            elem.text.replace("Kid-Friendly", "")
            return elem.text.encode("utf-8")

def construct_poem(text1, text2, times):

    # change to "word" for a word-level model
    level = "char"
    # controls the length of the n-gram
    order = 7
    # controls the number of lines to output
    output_n = 14
    # weights between the models; text A first, text B second.
    # if you want to completely exclude one model, set its corresponding value to 0
    weights = [1, 0.3]
    # limit sentence output to this number of characters
    length_limit = 100

    model_cls = markovify.Text if level == "word" else SentencesByChar
    sentences = []
    gen_a = model_cls(text1, state_size=order)
    gen_b = model_cls(text2, state_size=order)
    gen_combo = markovify.combine([gen_a, gen_b], weights)
    for i in range(times):
        out = gen_combo.make_short_sentence(length_limit, test_output=False)
        sentence = clean_sentence(out)
        sentences.append(sentence)
    return sentences

planet = random.choice(planets)
poet = random.choice(poets)
planet_txt = construct_planet(planet)
print("******************")
print("A POEM FOR " + planet.upper())
print("*******************")
poem = construct_poem(planet_txt, poet, 3)

for line in poem:
    print(line)




