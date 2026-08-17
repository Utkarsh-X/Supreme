#!/usr/bin/env python3
import os
from google import genai

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-3.7-flash',
    contents="Which exact model are you? State your official model name and version directly."
)

print(response.text)
