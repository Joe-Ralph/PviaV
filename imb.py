import json
import logging
import os
from queue import Queue
from threading import Thread
import time

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Watson websocket prints justs too many debug logs, so disable it
logging.disable(logging.CRITICAL)

# Chunk and buffer size
CHUNK_SIZE = 4096
BUFFER_MAX_ELEMENT = 10

# A callback class to process various streaming STT events
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.transcript = None

    def on_transcription(self, transcript):
        # print('transcript: {}'.format(transcript))
        pass

    def on_connected(self):
        # print('Connection was successful')
        pass

    def on_error(self, error):
        # print('Error received: {}'.format(error))
        pass

    def on_inactivity_timeout(self, error):
        # print('Inactivity timeout: {}'.format(error))
        pass

    def on_listening(self):
        # print('Service is listening')
        pass

    def on_hypothesis(self, hypothesis):
        # print('hypothesis: {}'.format(hypothesis))
        pass

    def on_data(self, data):
        self.transcript = data['results'][0]['alternatives'][0]['transcript']
        print('{0}final: {1}'.format(
            '' if data['results'][0]['final'] else 'not ',
            self.transcript
        ))

    def on_close(self):
        # print("Connection closed")
        pass

def watson_streaming_stt(filename: str, lang: str, encoding: str) -> str:
    authenticator = IAMAuthenticator(WATSON_API_KEY)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(WATSON_STT_URL)

    # Make watson audio source fed by a buffer queue
    buffer_queue = Queue(maxsize=BUFFER_MAX_ELEMENT)
    audio_source = AudioSource(buffer_queue, True, True)

    # Callback object
    mycallback = MyRecognizeCallback()

    # Read the file
    buffer, rate = read_wav_file(filename)

    # Start Speech-to-Text recognition thread
    stt_stream_thread = Thread(
        target=speech_to_text.recognize_using_websocket,
        kwargs={
            'audio': audio_source,
            'content_type': 'audio/l16; rate={}'.format(rate),
            'recognize_callback': mycallback,
            'interim_results': True
        }
    )
    stt_stream_thread.start()

    # Simulation audio stream by breaking file into chunks and filling buffer queue
    audio_generator = simulate_stream(buffer, CHUNK_SIZE)
    for chunk in audio_generator:
        buffer_queue.put(chunk)
        time.sleep(0.5)  # give a chance to callback

    # Close the audio feed and wait for STTT thread to complete
    audio_source.completed_recording()
    stt_stream_thread.join()

    # send final result
    return mycallback.transcript

# Run tests
for t in TESTCASES:
    print('\naudio file="{0}"    expected text="{1}"'.format(
        t['filename'], t['text']
    ))
    print('watson-cloud-streaming-stt: "{}"'.format(
        watson_streaming_stt(t['filename'], t['lang'], t['encoding'])
    ))