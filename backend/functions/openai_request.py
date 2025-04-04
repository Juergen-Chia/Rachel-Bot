import openai
from decouple import config

from functions.database import get_recent_messages

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file, language):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language=language)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return {"message": "Error"}
    
# Open AI - ChatGPT
# Get bot response
def get_chat_response(message_input):

    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        print(response)
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        print(f"Error in openai_request.py try statement: {e}")
        return "--- Error in openai_request.py try statement ---"