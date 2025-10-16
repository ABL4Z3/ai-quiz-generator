import os
import json
import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# --- GEMINI API SETUP ---
API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# Define the expected JSON structure for the quiz
QUIZ_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "question": {"type": "STRING"},
            "options": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            },
            "correct_answer": {"type": "STRING"}
        },
        "required": ["question", "options", "correct_answer"]
    }
}

def get_transcript(url: str) -> str:
    """Extracts the transcript from a YouTube URL."""
    try:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if not match:
            raise ValueError("Invalid YouTube URL or video ID not found.")
        
        video_id = match.group(1)
        
        ytt_api = YouTubeTranscriptApi()

        fetched_transcript = ytt_api.fetch(
            video_id, 
            languages=['hi', 'en'], 
            preserve_formatting=True
        )

        full_transcript = " ".join([snippet.text for snippet in fetched_transcript])
        
        return full_transcript

    except NoTranscriptFound:
        raise ValueError(f"No transcript found for video ID '{video_id}' in English or Hindi.")
    except TranscriptsDisabled:
        raise ValueError(f"Transcripts are disabled for the video with ID '{video_id}'.")
    except Exception as e:
        raise ConnectionError(f"Failed to retrieve transcript: {e}")

def generate_quiz_from_text(text, num_questions=5):
    """
    Calls the Gemini API to generate quiz questions from the provided text.
    """
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    prompt = f"""
    Based on the following text, generate a multiple-choice quiz with {num_questions} questions.
    Each question must have exactly 4 options.
    One of the options must be the correct answer.
    The `correct_answer` field must exactly match one of the strings in the `options` array.

    NOTE:- Language must me english of the questions and answers.

    Text:
    ---
    {text}
    ---
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": QUIZ_SCHEMA
        }
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        response_json = response.json()
        quiz_json_string = response_json['candidates'][0]['content']['parts'][0]['text']
        return json.loads(quiz_json_string)

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        error_info = response.json().get('error', {})
        error_message = error_info.get('message', 'An unknown error occurred with the API call.')
        raise ConnectionError(f"Failed to connect to Gemini API. Details: {error_message}") from e
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Failed to parse API response: {e}")
        print(f"Raw response: {response.text}")
        raise ValueError("The API returned an unexpected or malformed response.") from e