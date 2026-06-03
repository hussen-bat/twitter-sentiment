import pickle
import re
import nltk
from flask import Flask, render_template, request, jsonify
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open('trained_model.sav', 'rb'))
vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

post_stem = PorterStemmer()
stop_words = set(stopwords.words('english'))


def preprocess(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower().split()
    text = [post_stem.stem(word) for word in text if word not in stop_words]
    return ' '.join(text)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    tweet = ''
    confidence = None
    if request.method == 'POST':
        tweet = request.form.get('tweet', '').strip()
        if tweet:
            processed = preprocess(tweet)
            vector = vectorizer.transform([processed])
            prediction = model.predict(vector)[0]
            proba = model.predict_proba(vector)[0]
            confidence = round(max(proba) * 100, 1)
            result = 'Positive' if prediction == 1 else 'Negative'
    return render_template('index.html', result=result, tweet=tweet, confidence=confidence)


@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint for AJAX calls"""
    data = request.get_json()
    tweet = data.get('tweet', '').strip()
    if not tweet:
        return jsonify({'error': 'No tweet provided'}), 400

    processed = preprocess(tweet)
    vector = vectorizer.transform([processed])
    prediction = model.predict(vector)[0]
    proba = model.predict_proba(vector)[0]
    confidence = round(max(proba) * 100, 1)
    result = 'Positive' if prediction == 1 else 'Negative'

    return jsonify({
        'result': result,
        'confidence': confidence,
        'tweet': tweet
    })


if __name__ == '__main__':
    app.run(debug=True)
