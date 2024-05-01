# cleaning/clean_transform.py
import pandas as pd
import re

class DataCleaner:
    def clean_and_transform_comments(self, comments_df):
        # Convert list to DataFrame if necessary
        if isinstance(comments_df, list):
            comments_df = pd.DataFrame({'Comment': comments_df})
        
        # Remove header
        comments_df = comments_df[comments_df['Comment'] != 'Comment']
        
        # Remove duplicate comments
        comments_df = comments_df.drop_duplicates()

        # Remove null comments
        comments_df = comments_df.dropna(subset=['Comment'])

        # Clean comments
        comments_df['Comment'] = comments_df['Comment'].apply(self.clean_comment)
        
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

    def save_comments_to_csv(self, comments_df, file_path):
        comments_df.to_csv(file_path, index=False, encoding='utf-8', header=False)
