import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Initialize chatbot
chatbot = ChatBot('TravelBot')

# Define the path to the training data JSON file
DATA_FILE = r"C:\travel_agency\travel_agency\travel_app\storage\training_data.json"

# Load training data
with open(DATA_FILE, 'r', encoding='utf-8') as file:
    training_data = json.load(file)

# Train chatbot
trainer = ListTrainer(chatbot)
for question, answer in training_data.items():
    trainer.train([question, answer])

print("Training completed!")
