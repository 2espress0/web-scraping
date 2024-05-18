# cleaning/clean_transform.py
import pandas as pd
import re
import os
from googletrans import Translator

class DataCleaner:
    def __init__(self):
        self.translator = Translator()

    def clean_and_transform_comments(self, comments_df):
        # Remove duplicate comments
        comments_df = comments_df.drop_duplicates()

        # Remove null comments
        comments_df = comments_df.dropna(subset=['Comment'])

        # Clean comments
        comments_df['Comment'] = comments_df['Comment'].apply(self.clean_comment)
        
        # Remove empty comments
        comments_df = comments_df[comments_df['Comment'] != '']
        
        return comments_df

    def clean_comment(self, comment):
        # Remove non-Arabic characters and additional characters like ، and ؟
        arabic_comment = re.sub(r'[^\u0600-\u06FF\s،؟!-]', '', comment)
        # Remove double quotes, single commas, and multiple consecutive commas
        cleaned_comment = re.sub(r'[",]+', '', arabic_comment)
        # Remove extra spaces
        cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment).strip()
        # Remove any non-Arabic words
        arabic_words_only = ' '.join(word for word in cleaned_comment.split() if all(char.isalpha() and ord(char) >= 0x600 and ord(char) <= 0x6FF for char in word))
        return arabic_words_only

    def translate_and_save_comments_to_english(self, comments_file, translated_file):
        comments_df = pd.read_csv(comments_file, header=None, names=['Comment', 'Category'])
        translated_comments = []
        
        for index, row in comments_df.iterrows():
            try:
                translated_comment = self.translator.translate(row['Comment'], src='ar', dest='en').text
                # Remove double quotes, commas, and periods
                translated_comment = translated_comment.replace('"', '').replace(',', '').replace('.', '')
                if translated_comment:
                    translated_comments.append({'Translated_Comment': translated_comment, 'Category': row['Category']})
            except Exception as e:
                print(f"Translation failed for comment: {row['Comment']}, error: {e}")
        
        translated_df = pd.DataFrame(translated_comments)
        translated_df.to_csv(translated_file, index=False, encoding='utf-8', header=False)
        print(f"Translated comments saved to {translated_file}")
