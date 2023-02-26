# -*- coding: utf-8-*-
import logging
from client.notifier import Notifier
from client.brain import Brain
import speech_recognition as sr


class Conversation(object):

    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",self.persona)
        while True:
            # Print notifications until empty
            notifications = self.notifier.getAllNotifications()
            for notif in notifications:
                self._logger.info("Received notification: '%s'", str(notif))

            self._logger.debug("Started listening")

            try:
                input = self.mic.listen()
            except sr.WaitTimeoutError:
                self._logger.debug("Nothing has been said")
                continue

            self._logger.debug("Stopped listening, heared:" + input)

            if self.persona in input:
                self._logger.debug("Keyword said, processing input")
                self.brain.query(input)
            else:
                self._logger.debug("No keyword said")
