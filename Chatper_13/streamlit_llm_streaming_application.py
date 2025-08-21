import os
import time
import requests
import json
import streamlit as st
from dotenv import load_dotenv
from typing import Iterable
from google import genai


def call_llm_requests(text: str) -> str:
    """Call LLM using direct requests to Google API"""
    body = {
        'contents': [{
            'parts': [{'text': text}]
        }]
    }

    response = requests.post(
        URL, params={'key': API_KEY}, headers={'Content-Type': 'application/json'},
        data=json.dumps(body)
    )
    response_text = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')

    return response_text


def call_llm_genai(text: str) -> str:
    """Call LLM using google-ai-generativelanguage library"""
    try:
        # Create client
        client = genai.Client(api_key=API_KEY)

        # Generate content
        response = client.models.generate_content(
            model='gemini-1.5-flash-latest',
            contents={'parts': [{'text': text}]}
        )

        return response.candidates[0].content.parts[0].text
    except Exception as e:
        return f"Error calling LLM with google-ai-generativelanguage: {str(e)}"


def call_llm_genai_stream(text: str) -> Iterable[str]:
    """Call LLM using google-ai-generativelanguage library with streaming"""

    try:
        # Create client
        client = genai.Client(api_key=API_KEY)

        # Generate content with streaming
        response = client.models.generate_content_stream(
            model='gemini-1.5-flash-latest',
            contents={'parts': [{'text': text}]}
        )

        for chunk in response:
            if chunk.candidates and chunk.candidates[0].content.parts:
                text_chunk = chunk.candidates[0].content.parts[0].text
                if text_chunk:
                    yield text_chunk
                    time.sleep(0.01)  # Small delay for visual effect
    except Exception as e:
        yield f"Error calling LLM with streaming: {str(e)}"


def yield_text(text: str) -> Iterable[str]:
    """Yield text word by word for streaming effect"""
    for word in text.split(' '):
        yield word + ' '
        time.sleep(0.01)


def main():
    load_dotenv()

    st.title('LLMs in Streamlit')

    # API method selection
    st.sidebar.title("Configuration")

    api_options = ["Direct Requests", "Google AI GenerativeLanguage Library"]

    api_method = st.sidebar.selectbox(
        "Choose API Method:",
        api_options,
        help="Select how to call the Google Gemini API"
    )

    # Streaming option for google-ai-generativelanguage
    use_streaming = False
    if api_method == "Google AI GenerativeLanguage Library":
        use_streaming = st.sidebar.checkbox(
            "Use Streaming",
            value=True,
            help="Stream the response in real-time (only available with google-ai-generativelanguage library)"
        )

    # Main interface
    text = st.text_area('Write prompt here', height=100)
    sent = st.button('Send', type="primary")

    if not sent or not text.strip():
        return

    if not API_KEY:
        st.error("API_KEY not found. Please set it in your .env file.")
        return

    # Show which method is being used
    if api_method == "Direct Requests":
        st.info("🔗 Using direct HTTP requests to Google API")
        with st.spinner("Generating response..."):
            response_text = call_llm_requests(text)
        st.write_stream(yield_text(response_text))

    elif api_method == "Google AI GenerativeLanguage Library":
        st.info("🌊 Using google-ai-generativelanguage library with streaming")
        st.write_stream(call_llm_genai_stream(text))
    else:
        st.error("Selected API method is not available. Please install the required library or choose a different method.")


if __name__ == '__main__':
    API_KEY = os.getenv('API_KEY')
    URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

    main()
