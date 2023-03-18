import os
from fastapi import FastAPI, Request, Response
from google.cloud import texttospeech_v1
from pydantic import BaseModel
import re
from typing import Optional
from fastapi.responses import FileResponse

app = FastAPI()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "polyglot-379405-49f702545383.json"

class RequestModel(BaseModel):
    text: str

class ResponseModel(BaseModel):
    sound: str

@app.post("/synthesize")
async def synthesize_text(request: RequestModel, format: Optional[str] = "mp3") -> dict:
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

    if format == "mp3":
        file_extension = ".mp3"
        media_type = "audio/mp3"
    elif format == "wav":
        file_extension = ".wav"
        media_type = "audio/wav"
    else:
        raise ValueError("Unsupported audio format")

    with open("output" + file_extension, "wb") as out:
        out.write(response.audio_content)

    return {
        "url": f"/audio/output{file_extension}"
    }

@app.get("/audio/{filename}")
async def get_audio(filename: str) -> FileResponse:
    return FileResponse(filename)
