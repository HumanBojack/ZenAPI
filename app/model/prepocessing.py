import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from keras.preprocessing.text import Tokenizer
from keras.layers import TextVectorization
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import string 

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    lemmatizer = WordNetLemmatizer()
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            lemmatized_sentence.append(word)
        else:
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)

def cleaning(sentence, stop_words):
  sentence = re.sub("[^-9A-Za-z ]", "" , sentence)
  sentence = "".join([i.lower() for i in sentence if i not in string.punctuation])
  sentence = " ".join(word_tokenize(sentence))
  sentence = " ".join([i for i in sentence.split(" ") if i not in stop_words])
  return(sentence)

def preprocessing(data , categories = {'sadness' : 0, 'surprise' : 1, 'anger' : 2, 'fear' :3, 'happy' : 4, 'love' : 5}):
  stop_words = set(stopwords.words('english'))

  data['clean_text'] = data['text'].apply(lambda x : cleaning(x, stop_words))
  data['clean_text'] = data['clean_text'].apply(lambda x : lemmatize_sentence(x))
  
#   data["target"] = data["Emotion"].map(categories)
  return(data)
