# import torch
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import RobertaTokenizer, RobertaForSequenceClassification, RobertaConfig

# # Initialize Flask app
# app = Flask(__name__)

# # Enable CORS
# CORS(app)

# # Load the sentiment analysis model and tokenizer
# model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
# tokenizer = RobertaTokenizer.from_pretrained(model_name)
# config = RobertaConfig.from_pretrained(model_name)
# model = RobertaForSequenceClassification.from_pretrained(model_name, config=config)

# # Function to calculate the sentiment score
# def get_sentiment_scores(text):
#     # Tokenize the input text
#     inputs = tokenizer(
#         text,
#         truncation=True,
#         padding=True,
#         max_length=512,
#         return_tensors="pt",
#         clean_up_tokenization_spaces=True
#     )
#     # Get the model's output
#     with torch.no_grad():  # Avoid computing gradients
#         outputs = model(**inputs)
#     # Extract the logits (raw model predictions)
#     logits = outputs.logits
#     # Convert logits to probabilities using softmax
#     probabilities = torch.softmax(logits, dim=1)
#     # Ensure indices are correct based on model's labels
#     positive_score = probabilities[0][2].item()  # Index 2 corresponds to positive sentiment
#     negative_score = probabilities[0][0].item()  # Index 0 corresponds to negative sentiment
#     # Calculate the normalized sentiment score (-1 to 1)
#     normalized_score = positive_score - negative_score
#     return normalized_score

# def g(text):
#         return normalized_score



# # API endpoint to analyze sentiment
# @app.route('/analyze', methods=['POST'])
# def analyze_sentiment():
#     # Get the text from the request JSON payload
#     data = request.get_json()
#     text = data.get("text")
    
#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     try:
#         # Calculate the sentiment score
#         sentiment_score = round(get_sentiment_scores(text), 4)
#         sas = g()
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
#     # Return the result as JSON
#     return jsonify({"text": text, "sentiment_score": sentiment_score})

# # Main entry point to run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)

import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import RobertaTokenizer, RobertaForSequenceClassification, RobertaConfig

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Load the sentiment analysis model and tokenizer
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = RobertaTokenizer.from_pretrained(model_name)
config = RobertaConfig.from_pretrained(model_name)
model = RobertaForSequenceClassification.from_pretrained(model_name, config=config)

# Function to calculate the sentiment score
def get_sentiment_scores(text):
    # Tokenize the input text
    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=512,
        return_tensors="pt",
        clean_up_tokenization_spaces=True
    )
    # Get the model's output
    with torch.no_grad():  # Avoid computing gradients
        outputs = model(**inputs)
    # Extract the logits (raw model predictions)
    logits = outputs.logits
    # Convert logits to probabilities using softmax
    probabilities = torch.softmax(logits, dim=1)
    # Ensure indices are correct based on model's labels
    positive_score = probabilities[0][2].item()  # Index 2 corresponds to positive sentiment
    negative_score = probabilities[0][0].item()  # Index 0 corresponds to negative sentiment
    # Calculate the normalized sentiment score (-1 to 1)
    normalized_score = positive_score - negative_score
    return normalized_score

# API endpoint to analyze sentiment
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    # Get the text from the request JSON payload
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Calculate the sentiment score
        sentiment_score = round(get_sentiment_scores(text), 4)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Return the result as JSON
    return jsonify({"text": text, "sentiment_score": sentiment_score})

# Main entry point to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

