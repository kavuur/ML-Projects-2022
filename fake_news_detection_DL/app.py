from flask import Flask, request, url_for, redirect, render_template, jsonify
import warnings

warnings.filterwarnings('ignore')
from googletrans import Translator
from tensorflow.keras.models import load_model
import nltk
from tensorflow.keras.preprocessing.sequence import pad_sequences
from textblob import TextBlob
import numpy as np
import pickle
import os

app = Flask(__name__)

maxlen = 700
verbose = True


def print_s(obj, verbose=False):
    """Initial stage printing in terminal"""
    if verbose:
        if obj == 'model':
            print("Loading LSTM W2V Model...")
        elif obj == 'enc':
            print("Loading Encoder...")
        elif obj == 'pre':
            print("Preprocessing the news...")
        elif obj == 'trans':
            print("Transforming the news...")
    else:
        return


def print_f(obj, verbose=False):
    """Completed stages printing in terminal"""
    if verbose:
        if obj == 'model':
            print("LSTM W2V Model loading complete!")
        elif obj == 'enc':
            print("Encoder loading complete!")
        elif obj == 'pre':
            print("Preprocessing complete!")
        elif obj == 'trans':
            print("Transforming complete!")
    else:
        return


def loadModels(model_path, encoder_path, verbose=False):
    """Encoder and model loading"""
    model_path = os.path.join(model_path, "model_v1.h5")
    encoder_path = os.path.join(encoder_path, "tokenizer.h5")
    print_s('model', verbose)
    model = load_model(model_path)
    print_f('model', verbose)
    print_s('enc', verbose)
    with open(encoder_path, 'rb') as pickle_file:
        encoder = pickle.load(pickle_file)
    print_f('enc', verbose)
    return model, encoder


def count_words(txt):
    """Word count generation"""
    words = txt.split()
    return len(words)


def preprocess(par, verbose=False):
    """Pre-processing text"""
    print_s('pre', verbose)
    X = []
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tmp = []
    sentences = nltk.sent_tokenize(par)
    for sent in sentences:
        sent = sent.lower()
        tokens = tokenizer.tokenize(sent)
        filtered_words = [w.strip() for w in tokens if w not in stop_words and len(w) > 1]
        tmp.extend(filtered_words)
    print_f('pre', verbose)
    return tmp


def transform(X, maxlen, verbose=False):
    """Vector transformation"""
    print_s('trans', verbose)
    tmp = np.array(X)
    tmp = tmp.reshape(1, tmp.shape[0])
    X = encoder.texts_to_sequences(tmp.tolist())
    print_f('trans', verbose)
    return pad_sequences(X, maxlen)


def translate_news(txt):
    """Google Translation API"""
    trans_obj = []
    to_translate = txt

    translator = Translator()
    locale = (translator.detect(to_translate)).lang
    translated = (translator.translate(to_translate, dest='en', src='auto')).text
    trans_obj.append(locale)
    trans_obj.append(to_translate)
    trans_obj.append(translated)
    return trans_obj


def sentiment_analysis(txt):
    """Sentiment analysis"""
    sent_arr = []
    polarity = TextBlob(str(txt)).sentiment.polarity
    subjectivity = TextBlob(str(txt)).sentiment.subjectivity
    sentiment = np.select([polarity < 0, polarity == 0, polarity > 0], ['neg', 'neu', 'pos'])

    sent_arr.append(polarity)
    sent_arr.append(subjectivity)
    sent_arr.append(sentiment)

    return sent_arr


def predict_news(txt, maxlen, clf_model, txt_encoder, verbose=False):
    translated = translate_news(txt)
    X = preprocess(translated[2], verbose)
    X = transform(X, maxlen, verbose)
    print_s(verbose, 'pred')
    y = clf_model.predict(X)

    if y > 0.5:
        return "{:3f}% confidence. News content is reliable.".format(y[0][0] * 100)
    else:
        return "{:3f}% confidence. News content is unreliable.".format(y[0][0] * 100)


model, encoder = loadModels('models', 'models', verbose=verbose)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict', methods=['POST'])
def predict():
    data = dict(request.form)
    inner_data = data['News']
    x = translate_news(inner_data)
    y = predict_news(inner_data, maxlen, model, encoder, verbose=verbose)
    z = sentiment_analysis(x[2])
    wrdz = count_words(x[2])
    if x[0] != 'en':
        return render_template('home.html', loc='Detected locale: ({})'.format(x[0]),
                               pred='{}'.format(y), w_count='Word count: {}'.format(wrdz),
                               trans='{}'.format(x[2]),
                               sentiment='Polarity: {:.3f}, Subjectivity: {:.3f}, Sentiment: {}'.format(z[0], z[1],
                                                                                                        z[2]))
    else:
        return render_template('home.html', loc='Detected locale: ({})'.format(x[0]),
                               pred='{}'.format(y), w_count='Word count: {}'.format(wrdz),
                               sentiment='Polarity: {:.3f}, Subjectivity: {:.3f}, Sentiment: {}'.format(z[0], z[1],
                                                                                                        z[2]))


if __name__ == '__main__':
    app.run(debug=True)
