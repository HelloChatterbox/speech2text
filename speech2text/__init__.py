from speech2text.log import LOG
from speech2text.engines.kaldi import KaldiServerSTT
from speech2text.engines.bing import BingSTT
from speech2text.engines.ds import DeepSpeechServerSTT, \
    DeepSpeechStreamServerSTT
from speech2text.engines.govivace import GoVivaceSTT
from speech2text.engines.google import GoogleCloudStreamingSTT, \
    GoogleCloudSTT, GoogleSTT
from speech2text.engines.houndify import HoundifySTT
from speech2text.engines.yandex import YandexSTT
from speech2text.engines.ibm import IBMSTT
from speech2text.engines.wit import WITSTT


class STTFactory:
    CLASSES = {
        "google": GoogleSTT,
        "google_cloud": GoogleCloudSTT,
        "google_cloud_streaming": GoogleCloudStreamingSTT,
        "wit": WITSTT,
        "ibm": IBMSTT,
        "kaldi": KaldiServerSTT,
        "bing": BingSTT,
        "govivace": GoVivaceSTT,
        "houndify": HoundifySTT,
        "deepspeech_server": DeepSpeechServerSTT,
        "deepspeech_stream_server": DeepSpeechStreamServerSTT,
        "yandex": YandexSTT
    }

    @staticmethod
    def create(config=None, engines=None):
        engines = engines or STTFactory.CLASSES
        config = config or {"module": "google"}
        clazz = engines.get(config["module"])
        return clazz(config)
