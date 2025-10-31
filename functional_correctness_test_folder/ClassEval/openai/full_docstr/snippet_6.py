
class AutomaticGuitarSimulator:
    def __init__(self, text) -> None:
        """
        Initialize the score to be played
        :param text:str, score to be played
        """
        self.play_text = text

    def interpret(self, display=False):
        """
        Interpret the music score to be played
        :param display:Bool, representing whether to print the interpreted score
        :return: list of dict, The dict includes two fields, Chord and Tune, which are letters and numbers, respectively. If the input is empty or contains only whitespace, an empty list is returned.
        >>> context = AutomaticGuitarSimulator("C53231323 Em43231323 F43231323 G63231323")
        >>> play_list = context.interpret(display = False)
        [{'Chord': 'C', 'Tune': '53231323'}, {'Chord': 'Em', 'Tune': '43231323'}, {'Chord': 'F', 'Tune': '43231323'}, {'Chord': 'G', 'Tune': '63231323'}]
        """
        if not self.play_text or not self.play_text.strip():
            return []

        result = []
        tokens = self.play_text.strip().split()
        for token in tokens:
            # Find the first digit in the token
            idx = None
            for i, ch in enumerate(token):
                if ch.isdigit():
                    idx = i
                    break
            if idx is None:
                # No digits found; treat whole token as chord with empty tune
                chord = token
                tune = ""
            else:
                chord = token[:idx]
                tune = token[idx:]
            entry = {"Chord": chord, "Tune": tune}
            result.append(entry)
            if display:
                print(self.display(chord, tune))
        return result

    def display(self, key, value):
        """
        Print out chord and play tune with following format: Normal Guitar Playing -- Chord: %s, Play Tune: %s
        :param key:str, chord
        :param value:str, play tune
        :return: str
        >>> context = AutomaticGuitarSimulator("C53231323 Em43231323 F43231323 G63231323")
        >>> context.display("C", "53231323")
        Normal Guitar Playing -- Chord: C, Play Tune: 53231323
        """
        output = f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"
        return output
