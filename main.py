# main.py
from scraping.scrape import Scraper
from cleaning.clean_transform import DataCleaner
import os
from datetime import datetime
import logging

def main():
    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize scraper
    scraper = Scraper()

    # Scrape comments and save them to a single CSV file
    scraper.scrape_and_save_comments()

    # Initialize data cleaner
    cleaner = DataCleaner()

    # Get the combined comments file
    comments_file = f'{scraper.comments_folder}/all_comments.csv'

    # Translate and save comments to English
    translated_folder = f'english_comments_{datetime.now().strftime("%Y-%m-%d")}'
    os.makedirs(translated_folder, exist_ok=True)
    translated_file = f'{translated_folder}/all_comments_translated.csv'
    
    cleaner.translate_and_save_comments_to_english(comments_file, translated_file)

    logging.info("Translation process completed.")

if __name__ == "__main__":
    main()
