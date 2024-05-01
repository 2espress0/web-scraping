# main.py
from scraping.scrape import Scraper
from cleaning.clean_transform import DataCleaner
import pandas as pd

def main():
    # Initialize scraper
    scraper = Scraper()

    # Scrape comments
    comments_df = scraper.scrape_and_save_comments()

    # Initialize data cleaner
    cleaner = DataCleaner()

    # Clean and transform comments
    cleaned_comments = cleaner.clean_and_transform_comments(comments_df)

    # Save cleaned comments to a CSV file
    csv_file_path = 'cleaned_comments.csv'
    cleaner.save_comments_to_csv(cleaned_comments, csv_file_path)
    print(f"Cleaned comments saved to {csv_file_path}")

if __name__ == "__main__":
    main()
