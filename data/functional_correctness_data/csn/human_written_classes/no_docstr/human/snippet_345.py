from django.db import reset_queries
import random

class Plugin:

    def random_reset(self):
        if random.random() <= reset_chance:
            reset_queries()

    def city_post(self, parser, city, item):
        self.random_reset()

    def district_post(self, parser, district, item):
        self.random_reset()