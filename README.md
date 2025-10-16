# AI Quiz Generator

An AI-powered web application that generates multiple-choice quizzes from YouTube video transcripts using Google's Gemini API. Built with Flask, this tool allows users to input a YouTube URL, extract the video's transcript, and automatically create a quiz with questions and options.

## Features

- **YouTube Transcript Extraction**: Automatically fetches transcripts from YouTube videos (supports English and Hindi languages).
- **AI-Generated Quizzes**: Uses Google's Gemini 2.5 Flash API to generate relevant multiple-choice questions based on the video content.
- **Interactive Web Interface**: Simple web UI for quiz generation and submission.
- **Scoring System**: Provides instant feedback on quiz performance with detailed results.
- **Session Management**: Securely stores quiz data in user sessions to prevent cheating.

## Prerequisites

- Python 3.7 or higher
- A Google Gemini API key (obtain from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-quiz-generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Create a `.env` file in the root directory of the project:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

2. Replace `your_gemini_api_key_here` with your actual Gemini API key.

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Enter a YouTube URL in the provided field and click "Generate Quiz".

4. Answer the questions and submit the quiz to see your score and detailed results.

## Project Structure

```
ai-quiz-generator/
├── app.py                 # Main Flask application
├── quiz_logic.py          # Core logic for transcript extraction and quiz generation
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Frontend HTML template
├── .env                   # Environment variables (API key)
└── README.md              # Project documentation
```

## Technologies Used

- **Flask**: Web framework for Python
- **Google Gemini API**: AI model for quiz generation
- **YouTube Transcript API**: For extracting video transcripts
- **Requests**: HTTP library for API calls
- **Python-dotenv**: Environment variable management

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This application uses Google's Gemini API. Ensure you comply with Google's terms of service and API usage policies. The generated quizzes are for educational purposes only.
