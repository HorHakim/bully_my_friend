from dotenv import load_env

load_env()

import base64
import requests
import os
from mistralai import Mistral

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None



def load_context():
	with open("context.txt", "r") as file:
		return file.read()

def load_prompt():
	with open("prompt.txt", "r") as file:
		return file.read()


def get_joke(image_path):
	# Getting the base64 string
	base64_image = encode_image(image_path)

	# Retrieve the API key from environment variables
	api_key = os.environ["MISTRAL_API_KEY"]

	# Specify model
	model = "pixtral-12b-2409"

	# Initialize the Mistral client
	client = Mistral(api_key=api_key)

	# Define the messages for the chat
	messages = [
		{
			"role": "system",
			"content":  load_context()

		}
	    {
	        "role": "user",
	        "content": [
	            {
	                "type": "text",
	                "text": load_prompt()
	            },
	            {
	                "type": "image_url",
	                "image_url": f"data:image/jpeg;base64,{base64_image}" 
	            }
	        ]
	    }
	]

	# Get the chat response
	chat_response = client.chat.complete(
	    model=model,
	    messages=messages
	)

	# Print the content of the response
	return chat_response.choices[0].message.content

