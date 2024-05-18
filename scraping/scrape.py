# scraping/scrape.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import config
from cleaning.clean_transform import DataCleaner
import logging
from requests.exceptions import RequestException
import time

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.cleaner = DataCleaner()
        self.comments_folder = f'comments_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
        os.makedirs(self.comments_folder, exist_ok=True)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def scrape_comments(self, article_url):
        try:
            logging.info(f"Visiting article URL: {article_url}")
            response = requests.get(article_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            comment_divs = soup.find_all('div', class_='comment-text')
            comments = [div.get_text(strip=True) for div in comment_divs]
            return comments
        except RequestException as e:
            logging.error(f"Failed to fetch article: {article_url}, error: {e}")
            return []

    def scrape_and_save_comments(self):
        all_comments = []

        for url in config.URLS:
            try:
                logging.info(f"Visiting category URL: {url}")
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                article_links_tags = soup.find_all('a', class_='stretched-link')
                article_links = [tag['href'] for tag in article_links_tags]

                category_name = url.split('/')[-1]
                for article_link in article_links:
                    logging.info(f"Scraping comments from article: {article_link}")
                    comments = self.scrape_comments(article_link)
                    for comment in comments:
                        all_comments.append({'Comment': comment, 'Category': category_name})
                    time.sleep(1)  # to avoid hitting the server too hard

            except RequestException as e:
                logging.error(f"Failed to fetch category page: {url}, error: {e}")

        # Convert to DataFrame and clean comments
        comments_df = pd.DataFrame(all_comments)
        cleaned_comments_df = self.cleaner.clean_and_transform_comments(comments_df)

        # Save all comments to a single CSV file
        cleaned_comments_df.to_csv(f'{self.comments_folder}/all_comments.csv', index=False, encoding='utf-8', header=False)
        logging.info(f"All comments saved to {self.comments_folder}/all_comments.csv")

        logging.info("Scraping process completed.")
