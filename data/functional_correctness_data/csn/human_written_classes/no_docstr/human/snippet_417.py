import json

class shadowCallbackContainer:

    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    def customShadowCallback_Delta(self, payload, responseStatus, token):
        print('Received a delta message:')
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict['state'])
        print(deltaMessage)
        print('Request to update the reported state...')
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        print('Sent.')