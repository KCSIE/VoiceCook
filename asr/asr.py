import azure.cognitiveservices.speech as speechsdk
import threading
import time

AZURE_API_KEY = ""
AZURE_REGION = ""

class AzureASR:
    def __init__(self, AZURE_API_KEY, AZURE_REGION):
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)

    def speech_to_text_once(self):
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "20000")
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        print("Start ASR.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized:{}".format(speech_recognition_result.text))
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            print("Canceled:{}".format(speech_recognition_result.cancellation_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No Match :{}".format(speech_recognition_result.no_match_details))
        
        return None

    def speech_to_text_continuous(self):
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        all_records = []
        recognition_done = threading.Event()

        def record_result(evt):
            all_records.append(evt.result.text)
        
        def recognized_cb(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print('Recognized: {}'.format(evt.result.text))
                if not evt.result.text: # when silence stop recognition
                    print('Stop Listening - Silence Timeout')
                    recognition_done.set()
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print('No Match: {}'.format(evt))
                recognition_done.set()

        def stop_cb(evt):
            if evt.result.reason == speechsdk.ResultReason.Canceled:
                print('Canceled: {}'.format(evt))
                recognition_done.set()
            else:
                print('Closing on {}'.format(evt))
                recognition_done.set()

        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.recognized.connect(record_result)
        
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        print("Start ASR.")
        speech_recognizer.start_continuous_recognition()
        recognition_done.wait()
        speech_recognizer.stop_continuous_recognition()

        return ';'.join(all_records[:-1])

if __name__ == '__main__':
    test = AzureASR(AZURE_API_KEY, AZURE_REGION)
    test.speech_to_text_once()
    # test.speech_to_text_continuous()