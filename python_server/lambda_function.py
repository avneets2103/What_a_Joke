import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import pickle
import emoji
import re
import textblob as tb
import spacy as sp
import numpy as np
import math
from gensim.models import Word2Vec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.static_folder = 'public'

# Load models
nlp = sp.load("en_core_web_sm")

# offense models
offense_model_path = os.path.join(os.path.dirname(__file__), 'ai_models/offense_model.pkl')
with open(offense_model_path, 'rb') as f:
    offense_model = pickle.load(f)

offense_w2v_path = os.path.join(os.path.dirname(__file__), 'ai_models/offense_w2v.model')
w2v_model_offense = Word2Vec.load(offense_w2v_path)

# humor models
humor_model_path = os.path.join(os.path.dirname(__file__), 'ai_models/humor_model.pkl')
with open(humor_model_path, 'rb') as f:
    humor_model = pickle.load(f)

humor_w2v_path = os.path.join(os.path.dirname(__file__), 'ai_models/humor_w2v.model')
w2v_model_humor = Word2Vec.load(humor_w2v_path)

# Slang dictionary
slang_dict = {
    "AFAIK": "As Far As I Know", "AFK": "Away From Keyboard", "ASAP": "As Soon As Possible",
    # (Add the full dictionary here)
}

# Joke analysis logic
def convert_emojis_and_remove_colons(text):
    text_with_emojis = emoji.demojize(text)
    return re.sub(r':(\w+):', r'\1', text_with_emojis)

def tokenize_text(text):
    if isinstance(text, str):
        doc = nlp(text)
        return [token.text for token in doc]
    return []

def average_vector(tokens, model):
    vectors = [model.wv[token] for token in tokens if token in model.wv]
    if not vectors:
        return np.zeros(model.vector_size)
    return np.mean(vectors, axis=0)

def preprocess_joke(joke, model, w2v_model):
    for slang, replacement in slang_dict.items():
        joke = joke.replace(slang, replacement)
    joke = joke.lower()
    joke = convert_emojis_and_remove_colons(joke)
    joke = str(tb.TextBlob(joke).correct())
    tokens = tokenize_text(joke)
    input_vector = average_vector(tokens, w2v_model)
    input_vector = input_vector.reshape(1, 1, input_vector.shape[0])
    return input_vector

def joke_analyse(joke):
    offense_input = preprocess_joke(joke, offense_model, w2v_model_offense)
    offense_score = math.ceil((offense_model.predict(offense_input)) * 100)

    humor_input = preprocess_joke(joke, humor_model, w2v_model_humor)
    humor_score = max(0, min(100, math.ceil((humor_model.predict(humor_input)))))

    return {
        "message": "Joke analysis done!",
        "humorScore": humor_score,
        "offenseScore": offense_score,
        "joke": joke
    }, 201

# Define routes
@app.route('/api/v1/auth/jokeAnalysis', methods=['POST'])
def analyze_joke():
    data = request.get_json()
    joke = data.get('joke')
    return joke_analyse(joke)

# Connect DB and start server
def connect_db_and_start_server():
    try:
        port = os.getenv("PORT") or 8000
        print(f"Server listening on port {port}")
        app.run(debug=True, port=int(port))
    except Exception as err:
        print("App didn't launch!", err)

def lambda_handler(event, context):   
    connect_db_and_start_server()