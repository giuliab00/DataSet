from datetime import datetime
import threading
import os
import time
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define model versions to be used
model = ""

# Lock for thread-safe file writing
file_lock = threading.Lock()

# Function to get completion from OpenAI chat model
def get_completion_from_messages(messages, model="", temperature=1, max_tokens=100):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

# Custom OpenAI class definition
class OpenAImethods:
    def __init__(self, language):
        # Initialize instance variables based on input parameters
        self.language = "English"
        self.log_file = "trial_log.txt"