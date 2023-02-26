# -*- coding: utf-8-*-
"""
    The Mic class handles all the audio interactions: listening and speaking.
"""
import logging
from client import alteration
import speech_recognition as sr
from client.app_utils import get_profile



class Mic:

    speechRec = None
    speechRec_persona = None

    def __init__(self, tts_engine,  stt_engine):
        """

        """
        self.kw_config = self.get_config()
        self.microphone = sr.Microphone(**self.kw_config)

        self._logger = logging.getLogger(__name__)
        self.tts_engine = tts_engine
        self.engine = stt_engine

    def get_config(self):
        kw_config = {}
        profile = get_profile()
        try:
            kw_config = profile['microphone']
        except:
            pass
        return kw_config

    def adjustThreshold(self):
        with self.microphone as source:
            self.engine.recogniser.adjust_for_ambient_noise(source)

    def listen(self):
        with self.microphone as source:
            # listen for 1 second to calibrate the energy threshold for ambient noise levels
            self.engine.recogniser.adjust_for_ambient_noise(source)
            audio = self.engine.recogniser.listen(source)
            transcribed = self.engine.transcribe(audio)
        return transcribed

    def say(self, phrase,
            OPTIONS=" -vdefault+m3 -p 40 -s 160 --stdout > say.wav"):
        # alter phrase before speaking
        phrase = alteration.clean(phrase)
        self.tts_engine.say(phrase)
