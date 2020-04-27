from speech2text.log import LOG
from speech2text.engines import STT
from requests.exceptions import HTTPError
import requests
import json
from os.path import join, expanduser, isfile

# TODO remove this, this should not be supported in a package, nothing
#  should use it except mycroft-core
# mycroft-core should subclass STT factory instead


class NotMycroft(Exception):
    """ identity2.json not found"""


def requires_pairing(func):
    """Decorator kicking of pairing sequence if client is not allowed access.

    Checks the http status of the response if an HTTP error is recieved. If
    a 401 status is detected returns "pair my device" to trigger the pairing
    skill.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 401:
                LOG.warning('Access Denied at mycroft.ai')
                # phrase to start the pairing process
                return 'pair my device'
            else:
                raise

    return wrapper


class MycroftSTT(STT):
    """Default mycroft STT."""

    def __init__(self, config):
        self.base_url = "https://api.mycroft.ai"
        self.version = "v1"
        self.url = join(self.base_url, self.version, "stt")
        super().__init__(config)

    @property
    def identity(self):
        path = expanduser("~/.mycroft/identity2.json")
        if isfile(path):
            with open(path) as f:
                return json.load(f)
        raise NotMycroft

    def refresh_token(self):
        LOG.debug('Refreshing token')
        try:
            data = requests.post(
                join(self.base_url, self.version, "auth/token"),
                headers={
                    "Authorization": "Bearer " + self.identity.refresh,
                    "Device": self.identity.uuid
                }).json()
            # dont save, let mycroft devices refresh again and save it
            # do not mess with mycroft devices, extra refresh only to allow
            # usage
            return data
        except HTTPError as e:
            if e.response.status_code == 401:
                LOG.error('Could not refresh token, invalid refresh code.')
            else:
                raise

    def stt_api(self, audio, language, limit):
        """ Web API wrapper for performing Speech to Text (STT)

        Args:
            audio (bytes): The recorded audio, as in a FLAC file
            language (str): A BCP-47 language code, e.g. "en-US"
            limit (int): Maximum minutes to transcribe(?)

        Returns:
            str: JSON structure with transcription results
        """
        headers = {"Content-Type": "audio/x-flac",
                   "Authorization": "Bearer " + self.identity["access"]
                   }
        try:
            return requests.post(self.url,
                                 params={"lang": language, "limit": limit},
                                 headers=headers,
                                 data=audio)
        except:
            identity = self.refresh_token()
            headers = {"Content-Type": "audio/x-flac",
                       "Authorization": "Bearer " + identity["access"]
                       }
            return requests.post(self.url,
                                 params={"lang": language, "limit": limit},
                                 headers=headers,
                                 data=audio)

    @requires_pairing
    def execute(self, audio, language=None):
        self.lang = language or self.lang
        try:
            return self.stt_api(audio.get_flac_data(convert_rate=16000),
                                self.lang, 1)[0]
        except Exception:
            return self.stt_api(audio.get_flac_data(), self.lang, 1)[0]


class MycroftDeepSpeechSTT(MycroftSTT):
    """Mycroft Hosted DeepSpeech"""

    def __init__(self, config):
        super().__init__(config)
        self.url = join(self.base_url, self.version, "deepspeech")

    @requires_pairing
    def execute(self, audio, language=None):
        language = language or self.lang
        if not language.startswith("en"):
            raise ValueError("Deepspeech is currently english only")
        return self.stt_api(audio.get_wav_data(), self.lang, 1)
