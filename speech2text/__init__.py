from ovos_utils.log import LOG
from speech2text.engines.kaldi import KaldiServerSTT, VoskKaldiSTT, VoskKaldiStreamingSTT
from speech2text.engines.bing import BingSTT
from speech2text.engines.ds import DeepSpeechServerSTT, \
    DeepSpeechStreamServerSTT, DeepSpeechSTT, DeepSpeechStreamSTT
from speech2text.engines.govivace import GoVivaceSTT
from speech2text.engines.google import GoogleCloudStreamingSTT, \
    GoogleCloudSTT
from speech2text.engines.houndify import HoundifySTT
from speech2text.engines.yandex import YandexSTT
from speech2text.engines.ibm import IBMSTT
from speech2text.engines.wit import WITSTT
from jarbas_stt_plugin_chromium import ChromiumSTT


class STTFactory:
    CLASSES = {
        "google": ChromiumSTT,
        "chromium": ChromiumSTT,
        "google_cloud": GoogleCloudSTT,
        "google_cloud_streaming": GoogleCloudStreamingSTT,
        "wit": WITSTT,
        "ibm": IBMSTT,
        "kaldi_server": KaldiServerSTT,
        "kaldi_vosk": VoskKaldiSTT,
        "kaldi_vosk_streaming": VoskKaldiStreamingSTT,
        "bing": BingSTT,
        "govivace": GoVivaceSTT,
        "houndify": HoundifySTT,
        "deepspeech_server": DeepSpeechServerSTT,
        "deepspeech_stream_server": DeepSpeechStreamServerSTT,
        "deepspeech": DeepSpeechSTT,
        "deepspeech_streaming": DeepSpeechStreamSTT,
        "yandex": YandexSTT
    }

    @staticmethod
    def create(config=None, engines=None):
        engines = engines or STTFactory.CLASSES
        config = config or {"module": "google"}
        module = config["module"]
        module_config = config.get(module, config)
        stt = engines.get(module)()
        stt.config = module_config
        stt.credential = module_config.get("credential", {})
        return stt
