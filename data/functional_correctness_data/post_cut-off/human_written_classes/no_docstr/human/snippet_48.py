from chat_engine.contexts.handler_context import HandlerContext, HandlerResultType

class ChatDataSubmitter:

    def __init__(self, handler_name: str, output_info, session_context, sinks, outputs):
        self.handler_name = handler_name
        self.output_info = output_info
        self.session_context = session_context
        self.sinks = sinks
        self.outputs = outputs

    def submit(self, data: HandlerResultType):
        ChatSession.submit_data(data, self.handler_name, self.output_info, self.session_context, self.sinks, self.outputs)