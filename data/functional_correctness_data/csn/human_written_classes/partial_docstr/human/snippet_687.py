import json

class InlineKeyboardMarkup:
    """ This object represents an inline keyboard that appears right next to the message it belongs to.

    Attributes:
        inline_keyboard     (Sequence[Sequence[InlineKeyboardButton]])  :Array of button rows, each represented by an Array of InlineKeyboardButton objects
    """

    def __init__(self, inline_keyboard):
        self.inline_keyboard = inline_keyboard

    def serialize(self):
        return json.dumps(self.asdict())

    def asdict(self):
        inline_keyboard = []
        for button_list in self.inline_keyboard:
            temp_list = []
            for button in button_list:
                temp_list.append(button.serialize())
            inline_keyboard.append(temp_list)
        return dict(inline_keyboard=inline_keyboard)