import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVD_API_KEY")
debug_mode = os.getenv("DEBUG", "False")
print(api_key)

