import json
import pandas as pd

class FewShotPosts:
    def __init__(self, file_path="Data/preprocessed_post.json"):
        self.df = None
        self.unqiue_tags = None
        self.load_post(file_path)

    def load_post(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            post = json.load(f)
            self.df = pd.json_normalize(post)
            self.df['length'] = self.df['line_count'].apply(self.catagorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unqiue_tags = set(list(all_tags))


    def catagorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif line_count <= 10:
            return "Medium"
        else:
            return "Long"
        
    def get_tags(self):
        return self.unqiue_tags

    def get_filter_post(self,length,language,tag):
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags)) 
        ]
        return df_filtered.to_dict(orient="records")


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filter_post("Long", "English", "Web Development")
    
