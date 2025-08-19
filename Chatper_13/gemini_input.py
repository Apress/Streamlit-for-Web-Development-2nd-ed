import os
import requests
import json

API_KEY = os.getenv('API_KEY')
URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'


def call_llm(text: str) -> str:

    body = {
        'contents': [{
            'parts': [{'text': text}]
        }]
    }

    response = requests.post(
        URL, params={'key': API_KEY}, headers={'Content-Type': 'application/json'},
        data=json.dumps(body)
    )

    return response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')