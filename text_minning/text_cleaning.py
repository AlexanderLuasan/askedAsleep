
from nltk.corpus import stopwords
from textblob import Word
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