# lemmatize stories and save
# python -m spacy download ru_core_news_md

import ru_core_news_md
import pandas as pd
import os

# TODO define a function to lemmatize list of strings, call from main

PATH_TO_CORPUS = "data/sample_corpus/"
nlp = ru_core_news_md.load()

sample = os.listdir(PATH_TO_CORPUS)
text_data = {}

for i, story in enumerate(sample):
    with open(PATH_TO_CORPUS + story) as f:
        print(f"working with {i + 1} file out of {len(sample)}...")
        text = f.read().lower()
        lemmas = []
        doc = nlp(text)
        for token in doc:
            if token.is_alpha:
                lemmas.append(token.lemma_)
                text_data[story] = lemmas

ids = [title.split("_")[0] for title in sample]

files_lemmas_df = pd.DataFrame(list(text_data.items()), columns=["FILE NAME", "lemmas"])
files_lemmas_df["StoryID"] = ids
files_lemmas_df["lemmas"] = files_lemmas_df["lemmas"].apply(lambda x: " ".join(x))

files_lemmas_df.to_csv("data/lemmatized_stories.csv", index=False)

