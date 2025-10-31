from populous.bloom import BloomFilter
from populous.exceptions import GenerationError

class UniquenessMixin:
    MAX_TRIES = 10000

    def get_arguments(self, unique=False, **kwargs):
        super().get_arguments(**kwargs)
        self.unique = bool(unique)
        if isinstance(unique, (list, tuple)):
            self.unique_with = tuple(unique)
        elif unique and unique is not True:
            self.unique_with = (unique,)
        else:
            self.unique_with = None
        self.seen = BloomFilter()

    def get_generator(self):
        if self.unique:
            return self.generate_uniquely()
        return super().get_generator()

    def generate_uniquely(self):
        seen = self.seen
        unique_with = self.unique_with
        tries = 0
        for value in super().get_generator():
            if isinstance(value, tuple) and hasattr(value, 'id'):
                key = value.id
            else:
                key = value
            if unique_with:
                this = self.blueprint.vars['this']
                key = (key,) + tuple((getattr(this, f) for f in unique_with))
            if key in seen:
                tries += 1
                if tries > self.MAX_TRIES:
                    raise GenerationError("Item '{}', field '{}': Could not generate a new unique value in {} tries. Aborting.".format(self.item.name, self.field_name, self.MAX_TRIES))
                continue
            tries = 0
            seen.add(key, check=False)
            yield value