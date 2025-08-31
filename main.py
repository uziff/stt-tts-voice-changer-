from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import threading
from pygame import mixer
import os
import time
import random
import string
from google import genai
from google.genai import types
import wave
import io

mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")

engine = pyttsx3.init()
engine.setProperty('rate', 250)
client = genai.Client(api_key='') # add ur api key here

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def speak(text):
    file_name = "" 
    
    if not text.strip():
        print("Nessun testo da riprodurre.")
        return

    try:
        response = client.models.generate_content(
           model="gemini-2.5-flash-preview-tts",
           contents='Read aloud in a warm, natural, friendly but also really intrigued tone. you are speaking in an online voice chat called discord: ' + text, # to make the voice sound slightly natural
           config=types.GenerateContentConfig(
              response_modalities=["AUDIO"],
              speech_config=types.SpeechConfig(
                 voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                       voice_name='Leda',
                    )
                 )
              ),
           )
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        file_name = f"{generate_random_string()}.wav"

        
        with wave.open(file_name, 'wb') as wf:
            wf.setnchannels(1)  
            wf.setsampwidth(2)
            wf.setframerate(24000)  
            wf.writeframes(audio_data)
        
        mixer.music.load(file_name)
        mixer.music.play()

        while mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"Si è verificato un errore: {e}")

    finally:
        mixer.music.unload()
        if file_name and os.path.exists(file_name):
            os.remove(file_name)



if __name__ == '__main__':
    print("Wait until it says 'speak now'")

    recorder = AudioToTextRecorder()

    while True:
        text = recorder.text()
        print(text)
        t = threading.Thread(target=speak, args=(text,))
        t.start()
