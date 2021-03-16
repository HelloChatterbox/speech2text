from speech2text.engines import STT
import re
import requests


class KaldiServerSTT(STT):
    """ https://github.com/alumae/kaldi-gstreamer-server """
    def execute(self, audio, language=None):
        response = requests.post(self.config.get("uri"),
                                 data=audio.get_wav_data())
        try:
            hypotheses = response.json()["hypotheses"]
            return re.sub(r'\s*\[noise\]\s*', '', hypotheses[0]["utterance"])
        except Exception:
            return None


