import requests
from bs4 import BeautifulSoup

URL = "https://www.motorsport.com/f1/driver-ratings/?y=2022"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

print(soup)