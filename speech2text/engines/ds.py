from speech2text.engines import StreamingSTT, StreamThread, STT
import requests
from queue import Queue
from speech2text.log import LOG
from timeit import default_timer as timer


class DeepSpeechServerSTT(STT):
    """
        STT interface for the deepspeech-server:
        https://github.com/MainRo/deepspeech-server
        use this if you want to host DeepSpeech yourself
    """

    def execute(self, audio, language=None):
        language = language or self.lang
        if not language.startswith("en"):
            raise ValueError("Deepspeech is currently english only")
        response = requests.post(self.config.get("uri"),
                                 data=audio.get_wav_data())
        return response.text


class DeepSpeechStreamServerThread(StreamThread):
    def __init__(self, queue, language, url):
        if not language.startswith("en"):
            raise ValueError("Deepspeech is currently english only")
        super().__init__(queue, language)
        self.url = url

    def handle_audio_stream(self, audio, language):
        self.response = requests.post(self.url, data=audio, stream=True)
        self.text = self.response.text if self.response else None
        return self.text


class DeepSpeechStreamServerSTT(StreamingSTT):
    """
        Streaming STT interface for the deepspeech-server:
        https://github.com/JPEWdev/deep-dregs
        use this if you want to host DeepSpeech yourself
        STT config will look like this:

        "stt": {
            "module": "deepspeech_stream_server",
            "deepspeech_stream_server": {
                "stream_uri": "http://localhost:8080/stt?format=16K_PCM16"
        ...
    """

    def create_streaming_thread(self):
        self.queue = Queue()
        return DeepSpeechStreamServerThread(
            self.queue,
            self.lang,
            self.config.get('stream_uri')
        )


class DeepSpeechSTT(STT):

    def __init__(self, config):
        super().__init__(config)
        global DeepSpeechModel, np
        from deepspeech import Model as DeepSpeechModel
        import numpy as np
        model = self.config.get("model")
        scorer = self.config.get("scorer")
        self.ds = self.load_model(model, scorer)

    @staticmethod
    def load_model(models, scorer):
        '''
        Load the pre-trained model into the memory
        @param models: Output Grapgh Protocol Buffer file
        @param scorer: Scorer file
        @Retval
        Returns DeepSpeech Object
        '''
        model_load_start = timer()
        ds = DeepSpeechModel(models)
        model_load_end = timer() - model_load_start
        LOG.debug("Loaded model in %0.3fs." % (model_load_end))

        scorer_load_start = timer()
        ds.enableExternalScorer(scorer)
        scorer_load_end = timer() - scorer_load_start
        LOG.debug('Loaded external scorer in %0.3fs.' % (scorer_load_end))

        return ds

    def execute(self, audio, language=None):
        audio = np.frombuffer(audio.frame_data, np.int16)
        return self.ds.stt(audio)


class DeepSpeechStreamThread(StreamThread):
    def __init__(self, queue, language, ds):
        super().__init__(queue, language)
        self.ds = ds

    def handle_audio_stream(self, audio, language):
        for a in audio:
            data = np.frombuffer(a, np.int16)
            self.ds.feedAudioContent(data)
            # self.text = self.ds.intermediateDecode()
        return self.text

    def finalize(self):
        self.text = self.ds.finishStream()


class DeepSpeechStreamSTT(StreamingSTT, DeepSpeechSTT):
    def create_streaming_thread(self):
        self.queue = Queue()
        return DeepSpeechStreamThread(
            self.queue,
            self.lang,
            self.ds.createStream()
        )


