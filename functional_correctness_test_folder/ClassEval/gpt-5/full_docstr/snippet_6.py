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
        if not self.play_text or self.play_text.strip() == "":
            return []
        result = []
        for token in self.play_text.split():
            if not token:
                continue
            i = 0
            n = len(token)
            while i < n and token[i].isalpha():
                i += 1
            chord = token[:i]
            tune = token[i:]
            item = {"Chord": chord, "Tune": tune}
            result.append(item)
            if display:
                self.display(chord, tune)
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
        s = f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"
        print(s)
        return s
