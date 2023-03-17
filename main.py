import os
from google.cloud import texttospeech
from google.cloud import texttospeech_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/CVMU HACKATHON/polyglot-379405-49f702545383.json"
print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

# Instantiates a client
client = texttospeech_v1.TextToSpeechClient()

# text to convert
text = "Hello, aap mere acche dost ho, lekin fir bhi aap maha chutiye hein."

synthesis_input = texttospeech_v1.SynthesisInput(text=text)

# voice selection
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="en-in",
    ssml_gender=texttospeech_v1.SsmlVoiceGender.MALE
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

with open('audio file.mp3', 'wb') as output:
    output.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
