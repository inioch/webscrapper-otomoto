import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time

# base_url = "https://www.otomoto.pl/osobowe/audi/a3?search%5Border%5D=created_at_first%3Adesc"
base_url = "https://www.otomoto.pl/osobowe/audi/80--q3-sportback?search%5Border%5D=created_at_first%3Adesc"
headers = {"User-Agent": "Mozilla/5.0"}



def get_offers(url):
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        offers = []

        articles = soup.find_all("article")

        for offer in articles:
            title_tag = offer.find("h2", class_="ei3upbu0 ooa-1jjzghu")
            price_tag = offer.find("h3", class_="e149hmnd1 ooa-1n2paoq")
            link_tag = offer.find("a", href=True)
            
            title = title_tag.text.strip() if title_tag else "N/A"
            price = price_tag.text.strip() if price_tag else "N/A"
            link  = link_tag["href"] if link_tag  else "N/A"
            if title != "N/A":
                offers.append({
                    "Tytuł": title,
                    "Cena": price,
                    "Link": link
                })           
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []
    return offers


def scrape_all_pages(base_url):
    start_time = time.time()
    page = 1
    all_offers = []
    while True:
        url = f"{base_url}&page={page}"
        print(f"Pobieranie strony {page}...")
        offers = get_offers(url)
        if not offers:
            print(f"Nie znaleziono ofert na stronie {page}.")
            break
        all_offers.extend(offers)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        next_button = soup.find("li", title="Go to next Page")

        if next_button and next_button.get("aria-disabled") == "true":
            print("Brak kolejnych stron.")
            break
        page += 1
        print(next_button)
        
    if all_offers:
        df = pd.DataFrame(all_offers)
        df.to_excel("Oferty otomoto.xlsx", index=False)
        print("Pobrano oferty i zapisano do pliku Excel.")
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Czas wykonania: {execution_time:.2f} sekund")
    else:
        print("Nie znaleziono ofert.")

        
scrape_all_pages(base_url)