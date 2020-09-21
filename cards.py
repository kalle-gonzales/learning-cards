import json
from random import shuffle
from time import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

cards_file = 'data.json'

today = time()
with open(cards_file, 'r') as cards:
  raw_data=cards.read()


def get_effective_cards(date):
  effective_cards = []
  cards = json.loads(raw_data)
  for card in cards:
    if card["last"] + card["box"] * 24 * 60 * 60 <= date: # only ask n-th box every n days. last is in seconds
      effective_cards.append(card)

def ask(keys, trys, correct, cards):
  wrong_keys = []
  wrong_cards = []
  for key in keys:
    trys = trys + 1
    card = cards[key]
    if "pics" in card:
      user_input = show_pics(card["pics"])
    else:
      user_input = show(key)
    if user_input:
      card["box"] = card["box"] + 1 # increase box by one
      correct = correct + 1
    else:
      card["box"] = -1 # back to box 0 (when it's answered correctly it will be increased by one, resulting in 0)
      wrong_keys.append(key)
      wrong_cards.append(card)
    card["last"] = today
  if len(wrong_keys):
    return ask(wrong_keys, trys, correct, wrong_cards)
  return [trys, correct]

def show(key):
  plt.imshow(mpimg.imread('front/%s.jpeg' % (key)))
  plt.ion()
  plt.show()
  input()
  plt.close()
  plt.imshow(mpimg.imread('back/%s.jpeg' % (key)))
  plt.ion()
  plt.show()
  user_input = input("\n>>> ")
  plt.close()
  return user_input != "f"

def show_pics(pics):
  number_of_pics = len(pics)
  showing_number = 1
  for pic in pics:
    plt.imshow(mpimg.imread('%s.jpeg' % (pic)))
    plt.ion()
    plt.show()
    if showing_number == number_of_pics:
      user_input = input("Gewusst?\n>>> ")
    else:
      input()
    plt.close()
  return user_input != "f"

effective_cards = get_effective_cards
keys = list(effective_cards.keys())
shuffle(keys)
[trys, correct] = ask(keys, 0, 0, effective_cards)

print("Richtig: %i, Falsch: %i" % (correct, trys - correct))