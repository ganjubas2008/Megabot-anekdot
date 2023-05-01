import requests
from bs4 import BeautifulSoup
import telebot
import random
from telebot import types
 
import db
from jokeclass import Joke
     
def get_good(num):
    if num < 0 or num >= 30:
        return "error"
    url = 'https://baneks.ru/top'
    response = requests.get(url=url)

    response.encoding = 'utf-8'
 
    soup = BeautifulSoup(response.text, 'lxml')
    golden = soup.findAll('a', class_='golden-anek')
    return golden[num].text

def get_any(id):
    if id < 0 or id > 1100:
        return "error"
    
    if db.get(id).id == 0:    
        url = f'https://baneks.ru/{id}'
        response = requests.get(url=url)

        response.encoding = 'utf-8'
    
        soup = BeautifulSoup(response.text, 'lxml')
        anek = soup.find('p')
        db.add(Joke(id, anek.text, 0, 0))

    return db.get(id)

if __name__ == "__main__":
    print(get_any(2))