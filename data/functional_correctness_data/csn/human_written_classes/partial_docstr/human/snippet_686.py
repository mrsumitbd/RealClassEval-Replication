class InlineKeyboardButton:
    """ This object represents one button of an inline keyboard. You must use exactly one of the optional fields.

    Attributes:
        text     (str)  :Label text on the button
        url      (str)  :*Optional.* HTTP url to be opened when button is pressed
        callback_data (str) :*Optional.* Data to be sent in a callback query to the bot when button is pressed

        switch_inline_query (str) :*Optional.* If set, pressing the button will prompt the user to select
                                   one of their chats, open that chat and insert the bot‘s username and
                                   the specified inline query in the input field. Can be empty, in which case just the bot’s username will be inserted.

                                   Note: This offers an easy way for users to start using your bot in inline mode when they are currently in a private
                                   chat with it. Especially useful when combined with switch_pm… actions – in this case the user will be automatically
                                   returned to the chat they switched from, skipping the chat selection screen.
        switch_inline_query_current_chat (str) :*Optional.* If set, pressing the button will insert the bot‘s username and the specified inline query
                                                in the current chat's input field. Can be empty, in which case only the bot’s username will be inserted.

                                                This offers a quick way for the user to open your bot in inline mode in the same chat – good for
                                                selecting something from multiple options.
        callback_game (str) :*Optional.*  Description of the game that will be launched when the user presses the button.

                                          NOTE: This type of button must always be the first button in the first row.
        pay (bool)          :*Optional.*  Specify True, to send a Pay button.

                                          NOTE: This type of button must always be the first button in the first row.
    """

    def __init__(self, text, url=None, callback_data=None, switch_inline_query=None, switch_inline_query_current_chat=None, callback_game=None, pay=None):
        self.text = text
        self.url = url
        self.callback_data = str(callback_data)
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        if sum(map(bool, [url, callback_data, switch_inline_query, switch_inline_query_current_chat, callback_game])) != 1:
            raise ValueError('You must use exactly one of the optional fields.')

    def serialize(self):
        reply_markup = dict()
        reply_markup['text'] = self.text
        if self.url is not None:
            reply_markup['url'] = self.url
        if self.callback_data is not None:
            reply_markup['callback_data'] = self.callback_data
        if self.switch_inline_query is not None:
            reply_markup['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            reply_markup['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            reply_markup['callback_game'] = self.callback_game
        return reply_markup