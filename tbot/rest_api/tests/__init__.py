import json
import binascii
from contextlib import contextmanager

from django.dispatch import Signal
from django.test import override_settings

from django.core.exceptions import ObjectDoesNotExist

from mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from django.conf import settings
from json import dumps
import os
from random import choice
import string
import time

@contextmanager
def suspended_signal( signal, receiver, sender=None, weak=True, dispatch_uid=None ):
    result = Signal.disconnect( signal, receiver, sender=sender, dispatch_uid=dispatch_uid )
    assert result, 'Signal was not disconnected; details: {}'.format(
        (signal, receiver, sender, dispatch_uid))
    try:
        yield result
    finally:
        Signal.connect( signal, receiver, sender=sender, weak=weak, dispatch_uid=dispatch_uid )

class BasicTest( APITestCase ):
    """
    Generic Minnow stuff.
    """

    # Display standard message and passed message when displaying assertion failures, used to include API response
    longMessage = True

    PW = 'password123'

    def login(self, username, password=None):
        if password is None:
            password = self.PW
        self.client.login(username=username, password=password)

        if password is not None and password != self.PW:
            # The password unit test passes an invalid password, which will cause 2FA to fail, so we need to bail first.
            return

    def logout(self):
        self.client.logout()
 
    def tearDown(self):
        pass

    def _check_test_failed(self):
        result = self._resultForDoCleanups
        try:
            return not result.wasSuccessful()
        except AttributeError:
            # The Django parallel test runner uses a different class which doesn't implement that function
            for event in reversed(result.events):
                # Loop over the events to see if there is an error or failure event for the current test
                if event[1] == result.test_index:
                    if event[0] in ('addError', 'addFailure'):
                        return True
                else:
                    break
