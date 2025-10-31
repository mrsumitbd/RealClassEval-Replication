import json
import platform
from dashscope.protocol.websocket import ACTION_KEY, EVENT_KEY, HEADER, TASK_ID, ActionType, EventType, WebsocketStreamingMode
import uuid

class Request:

    def __init__(self, apikey, model, voice, format='wav', sample_rate=16000, bit_rate=64000, volume=50, speech_rate=1.0, pitch_rate=1.0, seed=0, synthesis_type=0, instruction=None, language_hints: list=None):
        self.task_id = self.genUid()
        self.apikey = apikey
        self.voice = voice
        self.model = model
        self.format = format
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.volume = volume
        self.speech_rate = speech_rate
        self.pitch_rate = pitch_rate
        self.seed = seed
        self.synthesis_type = synthesis_type
        self.instruction = instruction
        self.language_hints = language_hints

    def genUid(self):
        return uuid.uuid4().hex

    def getWebsocketHeaders(self, headers, workspace):
        ua = 'dashscope/%s; python/%s; platform/%s; processor/%s' % ('1.18.0', platform.python_version(), platform.platform(), platform.processor())
        self.headers = {'user-agent': ua, 'Authorization': 'bearer ' + self.apikey}
        if headers:
            self.headers = {**self.headers, **headers}
        if workspace:
            self.headers = {**self.headers, 'X-DashScope-WorkSpace': workspace}
        return self.headers

    def getStartRequest(self, additional_params=None):
        cmd = {HEADER: {ACTION_KEY: ActionType.START, TASK_ID: self.task_id, 'streaming': WebsocketStreamingMode.DUPLEX}, 'payload': {'model': self.model, 'task_group': 'audio', 'task': 'tts', 'function': 'SpeechSynthesizer', 'input': {}, 'parameters': {'voice': self.voice, 'volume': self.volume, 'text_type': 'PlainText', 'sample_rate': self.sample_rate, 'rate': self.speech_rate, 'format': self.format, 'pitch': self.pitch_rate, 'seed': self.seed, 'type': self.synthesis_type}}}
        if self.format == 'opus':
            cmd['payload']['parameters']['bit_rate'] = self.bit_rate
        if additional_params:
            cmd['payload']['parameters'].update(additional_params)
        if self.instruction is not None:
            cmd['payload']['parameters']['instruction'] = self.instruction
        if self.language_hints is not None:
            cmd['payload']['parameters']['language_hints'] = self.language_hints
        return json.dumps(cmd)

    def getContinueRequest(self, text):
        cmd = {HEADER: {ACTION_KEY: ActionType.CONTINUE, TASK_ID: self.task_id, 'streaming': WebsocketStreamingMode.DUPLEX}, 'payload': {'model': self.model, 'task_group': 'audio', 'task': 'tts', 'function': 'SpeechSynthesizer', 'input': {'text': text}}}
        return json.dumps(cmd)

    def getFinishRequest(self):
        cmd = {HEADER: {ACTION_KEY: ActionType.FINISHED, TASK_ID: self.task_id, 'streaming': WebsocketStreamingMode.DUPLEX}, 'payload': {'input': {}}}
        return json.dumps(cmd)