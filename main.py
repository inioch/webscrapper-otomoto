import requests 
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.otomoto.pl/osobowe/audi/a3?search%5Border%5D=created_at_first%3Adesc"

def get_offers(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        offers = soup.find_all("article")

        for offer in offers:
            title_tag = offer.find("h2", class_="ei3upbu0 ooa-1jjzghu")
            price_tag = offer.find("h3", class_="e149hmnd1 ooa-1n2paoq")
            link_tag = offer.find("a", href=True)
            
            title = title_tag.text.strip() if title_tag else "N/A"
            price = price_tag.text.strip() if price_tag else "N/A"
            link  = link_tag["href"] if link_tag  else "N/A"



            if title != "N/A":
                print(f"🔹 Tytuł: {title}")
                print(f"💰 Cena: {price}")
                print(f"🔗 Link: {link}")
            
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

def scrape_all_pages(base_url):
    page = 1
    while True:
        print(f"Pobieranie strony {page}")
        url = f"{base_url}&page={page}"
        get_offers(url)

        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        next_button = soup.find("li", {"class": "ooa-12wp27z"})
        if next_button and next_button.has_attr('disabled'):
            break
        page += 1
        
scrape_all_pages(base_url)