import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_elements(URL):
    
    # tu peux l'obtenir en tapant sur google : 'my user agent'
    # question de dire au site scrapé qu'on est des vrais users et pas des robots!
    # à voir si tu dois l'adapter
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    reviews = []
    #Boucle pour tout les reviews du produit, j'ai utilisé les expressions régulières à l'aide du 're' library
    #[customer_review-*] va chercher tout les div qui commencent par 'customer_review-' et peu importe la suite, d'où l'utilisation de la 'star *'
    for heading in soup.find_all("div", id=re.compile("customer_review-*")):
        #pour obtenir le nom du reviewer
        author = heading.find("span", {"class": "a-profile-name"}).text
        #pour obtenir le text de la review
        review = heading.find("div", {"class": "reviewText"}).text
        reviews.append([author,review])
    
    return reviews
    
        
