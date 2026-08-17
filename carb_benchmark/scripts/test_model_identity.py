#!/usr/bin/env python3
"""
test_model_identity.py — Test script to query Gemini model identity via live API call.
"""

import os
import sys
from google import genai
from google.genai import types

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: No API Key found.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

print("=== Sending Live Verification Request to 'gemini-3.7-flash' ===")

try:
    response = client.models.generate_content(
        model='gemini-3.7-flash',
        contents="Identify yourself. What model name, version, and architecture are you running under?",
        config=types.GenerateContentConfig(
            temperature=0.0
        )
    )
    print("\n--- MODEL RESPONSE OUTPUT ---")
    print(response.text)
    print("----------------------------")
    if hasattr(response, 'usage_metadata'):
        print(f"Total Tokens Used: {response.usage_metadata.total_token_count}")
except Exception as e:
    print(f"API Error: {e}")
