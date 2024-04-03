import time
from datetime import datetime
import threading
import pyttsx3

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type

# Timer is from https://github.com/Avo-k/cyrano/blob/main/src/tools/_timer.py
class Timer:
    def __init__(self, duration):
        self.duration = int(duration)
        self.start_time = None
        self.remaining = int(duration)
        self.thread = None
        self.paused = False
        self.stopped = False

    def start(self):
        self.start_time = time.time()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.stopped and self.remaining > 0:
            if not self.paused:
                time.sleep(1)
                self.remaining = self.duration - (time.time() - self.start_time)
        if self.stopped:
            print("Timer stopped.")
        else:
            print("Timer finished.")
            engine = pyttsx3.init()
            engine.say("Times up! Times up! Times up!")
            engine.runAndWait()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.start_time = time.time() - (self.duration - self.remaining)

    def stop(self):
        self.stopped = True
        if self.thread is not None:
            self.thread.join()

class SecondsInput(BaseModel):
    """Inputs for set_timer"""
    seconds: int = Field(description="duration of the timer in seconds")

class SetTimer(BaseTool):
    name = "set_timer"
    description = "useful when you need to set a timer or alarm"
    args_schema: Type[BaseModel] = SecondsInput

    def _run(self, seconds: int) -> str:
        timer = Timer(duration=seconds)
        timer.start()
        return "Successfully set timer."

class GetTime(BaseTool):
    name = "get_time"
    description = "useful when you want to know current time"

    def _run(self, no_use: str) -> str:
        return datetime.now().strftime('%H:%M')

if __name__ == '__main__':
    test = Timer(duration=5)
    test.start()
    # test = GetTime()
    # print(test._run())
