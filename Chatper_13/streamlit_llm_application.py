import os
import time
import requests
import json
import streamlit as st
from dotenv import load_dotenv
from typing import Iterable


def call_llm(text: str) -> str:
    """Call LLM using direct requests to Google API"""
    body = {
        'contents': [{
            'parts': [{'text': text}]
        }]
    }

    try:
        response = requests.post(
            URL,
            params={'key': API_KEY},
            headers={'Content-Type': 'application/json'},
            data=json.dumps(body),
            timeout=30
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        response_data = response.json()
        response_text = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

        if not response_text:
            return "No response generated. Please try again."

        return response_text

    except requests.exceptions.RequestException as e:
        return f"Error calling API: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing response: {str(e)}"


def yield_text(text: str) -> Iterable[str]:
    """Yield text word by word for streaming effect"""
    for word in text.split(' '):
        yield word + ' '
        time.sleep(0.02)  # Slightly slower for better readability


def main():
    load_dotenv()

    st.title('LLM Chat with Streamlit')

    # Main interface
    st.write("Enter your prompt below and click Send to get a response from Gemini.")

    text = st.text_area(
        'Your prompt:',
        height=120,
        placeholder="Ask me anything..."
    )

    sent = st.button('Send', type="primary")

    # Handle submission
    if sent:

        response_text = call_llm(text)
        st.write_stream(yield_text(response_text))

if __name__ == '__main__':
    API_KEY = os.getenv('API_KEY')
    URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

    main()
