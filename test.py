import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from natsort import natsorted

# Paths to training and validation datasets
root_train = "C:\\Users\\Research chair\\Desktop\\Roken Alhewar Datasset\\latest_dataset(en)\\train (80)"
root_validation = "C:\\Users\\Research chair\\Desktop\\Roken Alhewar Datasset\\latest_dataset(en)\\validation (20)"
categories = ["Accepted_Islam_splits - Copy", "Wants_to_Convert_splits - Copy", "Interested_in_Islam_splits - Copy"]


# Load and preprocess data using natsorted

def stopwords_removal(text):
    # Define a list of stop words
    stop_words = [
        "i", "on", "in", "the", "is", "am", "are", "a", "an", "and", "to", "of", "for", "with", "it", "that", "this",
        "you", "he", "she", "we", "they", "them", "as", "at", "by", "from", "or", "but", "so", "if", "then"
    ]

    filtered_text = []
    for sentence in text:
        words = sentence.split()  # Split the sentence into words
        # Remove words that are in the stop_words list
        filtered_sentence = " ".join([word for word in words if word.lower() not in stop_words])
        filtered_text.append(filtered_sentence)
    return filtered_text

def load_data(root, categories):
    data = []
    y = []
    for category in categories:
        category_path = os.path.join(root, category)

        # Use natsorted to sort files in natural order
        sorted_files = natsorted(os.listdir(category_path))

        for filename in sorted_files:
            file_path = os.path.join(category_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data.append(json.load(file))  # Add entire conversation for processing
                y.append(category)  # Add the category label
    print(data)
    return data, y

# Extract messages and sentiment scores from the dataset
def extract_messages(data):
    X = []
    for conversation in data:
        messages = []
        for msg in conversation['messages']:
            if "Visitor" in msg:
                sender = "Visitor"  # Set sender as 'Visitor'
            elif "Daei" in msg:
                sender = "Daei"  # Set sender as 'Daei'
            message = f"{sender}: {msg['message']}"  # Prepend the sender to the message
            messages.append(message)
        X.append(" ".join(messages))  # Join all messages in the conversation
    return X


# Extract sentiment features (average sentiment score for each conversation)
def extract_numerical_features(data):
    sentiment_scores = []
    for conversation in data:
        scores = [msg['message_sentiment_score'] for msg in conversation['messages']]
        sentiment_scores.append(np.mean(scores))  # Average sentiment score
    return sentiment_scores


# Load training and validation data
train_data, y_train = load_data(root_train, categories)
val_data, y_val = load_data(root_validation, categories)

# Extract text messages from the conversations
X_train_text = extract_messages(train_data)
X_val_text = extract_messages(val_data)

# Remove stop words from the training and validation text data
X_train_text_filtered = stopwords_removal(X_train_text)
X_val_text_filtered = stopwords_removal(X_val_text)


# Tokenizer setup
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(X_train_text_filtered)
word_index = tokenizer.word_index
print("Word Index: ")
for word, index in word_index.items():
    print(f"{word}: {index}")
X_train_seq = tokenizer.texts_to_sequences(X_train_text)
X_val_seq = tokenizer.texts_to_sequences(X_val_text)

# Padding sequences to ensure uniform length
max_sequence_len = 500  # You can adjust this length based on your dataset
X_train_padded = pad_sequences(X_train_seq, maxlen=max_sequence_len, padding='post', truncating='post')
X_val_padded = pad_sequences(X_val_seq, maxlen=max_sequence_len, padding='post', truncating='post')

# Extract sentiment features
train_sentiments = extract_numerical_features(train_data)
val_sentiments = extract_numerical_features(val_data)

# Normalize the sentiment scores
scaler = MinMaxScaler()
train_sentiments_scaled = scaler.fit_transform(np.array(train_sentiments).reshape(-1, 1))
val_sentiments_scaled = scaler.transform(np.array(val_sentiments).reshape(-1, 1))

# Combine text (padded sequences) and sentiment features
X_train_combined = np.hstack([X_train_padded, train_sentiments_scaled])
X_val_combined = np.hstack([X_val_padded, val_sentiments_scaled])

# Encode the labels (categories)
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_val_encoded = label_encoder.transform(y_val)

# Convert labels to categorical (one-hot encoding)
y_train_categorical = to_categorical(y_train_encoded, num_classes=len(categories))
y_val_categorical = to_categorical(y_val_encoded, num_classes=len(categories))

# Reshape data for the LSTM (3D input: [samples, timesteps, features])
X_train_combined = np.expand_dims(X_train_combined, axis=-1)
X_val_combined = np.expand_dims(X_val_combined, axis=-1)