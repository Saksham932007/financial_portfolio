"""
Direct API test with timeout
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import signal

load_dotenv()

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Configure safety settings to allow financial content
safety_settings = {
    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
    'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
    'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
}

model = genai.GenerativeModel("gemini-2.5-flash", safety_settings=safety_settings)

print("Testing with 10 second timeout...")
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)

try:
    print("Sending request...")
    response = model.generate_content(
        "Analyze AAPL stock technical indicators. Current price: $247. Provide analysis in JSON format with RSI, MACD, and trend direction.",
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=500,
        )
    )
    signal.alarm(0)  # Cancel alarm
    print(f"✅ Response received:\n{response.text}")
except TimeoutError:
    print("❌ Request timed out after 10 seconds")
except Exception as e:
    signal.alarm(0)
    print(f"❌ Error: {e}")
