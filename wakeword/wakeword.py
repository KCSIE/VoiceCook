import pyaudio
import azure.cognitiveservices.speech as speechsdk
import struct
import time

AZURE_API_KEY = ""
AZURE_REGION = ""
model_path = "wakeword\Hey-Gordon-Advanced.table"

class AzureWakeWord:
    def __init__(self, AZURE_API_KEY, AZURE_REGION, model_path):
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
        self.model_path = model_path
    
    def detect_wakeword_once(self):
        model = speechsdk.KeywordRecognitionModel(self.model_path)
        keyword_recognizer = speechsdk.KeywordRecognizer()

        print("Start Wakeword Detection.")
        keyword_recognition_result = keyword_recognizer.recognize_once_async(model).get()

        if keyword_recognition_result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print("Recognized:{}".format(keyword_recognition_result.text))
            return keyword_recognition_result.text
        elif keyword_recognition_result.reason == speechsdk.ResultReason.Canceled:
            print("Canceled:{}".format(keyword_recognition_result.cancellation_details))
        elif keyword_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No Match :{}".format(keyword_recognition_result.no_match_details))
        
        return None

    def detect_wakeword_with_speech(self):
        model = speechsdk.KeywordRecognitionModel(self.model_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
        done = False

        def stop_cb(evt):
            # print('Closing on {}'.format(evt))
            nonlocal done
            done = True

        def recognized_cb(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
                print('Recognized Wakeword: {}'.format(evt.result.text))
            elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print('Recognized: {}'.format(evt.result.text))
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print('No Match: {}'.format(evt))

        speech_recognizer.recognized.connect(recognized_cb)
        # speech_recognizer.canceled.connect(lambda evt: print('Canceled {}'.format(evt)))
        
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)
        
        speech_recognizer.start_keyword_recognition(model)
        print("Start Wakeword Detection.")
        while not done:
            time.sleep(.5)
        speech_recognizer.stop_keyword_recognition()

if __name__ == '__main__':    
    test = AzureWakeWord(AZURE_API_KEY, AZURE_REGION, model_path)
    while True:
        # keyword = test.detect_wakeword_once()
        # if keyword != None:
        #     print("Hi, I'm listening.")
        test.detect_wakeword_with_speech()
        print("Hi, I'm listening.")