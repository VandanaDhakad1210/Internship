import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import random

# Download NLTK data (only first time)
# nltk.download('punkt')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# ------------------------
# TRAINING DATA (Intents)
# ------------------------
intents = {
    "greeting": {
        "examples": ["hello", "hi", "hey", "good morning", "good evening"],
        "responses": ["Hello!", "Hi there!", "Greetings!", "How can I help you today?"]
    },
    "goodbye": {
        "examples": ["bye", "goodbye", "see you", "exit", "quit"],
        "responses": ["Goodbye!", "See you later!", "Have a great day!", "Bye!"]
    },
    "thanks": {
        "examples": ["thanks", "thank you", "appreciate it"],
        "responses": ["You're welcome!", "No problem!", "Happy to help!"]
    },
    "name": {
        "examples": ["what is your name", "who are you", "your name"],
        "responses": ["I'm a simple chatbot built with NLTK!", "You can call me ChatBot."]
    },
    "unknown": {
        "responses": ["Sorry, I didn’t understand that.", "Can you rephrase?", "I'm not sure how to respond to that."]
    }
}

# ------------------------
# NLP FUNCTIONS
# ------------------------
def preprocess(sentence):
    tokens = word_tokenize(sentence.lower())
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized

def classify_intent(user_input):
    user_tokens = preprocess(user_input)

    for intent, data in intents.items():
        for example in data.get("examples", []):
            example_tokens = preprocess(example)
            if set(example_tokens).intersection(user_tokens):
                return intent

    return "unknown"

def generate_response(intent):
    return random.choice(intents[intent]["responses"])

# ------------------------
# CHAT LOOP
# ------------------------
def chat():
    print("ChatBot: Hello! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("ChatBot: Goodbye!")
            break

        intent = classify_intent(user_input)
        response = generate_response(intent)
        print(f"ChatBot: {response}")

# ------------------------
# RUN CHATBOT
# ------------------------
if __name__ == "__main__":
    chat()
