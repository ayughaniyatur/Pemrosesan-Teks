import requests
from bs4 import BeautifulSoup
import pandas as pd

# Mengambil konten dari URL
def get_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# Scraping satu halaman
def scrape_page(page_num):
    url = f"https://indeks.kompas.com/?page={page_num}"
    soup = get_content(url)

    articles = soup.find_all('div', class_='articleItem')

    print(f"Page {page_num}: Found {len(articles)} articles")

    data = []

    for article in articles:
        title = article.find('h2', class_='articleTitle').text.strip()
        category = article.find('div', class_='articlePost-subtitle').text.strip()
        date = article.find('div', class_='articlePost-date').text.strip()
        link = article.find('a')['href']

        # Mendapatkan isi berita
        article_soup = get_content(link)
        content = article_soup.find('div', class_='read__content').text.strip()

        data.append({
            'Title': title,
            'Category': category,
            'Date': date,
            'Content': content
        })

    return data

# Scraping beberapa halaman
def scrape_kompas(pages=10):
    all_data = []
    for page_num in range(1, pages + 1):
        data = scrape_page(page_num)
        all_data.extend(data)
    return all_data

# Menyimpan hasil scraping ke dalam file CSV
def save_to_csv(data, filename='kompas_scraping_results.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n Data saved to {filename}")

# Scrape 10 halaman dari kompas.com
scraped_data = scrape_kompas(pages=10)

df = pd.DataFrame(scraped_data)
print(df.head(5))

save_to_csv(scraped_data)
