import pyttsx3
import azure.cognitiveservices.speech as speechsdk
import time

AZURE_API_KEY = ""
AZURE_REGION = ""

class Pyttsx3TTS:
    def __init__(self):
        pass

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

class AzureTTS:
    def __init__(self, AZURE_API_KEY, AZURE_REGION):
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        self.speech_config.speech_synthesis_voice_name = "en-US-BrianMultilingualNeural"

    def text_to_speech(self, text):
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)

        print("Start TTS.")
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            print("Speech synthesis canceled: {}".format(speech_synthesis_result.cancellation_details.reason))

if __name__ == '__main__':
    # test = Pyttsx3TTS()
    # test.text_to_speech("I will speak this text")
    test = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    test.text_to_speech("I will speak this text")