from datetime import datetime
import threading
import os
import time
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


# Load environment variables from .env file
load_dotenv(find_dotenv())

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Lock for thread-safe file writing
file_lock = threading.Lock()

# Model to use for completion requests
model="gpt-4o"

# Function to get completion from OpenAI chat model
def get_completion_from_messages(messages, model, temperature=0, max_tokens=100):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

# Custom OpenAI class definition
class OpenAImethods:
    def __init__(self, language, interaction, context, gt = None, gt_list=None):
        # Initialize instance variables based on input parameters
        self.language = "Italian" if language == "it" else "English"
        self.interaction = interaction
        self.context = context
        self.gt = gt
        self.gt_list = gt_list
        # Log file for recording interactions
        self.log_file = "trial_log.txt"

    # Method to log messages to a file in a thread-safe manner
    def log(self, message):
        with file_lock:
            with open(self.log_file, "a+") as log:
                log.write(message + "\n")

    def binary_request(self):

        # Prompt the model with the interaction
        # add empty lines and delimiter per il co
        # 
        system = (
            "You are provided with an interaction about " f"{self.context}. " 
            "Do you think that " f"{self.gt}? "
            "Answer only with 'yes' or 'no'. "
        )

        user = f"{self.interaction}"
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

        # Time and process the completion request
        start = time.time()
        res = get_completion_from_messages(messages, model)
        end = time.time()

        # Process and log response
        self.response = res.strip('"').lower()
        log_msg = (
            f"request_response_time: {round(end - start, 3)}\n"
            f"request_prompt_characters: {len(system) + len(user)}\n"
            f"request_response: {self.response}"
        )
        self.log(log_msg)

    def three_class_request(self):

        system = (
            "You are provided with an interaction about " f"{self.context}. " 
            "Among these mental states which one better suits the interaction: " f"{self.gt_list}? "
            "Answer only with '"f"{self.gt_list[0]}' or '"f"{self.gt_list[1]}' or 'None'. "
        )

        user = f"{self.interaction}"
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

        # Time and process the completion request
        start = time.time()
        res = get_completion_from_messages(messages, model)
        end = time.time()

        # Process and log response
        self.response = res.strip('"').lower()
        log_msg = (
            f"request_response_time: {round(end - start, 3)}\n"
            f"request_prompt_characters: {len(system) + len(user)}\n"
            f"request_response: {self.response}"
        )
        self.log(log_msg)

