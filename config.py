import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "")
PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro")
FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-2.5-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


def get_model(name: str):
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not set. Add it to your .env file.")
    return genai.GenerativeModel(name)
