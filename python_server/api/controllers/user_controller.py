import pickle
import emoji
import re
import textblob as tb
import spacy as sp
import numpy as np
import math
from gensim.models import Word2Vec
import os
# from tensorflow.keras.models import load_model

# with open('path/to/humor_model.pkl', 'rb') as humor_model_file:
#     humor_model = pickle.load(humor_model_file)

offense_model_path = os.path.join(os.path.dirname(__file__), '../ai_models/offense_model.pkl')
with open(offense_model_path, 'rb') as f:
    offense_model = pickle.load(f)

offense_w2v_path = os.path.join(os.path.dirname(__file__), '../ai_models/offense_w2v.model')
w2v_model_offense = Word2Vec.load(offense_w2v_path)

slang_dict = {
    "AFAIK": "As Far As I Know",
    "AFK": "Away From Keyboard",
    "ASAP": "As Soon As Possible",
    "ATK": "At The Keyboard",
    "ATM": "At The Moment",
    "A3": "Anytime, Anywhere, Anyplace",
    "BAK": "Back At Keyboard",
    "BBL": "Be Back Later",
    "BBS": "Be Back Soon",
    "BFN": "Bye For Now",
    "B4N": "Bye For Now",
    "BRB": "Be Right Back",
    "BRT": "Be Right There",
    "BTW": "By The Way",
    "B4": "Before",
    "CU": "See You",
    "CUL8R": "See You Later",
    "CYA": "See You",
    "FAQ": "Frequently Asked Questions",
    "FC": "Fingers Crossed",
    "FWIW": "For What It's Worth",
    "FYI": "For Your Information",
    "GAL": "Get A Life",
    "GG": "Good Game",
    "GN": "Good Night",
    "GMTA": "Great Minds Think Alike",
    "GR8": "Great!",
    "G9": "Genius",
    "IC": "I See",
    "ICQ": "I Seek you",
    "ILU": "I Love You",
    "IMHO": "In My Honest/Humble Opinion",
    "IMO": "In My Opinion",
    "IOW": "In Other Words",
    "IRL": "In Real Life",
    "KISS": "Keep It Simple, Stupid",
    "LDR": "Long Distance Relationship",
    "LMAO": "Laughing My A.. Off",
    "LOL": "Laughing Out Loud",
    "LTNS": "Long Time No See",
    "L8R": "Later",
    "MTE": "My Thoughts Exactly",
    "M8": "Mate",
    "NRN": "No Reply Necessary",
    "OIC": "Oh I See",
    "PITA": "Pain In The A..",
    "PRT": "Party",
    "PRW": "Parents Are Watching",
    "QPSA?": "Que Pasa?",
    "ROFL": "Rolling On The Floor Laughing",
    "ROFLOL": "Rolling On The Floor Laughing Out Loud",
    "ROTFLMAO": "Rolling On The Floor Laughing My A.. Off",
    "SK8": "Skate",
    "STATS": "Your sex and age",
    "ASL": "Age, Sex, Location",
    "THX": "Thank You",
    "TTFN": "Ta-Ta For Now!",
    "TTYL": "Talk To You Later",
    "U": "You",
    "U2": "You Too",
    "U4E": "Yours For Ever",
    "WB": "Welcome Back",
    "WTF": "What The F...",
    "WTG": "Way To Go!",
    "WUF": "Where Are You From?",
    "W8": "Wait...",
    "7K": "Sick:-D Laugher",
    "TFW": "That feeling when",
    "MFW": "My face when",
    "MRW": "My reaction when",
    "IFYP": "I feel your pain",
    "TNTL": "Trying not to laugh",
    "JK": "Just kidding",
    "IDC": "I don’t care",
    "ILY": "I love you",
    "IMU": "I miss you",
    "ADIH": "Another day in hell",
    "ZZZ": "Sleeping, bored, tired",
    "WYWH": "Wish you were here",
    "TIME": "Tears in my eyes",
    "BAE": "Before anyone else",
    "FIMH": "Forever in my heart",
    "BSAAW": "Big smile and a wink",
    "BWL": "Bursting with laughter",
    "BFF": "Best friends forever",
    "CSL": "Can’t stop laughing"
}
nlp = sp.load("en_core_web_sm")

def offense_preprocess_joke(joke):
    # Replace slangs using the dictionary
    for slang, replacement in slang_dict.items():
        joke = joke.replace(slang, replacement)
    
    # Convert to lowercase
    joke = joke.lower()
    
    # Convert emojis and remove colons
    def convert_emojis_and_remove_colons(text):
        text_with_emojis = emoji.demojize(text)
        return re.sub(r':(\w+):', r'\1', text_with_emojis)
    
    joke = convert_emojis_and_remove_colons(joke)
    
    # Text correction
    blob = tb.TextBlob(joke)
    joke = str(blob.correct())
    
    # Tokenize using spaCy
    def tokenize_text(text):
        if isinstance(text, str):
            doc = nlp(text) 
            return [token.text for token in doc]
        else:
            return []
    tokens = tokenize_text(joke)
    
    # w2v
    def average_vector(tokens, model):
        vectors = []
        for token in tokens:
            if token in model.wv:
                vectors.append(model.wv[token])
        # If no vectors are found, return a zero vector
        if not vectors:
            return np.zeros(model.vector_size)
        # Calculate the average
        return np.mean(vectors, axis=0)
    input = average_vector(tokens, w2v_model_offense)
    input = input.reshape(-1, 1)  # Reshape to (100, 1)
    input = input.reshape(1, 1, input.shape[0])  # Reshape to (1, 1, 100)
    
    return input

def joke_analyse(request):
    data = request.get_json()
    joke = data.get('joke')

    # Preprocess the joke
    # processed_joke = preprocess_joke(joke)

    # Predict humor score
    # humorScore = humor_model.predict([processed_joke])[0]  # Assuming your model requires a list

    # offense processing
    offense_processed_joke = offense_preprocess_joke(joke)

    # Predict offense score
    offenseScore = math.ceil((offense_model.predict(offense_processed_joke))*100) # Same assumption as above

    return {
        "message": "Joke analysis done!",
        "humorScore": 0,
        "offenseScore": offenseScore,
        "joke": joke
    }, 201
