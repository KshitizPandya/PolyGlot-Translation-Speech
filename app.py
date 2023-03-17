import os
from fastapi import FastAPI, Request, Response
from google.cloud import texttospeech_v1
from pydantic import BaseModel
import re

app = FastAPI()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/CVMU HACKATHON/polyglot-379405-49f702545383.json"

class RequestModel(BaseModel):
    text: str

class ResponseModel(BaseModel):
    sound: str

@app.post("/synthesize")
async def synthesize_text(request: RequestModel) -> RequestModel:
    text_to_synthesize = request.text
    text_to_synthesize = re.sub('[^A-Za-z0-9 \/\\\\]+', '', text_to_synthesize)

    print(text_to_synthesize)
    # Instantiates a client
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text_to_synthesize)

    # voice selection
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code="en-in",
        ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
    )

    # output file configuration
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    mp3_file = response.audio_content

    headers = {
        "Content-Disposition": 'attachment; filename="output.mp3"'
    }
    return Response(content=mp3_file, headers=headers, media_type="audio/mp3")
