# scraping/scrape.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import config

class Scraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def scrape_comments(self, article_url):
        print(f"Visiting article URL: {article_url}")
        response = requests.get(article_url, headers=self.headers)
        if response.status_code == 200:
            print("Successfully fetched article page.")
            soup = BeautifulSoup(response.text, 'html.parser')
            comment_divs = soup.find_all('div', class_='comment-text')
            comments = [div.get_text(strip=True) for div in comment_divs]
            return comments
        else:
            print(f"Failed to fetch article: {article_url}")
            return []

    def scrape_and_save_comments(self):
        article_links = []
        for url in config.URLS:
            print(f"Visiting category URL: {url}")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                print("Successfully fetched category page.")
                soup = BeautifulSoup(response.text, 'html.parser')
                article_links_tags = soup.find_all('a', class_='stretched-link')
                article_links.extend([tag['href'] for tag in article_links_tags])
            else:
                print(f"Failed to fetch category page: {response.status_code}")
        
        comments = []
        for article_link in article_links:
            print(f"Scraping comments from article: {article_link}")
            comments.extend(self.scrape_comments(article_link))
        
        comments_df = pd.DataFrame({'Comment': comments})
        print("Scraping process completed.")
        return comments_df
