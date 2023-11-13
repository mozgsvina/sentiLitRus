import pandas as pd
from math import sqrt

sent_scores = pd.read_csv("static/emo_vectores_602_loc_md.csv")

# checks if the words is associated with the emotional label
def is_emo(lemma, label):
    score = sent_scores[sent_scores["lemma"] == lemma][label]
    return score.values[0] > 0.4

# returns all emotional words from a list of words for particular emotion label
def get_emo_words(story_lemmas, label):
    emo_words = [l for l in story_lemmas if l in sent_scores.lemma.values and is_emo(l, label)]
    return emo_words


def get_emo_words(lemmas, labels):
    emo_dict = {}
    for emotion in labels:
        print(f"Creating list of {emotion} words")
        emo_words = [w for w in lemmas if is_emo(w, emotion)]
        emo_dict[emotion] = emo_words
    return emo_dict


# takes result of get_emo_words
def get_scores_and_freqs(emo_lemmas: dict, all_lemmas):
    emo_data = {}
    for emo_label in emo_lemmas:
        emo_lexicon = []
        for word in emo_lemmas[emo_label]:
            w_count = all_lemmas.count(word)
            w_score = sent_scores[sent_scores["lemma"] == word][emo_label].values[0]
            emo_lexicon.append({
                "lemma": word,
                "freq": w_count,
                "score": w_score,
            })
        emo_data[emo_label]  = emo_lexicon
    return emo_data


# takes result of get_scores_and_freqs
def count_emo_words_total_freq(scores_and_freqs):
    print(scores_and_freqs)

    data = {
        'emotion': [],
        'number_of_lemmas': []
    }

    for emotion, lemma_list in scores_and_freqs.items():
        data['emotion'].append(emotion)
        data['number_of_lemmas'].append(len(lemma_list))

    return data

# TODO process unknown words and add different formulas
def get_score_per_story(lemmas_per_story_dict, emo_data):

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
            story_len = len(lemmas_per_story_dict[story_id])
            story_emo_score = story_emo_score / story_len * 100

            new_entry.append({
                "StoryID": story_id,
                "story_freq": story_total_freq,
                "story_emo_score": story_emo_score,
            })
        data_per_stories[emotion] = new_entry
    
    return data_per_stories