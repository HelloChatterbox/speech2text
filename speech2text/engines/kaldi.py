from speech2text.engines import STT
import re
from os.path import isdir
import json
import requests
from speech2text.log import LOG


class KaldiServerSTT(STT):
    def execute(self, audio, language=None):
        response = requests.post(self.config.get("uri"),
                                 data=audio.get_wav_data())
        try:
            hypotheses = response.json()["hypotheses"]
            return re.sub(r'\s*\[noise\]\s*', '', hypotheses[0]["utterance"])
        except Exception:
            return None


class KaldiSTT(STT):
    def __init__(self, config):
        super().__init__(config)
        global Model, KaldiRecognizer
        from vosk import Model, KaldiRecognizer
        model_path = self.config.get("model")
        if not model_path or not isdir(model_path):
            LOG.error("You need to provide a valid model file")
            LOG.info("download a model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md")
            raise FileNotFoundError
        self.model = Model(model_path)

    def execute(self, audio, language=None):
        kaldi = KaldiRecognizer(self.model, 16000)
        kaldi.AcceptWaveform(audio.get_wav_data())
        res = kaldi.FinalResult()
        res = json.loads(res)
        return res["text"]
