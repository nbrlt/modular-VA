#!/usr/bin/env python2
# -*- coding: utf-8-*-
import os
from abc import ABCMeta, abstractmethod
import yaml
from client import jasperpath
from client import diagnose
import speech_recognition as sr

class AbstractSpeechRecogniser:
    """"
    Generic parent class for all SpeechRecogniser engines
    """
    __metaclass__ = ABCMeta

    def __init__(self, profile):
        self.profile = profile
        self.recogniser = sr.Recognizer()


    @abstractmethod
    def get_config(self):
        pass

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def get_passive_instance(cls):
        return cls.get_instance()

    @classmethod
    def get_active_instance(cls):
        return cls.get_instance()

    @classmethod
    @abstractmethod
    def is_available(cls):
        return True

    @abstractmethod
    def transcribe(self, audio):
        pass


class Whisper(AbstractSpeechRecogniser):

    SLUG = "whisper"
    def __init__(self, profile):
        super().__init__(profile)
        self.kw_config = self.get_config()


    def get_config(self):
        # Needed config

        # Optional config
        kw_config = {}
        if 'whisper' in self.profile:
            try: kw_config['model'] = self.profile['whisper']['model']
            except: pass
            try: kw_config['language'] = self.profile['whisper']['language']
            except: pass
            try: kw_config['translate'] = self.profile['whisper']['translate']
            except: pass
        return kw_config

    @classmethod
    def is_available(cls):
        ffmpeg = diagnose.check_executable("ffmpeg")
        whisper = diagnose.check_python_import("whisper")
        soundfile = diagnose.check_python_import("soundfile")
        return  ffmpeg and whisper and soundfile

    def transcribe(self, audio):
        return self.recogniser.recognize_whisper(audio, **self.kw_config).upper()
        pass

def get_engine_by_slug(slug=None):
    """
    Returns:
        An STT Engine implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                              engine.SLUG == slug, get_engines()))
    if len(selected_engines) == 0:
        raise ValueError("No STT engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print(("WARNING: Multiple STT engines found for slug '%s'. " +
                   "This is most certainly a bug.") % slug)
        engine = selected_engines[0]
        if not engine.is_available():
            raise ValueError(("STT engine '%s' is not available (due to " +
                              "missing dependencies, missing " +
                              "dependencies, etc.)") % slug)
        return engine


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractSpeechRecogniser))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]
