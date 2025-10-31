import logging
from mireport.conversionresults import Message, MessageType, Severity
from arelle.logging.handlers.LogToXmlHandler import LogToXmlHandler
import json
from mireport.filesupport import FilelikeAndFileName
from typing import Any, MutableMapping, NamedTuple, Optional, Self

class ArelleProcessingResult:
    """Holds the results of processing an XBRL file with Arelle."""
    _INTERESTING_LOG_MESSAGES = ('validated in', 'loaded in')

    def __init__(self, jsonMessages: str, textLogLines: list[str]):
        self._validationMessages: list[Message] = []
        self._textLogLines: list[str] = textLogLines
        self._viewer: Optional[FilelikeAndFileName] = None
        self._xbrlJson: Optional[FilelikeAndFileName] = None
        self.__importArelleMessages(jsonMessages)

    def __importArelleMessages(self, json_str: str) -> None:
        wantDebug = L.isEnabledFor(logging.DEBUG)
        records: list[dict] = json.loads(json_str)['log']
        for r in records:
            code: str = r.get('code', '')
            level: str = r.get('level', '')
            text: str = r.get('message', {}).get('text', '')
            fact: Optional[str] = r.get('message', {}).get('fact')
            if wantDebug:
                L.debug(f'code={code!r} level={level!r} text={text!r} fact={fact!r}')
            if code == 'info' and text.startswith('Option '):
                continue
            match code:
                case 'info' | '':
                    if '' == code or any((a in text for a in ArelleProcessingResult._INTERESTING_LOG_MESSAGES)):
                        self._validationMessages.append(Message(messageText=text, severity=Severity.INFO, messageType=MessageType.DevInfo))
                case _:
                    messageText = f'[{code}] {text}'
                    self._validationMessages.append(Message(messageText=messageText, severity=Severity.fromLogLevelString(level), messageType=MessageType.XbrlValidation, conceptQName=fact))

    @classmethod
    def fromLogToXmlHandler(cls, logHandler: LogToXmlHandler) -> Self:
        json = logHandler.getJson(clearLogBuffer=False)
        logLines = logHandler.getLines(clearLogBuffer=False)
        logHandler.clearLogBuffer()
        return cls(json, logLines)

    @property
    def viewer(self) -> FilelikeAndFileName:
        if self._viewer is not None:
            return self._viewer
        raise ArelleRelatedException('No viewer stored/retrieved.')

    @property
    def xBRL_JSON(self) -> FilelikeAndFileName:
        if self._xbrlJson is not None:
            return self._xbrlJson
        raise ArelleRelatedException('No JSON stored/retrieved.')

    @property
    def messages(self) -> list[Message]:
        return list(self._validationMessages)

    @property
    def logLines(self) -> list[str]:
        return list(self._textLogLines)