import random

class NullableMixin:

    def get_arguments(self, nullable=0, **kwargs):
        super().get_arguments(**kwargs)
        if not nullable:
            self.nullable = 0
        elif nullable is True:
            self.nullable = 0.5
        else:
            self.nullable = self.parse_vars(nullable)

    def get_generator(self):
        if self.nullable:
            return self.generate_with_null()
        return super().get_generator()

    def generate_with_null(self):
        generator = super().get_generator()
        while True:
            if random.random() <= self.evaluate(self.nullable):
                yield None
            else:
                yield next(generator)