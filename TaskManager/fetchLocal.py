import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the secret key from the .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
