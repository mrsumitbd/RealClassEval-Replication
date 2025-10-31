class CallbackQuery:

    def __init__(self, bot, src):
        self.bot = bot
        self.query_id = src['id']
        self.data = src['data']
        self.src = src

    def answer(self, **options):
        return self.bot.api_call('answerCallbackQuery', callback_query_id=self.query_id, **options)