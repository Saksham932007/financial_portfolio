"""
Simple Gemini API test
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Testing Gemini API...")
print("=" * 80)

# Try with gemini-2.5-flash
model = genai.GenerativeModel("gemini-2.5-flash")

print("\nSending a simple request...")
try:
    response = model.generate_content("What is 2+2? Answer in one sentence.")
    print(f"✅ Success! Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("Testing with tools parameter...")
try:
    model_with_tools = genai.GenerativeModel(
        "gemini-2.5-flash",
        tools='google_search_retrieval'
    )
    response = model_with_tools.generate_content("What is the capital of France?")
    print(f"✅ Success with tools! Response: {response.text}")
except Exception as e:
    print(f"❌ Error with tools: {e}")
