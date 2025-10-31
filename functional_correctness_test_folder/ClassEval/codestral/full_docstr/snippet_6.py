
class AutomaticGuitarSimulator:
    def __init__(self, text) -> None:
        self.play_text = text

    def interpret(self, display=False):
        if not self.play_text or self.play_text.isspace():
            return []

        play_list = []
        parts = self.play_text.split()

        for part in parts:
            chord = ''.join([c for c in part if c.isalpha()])
            tune = ''.join([c for c in part if c.isdigit()])
            play_list.append({'Chord': chord, 'Tune': tune})

            if display:
                self.display(chord, tune)

        return play_list

    def display(self, key, value):
        print(f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}")
