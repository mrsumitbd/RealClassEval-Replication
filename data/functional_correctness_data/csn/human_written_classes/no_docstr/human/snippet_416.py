import time
import logging
from threading import Lock

class shadowManager:
    _logger = logging.getLogger(__name__)

    def __init__(self, srcMQTTCore):
        if srcMQTTCore is None:
            raise TypeError('None type inputs detected.')
        self._mqttCoreHandler = srcMQTTCore
        self._shadowSubUnsubOperationLock = Lock()

    def basicShadowPublish(self, srcShadowName, srcShadowAction, srcPayload):
        currentShadowAction = _shadowAction(srcShadowName, srcShadowAction)
        self._mqttCoreHandler.publish(currentShadowAction.getTopicGeneral(), srcPayload, 0, False)

    def basicShadowSubscribe(self, srcShadowName, srcShadowAction, srcCallback):
        with self._shadowSubUnsubOperationLock:
            currentShadowAction = _shadowAction(srcShadowName, srcShadowAction)
            if currentShadowAction.isDelta:
                self._mqttCoreHandler.subscribe(currentShadowAction.getTopicDelta(), 0, srcCallback)
            else:
                self._mqttCoreHandler.subscribe(currentShadowAction.getTopicAccept(), 0, srcCallback)
                self._mqttCoreHandler.subscribe(currentShadowAction.getTopicReject(), 0, srcCallback)
            time.sleep(2)

    def basicShadowUnsubscribe(self, srcShadowName, srcShadowAction):
        with self._shadowSubUnsubOperationLock:
            currentShadowAction = _shadowAction(srcShadowName, srcShadowAction)
            if currentShadowAction.isDelta:
                self._mqttCoreHandler.unsubscribe(currentShadowAction.getTopicDelta())
            else:
                self._logger.debug(currentShadowAction.getTopicAccept())
                self._mqttCoreHandler.unsubscribe(currentShadowAction.getTopicAccept())
                self._logger.debug(currentShadowAction.getTopicReject())
                self._mqttCoreHandler.unsubscribe(currentShadowAction.getTopicReject())