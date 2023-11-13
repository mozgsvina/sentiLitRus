import pandas as pd
sent_scores = pd.read_csv("static/emo_vectores_602_loc_md.csv")

# checks if the words is associated with the emotional label
def is_emo(lemma, label):
    score = sent_scores[sent_scores["lemma"] == lemma][label]
    return score.values[0] > 0.4

# returns all emotional words from a list of words for particular emotion label
def get_emo_words(story_lemmas, label):
    emo_words = [l for l in story_lemmas if l in sent_scores.lemma.values and is_emo(l, label)]
    return emo_words

lemmas_per_story_df = pd.read_csv("data/lemmatized_stories.csv")

lemmas_per_story_dict = {}
for index, row in lemmas_per_story_df.iterrows():
    story_id = row['StoryID']
    lemmas = row['lemmas'].split()
    lemmas_per_story_dict[story_id] = lemmas

all_lemmas = []
for idx in lemmas_per_story_dict:
    all_lemmas.extend(lemmas_per_story_dict[idx])

unique_lemmas = list(set(all_lemmas))

print(f"The number of words in the corpus: {len(all_lemmas)}")
print(f"The number of unique lemmas in the corpus: {len(unique_lemmas)}")

labels = list(sent_scores.columns)[1:]  # ["happy", "pleas", "cont", "pride", "relief", "amuse', 'surp', 'sad', 'fear', 'disgust', 'shame', 'anger']

emo_dict = {}

for emotion in labels:
    print(f"Creating list of {emotion} words")
    emo_words = [w for w in unique_lemmas if is_emo(w, emotion)]
    emo_dict[emotion] = emo_words


# join scores and corpus frequencies for all emotional words per each emotion

emo_data = {}

for emo_label in emo_dict:
    emo_lexicon = []
    for word in emo_dict[emo_label]:
        w_count = all_lemmas.count(word)
        w_score = sent_scores[sent_scores["lemma"] == word][emo_label].values[0]
        emo_lexicon.append({
            "lemma": word,
            "freq": w_count,
            "score": w_score,
        })
    emo_data[emo_label]  = emo_lexicon

# emo_data

data = {
    'emotion': [],
    'number_of_lemmas': []
}

for emotion, lemma_list in emo_data.items():
    data['emotion'].append(emotion)
    data['number_of_lemmas'].append(len(lemma_list))

df = pd.DataFrame(data)
df.to_csv("results/emo_words_count.csv", index=False)

# save lexicons to csv
for emotion in emo_data:
    df = pd.DataFrame(emo_data[emotion])
    df.to_csv(f"results/{emotion}_lexicon.csv", index=False)

# count frequencies and scores per story

from math import sqrt

data_per_stories = {}

for emotion in emo_data:
    print(emotion.upper())
    emo_lex = [item["lemma"] for item in emo_data[emotion]]
    new_entry = []
    for i, story_id in enumerate(lemmas_per_story_dict):
        print(i + 1, "/", len(lemmas_per_story_dict), story_id)
        story_total_freq = 0
        story_emo_score = 0
        for word in emo_lex:
            word_freq = lemmas_per_story_dict[story_id].count(word)
            story_total_freq += word_freq
            word_score = sqrt(sent_scores[sent_scores["lemma"] == word][emotion].values[0])
            story_emo_score += word_score * word_freq

        new_entry.append({
            "StoryID": story_id,
            "story_freq": story_total_freq,
            "story_emo_score": story_emo_score,
        })
    data_per_stories[emotion] = new_entry




lemmas_per_story_df["n_words"] = lemmas_per_story_df["lemmas"].apply(lambda x: len(x.split()))
for emotion in data_per_stories:
    df = pd.DataFrame(data_per_stories[emotion])
    df.story_emo_score = df.story_emo_score.round(3)
    merged_df = pd.merge(df, lemmas_per_story_df[["StoryID", "FILE NAME", "n_words"]], on="StoryID", how="left")
    # merged_df = merged_df.reset_index(drop=True)

    merged_df.to_csv(f"results/{emotion}_per_story_sqrt.csv", index=False)




