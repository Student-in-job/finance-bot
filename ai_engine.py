import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_spending(text, category_context):
    prompt = f"""
    Act as a financial parser. Analyze this Russian spending note: \"{text}\"
    
    Available Categories and their tags:
    {category_context}
    
    Rules:
    1. Select the BEST category from the list based on text and tags.
    2. Convert amount to a ROUNDED INTEGER.
    3. Return ONLY JSON: {{"amount": int, "category": "name", "currency": "RUB", "original_text": "text"}}
    """
    response = model.generate_content(prompt)
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)
