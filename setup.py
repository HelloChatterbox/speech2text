from setuptools import setup

PLUGIN_ENTRY_POINT = ('chatterbox_kaldiserver_stt_plug = '
                      'speech2text.engines.kaldi:KaldiServerSTT',
                      'chatterbox_vosk_stt_plug = '
                      'speech2text.engines.kaldi:VoskKaldiSTT',
                      'chatterbox_vosk_streaming_stt_plug = '
                      'speech2text.engines.kaldi:VoskKaldiStreamingSTT',

                      'chatterbox_deepspeech_server_stt_plug = '
                      'speech2text.engines.ds:DeepSpeechServerSTT',
                      'chatterbox_deepspeech_server_streaming_stt_plug = '
                      'speech2text.engines.ds:DeepSpeechStreamServerSTT',
                      'chatterbox_deepspeech_stt_plug = '
                      'speech2text.engines.ds:DeepSpeechSTT',
                      'chatterbox_deepspeech_streaming_stt_plug = '
                      'speech2text.engines.ds:DeepSpeechStreamSTT',

                      'chatterbox_chromium_stt_plug = '
                      'speech2text.engines.google:GoogleSTT',
                      'chatterbox_google_stt_plug = '
                      'speech2text.engines.google:GoogleCloudSTT',
                      'chatterbox_google_streaming_stt_plug = '
                      'speech2text.engines.google:GoogleCloudStreamingSTT',

                      'chatterbox_bing_stt_plug = '
                      'speech2text.engines.bing:BingSTT',

                      'chatterbox_wit_stt_plug = '
                      'speech2text.engines.wit:WITSTT',

                      'chatterbox_ibm_stt_plug = '
                      'speech2text.engines.ibm:IBMSTT',

                      'chatterbox_houndify_stt_plug = '
                      'speech2text.engines.houndify:HoundifySTT',

                      'chatterbox_govivace_stt_plug = '
                      'speech2text.engines.govivace:GoVivaceSTT',

                      'chatterbox_yandex_stt_plug = '
                      'speech2text.engines.yandex:YandexSTT'

                      )

setup(
    name='speech2text',
    version='0.3.0a1',
    packages=['speech2text', 'speech2text.engines'],
    url='https://github.com/JarbasAl/speech2text',
    install_requires=["requests",
                      "SpeechRecognition>=3.8.1",
                      "ovos_utils>=0.0.8a3"],
    license='Apache2.0',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='Mycroft STT engine wrappers',
    entry_points={'mycroft.plugin.stt': PLUGIN_ENTRY_POINT}
)
