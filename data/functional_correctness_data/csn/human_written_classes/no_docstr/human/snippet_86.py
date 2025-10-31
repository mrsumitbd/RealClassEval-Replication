class UserPrompt:

    def __init__(self, allow_labelling: bool, allow_backstep: bool) -> None:
        options = []
        if allow_labelling:
            options += [InputOptions.YES, InputOptions.NO]
        options.append(InputOptions.SKIP)
        if allow_backstep:
            options.append(InputOptions.BACK)
        options.append(InputOptions.QUIT)
        self.valid_input = {option.name[0] for option in options}
        self.options = [option.name.lower() for option in options]

    def __str__(self) -> str:
        if 'Y' in self.valid_input:
            output = 'Should this string be committed to the repository?'
        else:
            output = 'What would you like to do?'
        options = ', '.join([f'({option[0]}){option[1:]}' for option in self.options])
        return output + ' ' + options + ': '