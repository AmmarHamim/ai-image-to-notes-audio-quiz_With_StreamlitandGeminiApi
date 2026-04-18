from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io


#loading the environment variables
load_dotenv()

my_api_key=os.getenv("GEMINI_API_KEY")

client=genai.Client(api_key=my_api_key)


#note generator
def note_generator(images):

    prompt="""summarize the pictures in note format in bangla at max 100 words and 
    make sure to add necessary markdown to distinguish different section"""
    response=client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images,prompt]
    )

    return response.text

def audio_transcription(text):
    speech=gTTS(text,lang='bn',slow=False)

    audio_buffer=io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer


def quiz_generator(images,difficulty):
    prompt=f"generate 5 quizes with correct answers in bangla based on {difficulty}"

    response=client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images,prompt]
    )
    return response.text