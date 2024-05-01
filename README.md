# Hespress Web Scraping

This project is designed to scrape comments in arabic from articles on the Hespress website, clean and transform the data, and perform sentiment analysis on the comments.

## Installation

1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.

## Usage

1. Run the `main.py` script to scrape comments from the Hespress website and save them to a CSV file.
2. You can then use the cleaned CSV file for further analysis or processing.

## Project Structure

- `scraping/`: Contains the scraper module responsible for fetching comments from the Hespress website for each category.
- `cleaning/`: Contains the data cleaner module responsible for cleaning and transforming the scraped data.
- `sentiment_analysis/`: (currently not implemented).
- `config.py`: Configuration file containing URLs of different sections of the Hespress website.
- `main.py`: Main script to run the scraping and cleaning process.


