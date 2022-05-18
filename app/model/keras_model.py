import pandas as pd
import numpy as np
from tensorflow import keras
from model.prepocessing import preprocessing
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def predict(df):
    model = keras.models.load_model("../code/app/model/keras_model.h5")
    df = preprocessing(df)
    tokenizer = Tokenizer(nb_words=15729)
    tokenizer.fit_on_texts(df["clean_text"])
    df["text_encode"] = tokenizer.texts_to_sequences(df["clean_text"])
    padded_sequence = pad_sequences(df["text_encode"], padding='post')
    prediction = model.predict(padded_sequence)
    df["predict"] = np.argmax(prediction, axis = 1)
    categories = {0:'sadness', 1:'surprise', 2:'anger', 3:'fear' , 4:'happy', 5:'love'}
    return(df["predict"].map(categories))