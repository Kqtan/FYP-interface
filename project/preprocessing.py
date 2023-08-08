import re
import pandas as pd
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
from keras_preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf
from spellchecker import SpellChecker

with open('lstm_tokenizer.pickle', 'rb') as handle:
    w_tokenizer = pickle.load(handle)

with open('spam_tokenizer.pickle', 'rb') as handle:
    sw_tokenizer = pickle.load(handle)

bi_lstm = tf.keras.models.load_model("bi_lstm.h5")
spam_lstm = tf.keras.models.load_model("spam_lstm.h5")

def remove_emoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags = re.UNICODE)
    return emoji_pattern.sub(r'', text)

def word_processor(text, the_file, the_list):    
    words = []
    for word in word_tokenize(text):
        if word in the_list:
            words += the_file[word].split()
        else:
            words += word.split()
    return " ".join(words)

def spelling(text):
    spell = SpellChecker()
    word_list = word_tokenize(text)
    correct_word_list = []
    for word in word_list:
        if word in spell.unknown(word_list):
            corrected_word = spell.correction(word)
            if corrected_word is None:
                correct_word_list.append(word)
            else:
                correct_word_list.append(corrected_word)
        else:
            correct_word_list.append(word)
    
    return " ".join(correct_word_list)

def remove_stop_words(text):
    text = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    # stemming + only word + remove stop words
    text = [lemmatizer.lemmatize(word) for word in text if word.isalpha() and not word in stop_words]

    return ' '.join(text)


acronyms = pd.read_json("acronyms.json", typ="series")
acronyms_list = list(acronyms.keys())

contraction = pd.read_json("contraction.json", typ="series")
contraction_list = list(contraction.keys())

lemmatizer = WordNetLemmatizer()
def text_normaliser(text):
    # text = word_tokenize(text.lower())
    text = text.lower().strip()

    # convert text to one line
    text = re.sub("\n", "", text)
    text = re.sub("\[.*?\]", "", text)

    # remove html tags
    html_tags = re.compile(r"<.*?>")
    text = html_tags.sub(r"", text)

    # remove http
    http = "https?://\S+|www\.\S+"
    pattern = r"({})".format(http)
    text = re.sub(pattern, "", text)

    # remove emojis
    text = remove_emoji(text)

    # to remove ' for the future processing like contraction
    punct = string.punctuation.replace("'", "") 
    text = text.translate(str.maketrans("", "", punct))

    # check spelling
    text = spelling(text)
    # problem: example like Ecommerce is being corrected
    # might cause a problem for the overall performance

    # remove acronyms
    text = word_processor(text, acronyms, acronyms_list)

    # contraction of words
    text = word_processor(text, contraction, contraction_list)

    # removing stop words
    text = remove_stop_words(text)
    return text

# for spam filter
def predict_spam(text, SEQ_LEN):
    df = pd.DataFrame({"text": [text]})
    x = df.apply(lambda row: text_normaliser(row['text']), axis=1)

    sequences = sw_tokenizer.texts_to_sequences(x)

    data = pad_sequences(sequences, maxlen=SEQ_LEN)

    predicted_probs = spam_lstm.predict(data)
    y_pred = (predicted_probs >= 0.8).astype(int)
    
    label_list = ["Ham", "Spam"]
    return label_list[y_pred[0][0]]

# for categorising
def predict_category(text, SEQ_LEN):
    df = pd.DataFrame({"text": [text]})
    x = df.apply(lambda row: text_normaliser(row['text']), axis=1)

    sequences = w_tokenizer.texts_to_sequences(x)

    data = pad_sequences(sequences, maxlen=SEQ_LEN)

    y_pred = np.argmax(bi_lstm.predict(data), axis=-1)
    label_list = ["World", "Sports", "Business", "Sci/Tech"]
    return label_list[y_pred[0]]

