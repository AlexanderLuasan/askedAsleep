
from nltk.corpus import stopwords
from textblob import Word
import json

import pandas as pd

stop = stopwords.words('english')

punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~“”’'''

def lower(data):
    return map( lambda x:x.lower() ,data)

def remove_punc(data):
    for x in punctuation:
        data = data.replace(x,'')
    return data
def drop_stop_words(data):
    return " ".join(x for x in data.split(" ") if x not in stop)

def lemmatization(data):
    return " ".join(Word(x).lemmatize() for x in data.split(" "))

def clean(data):
    data = "".join(lower(data))
    data = remove_punc(data)
    data = drop_stop_words(data)
    data = lemmatization(data)
    return data




def get_json_data():
    all_trivia = None
    with open("data/all.json",'r') as f:
        all_trivia = json.load(f) 
    return all_trivia

def question_frame(all_trivia):

    question_text_list = [q["question_text"] for q in all_trivia]

    return pd.DataFrame(question_text_list,columns=["raw"])


if __name__ == "__main__":
    qs = get_json_data()
    df = question_frame(qs)
    print(df.head())