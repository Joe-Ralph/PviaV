import speech_recognition as sr
from grammarChannel import GrammerChannel
# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`

    print(r.recognize_google(audio).lower())
except sr.UnknownValueError:
    print("""
    █▀█ █▀▀ ▀█▀ █▀█ █▄█
    █▀▄ ██▄ ░█░ █▀▄ ░█░                                                                  
""")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))