# uvicorn main:app
# uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# Custom function imports
from functions.openai_request import convert_audio_to_text, get_chat_response
from functions.database import reset_messages, store_messages
from functions.text_to_speech import convert_text_to_speech


# Initiate App
app = FastAPI()

# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check health
@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

# Reset database file
@app.get("/reset")
async def reset_conversation():
    # Reset the database file
    reset_messages()
    return {"message": "Reset successful"}

# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    print("===== POST AUDIO =====")
    # Convert audio to text - production
    # Save the file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_input, "en")

    #Guard: Ensure message decoded
    if not message_decoded:
        raise HTTPException(status_code=404, detail="Failed to decode audio")
        
    # Get ChatGPT response
    chat_response = get_chat_response(message_decoded)

    # Store messages
    store_messages(message_decoded, chat_response)

    #Guard: Ensure message decoded
    if not chat_response:
        raise HTTPException(status_code=404, detail="Failed to get chat response")

    # Convert text to speech
    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        raise HTTPException(status_code=404, detail="Failed to get Eleven Labs audio response")

    # Create a generator that yields chunks of the audio file
    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
