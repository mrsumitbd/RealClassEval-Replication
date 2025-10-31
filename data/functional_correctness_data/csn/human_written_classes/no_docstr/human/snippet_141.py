class Voice:

    def __init__(self, id, name=None, languages=None, gender=None, age=None) -> None:
        self.id = id
        self.name = name
        self.languages = languages or []
        self.gender = gender
        self.age = age

    def __str__(self) -> str:
        return '<Voice id={id}\n          name={name}\n          languages={languages}\n          gender={gender}\n          age={age}>'.format(**self.__dict__)