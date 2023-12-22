from flask import Flask, render_template, request
from sklearn.svm import SVC
import pandas as pd

# Preprocessing importation
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk import PorterStemmer
from nltk import tokenize
import string

# Data Transformation
from sklearn.feature_extraction.text import CountVectorizer

data1 = pd.read_csv('/SMS_spam_detection/Dataset/spam1.csv', encoding="ISO-8859-1")
data2 = pd.read_csv('/SMS_spam_detection/Dataset/spam2.csv', encoding="ISO-8859-1")

# Drop null columns
data1.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis = 1, inplace = True)
data1.columns = ['labels', 'text']
data2 = data2[data2['labels'] == 'spam']
data = pd.concat([data1, data2])
data['label_enc'] = data['labels'].map({'ham':0,'spam':1})
data.drop(['labels'], axis = 1, inplace = True)

# Preprocess
SW = stopwords.words("english") + ['u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']

def preprocess_text(text):

    """
    String text in input, remove its punctuation and stopwords.
    Return the cleaned text
    """
    text = text.strip()
    text = text.lower()

    words = tokenize.word_tokenize(text)

    ps = PorterStemmer()

    filter_words = [ps.stem(word) for word in words if word not in SW and word.isalnum()]

    transformed_text = " ".join(filter_words)

    return transformed_text

data["cleaned text"] = data["text"].apply(preprocess_text)

# Count Vectorizer
Vect = CountVectorizer()

X_vect = Vect.fit_transform(data["cleaned text"]).toarray()
y_vect = data['label_enc']

# Model
model = SVC(C = 1000, gamma = 0.1, kernel = 'rbf')
model.fit(X_vect, y_vect)

app = Flask(__name__)

def classify_message(message):
    mes = message.apply(preprocess_text)
    mes = Vect.transform(mes).toarray()
    if model.predict(mes) == 1:
        return True
    else:
        return False
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_spam', methods=['POST'])
def check_spam():
    user_message = request.form['userMessage']
    is_spam = classify_message(user_message)
    return {'is_spam': is_spam}

if __name__ == '__main__':
    app.run(debug=True)
