from culqi.utils.validation.country_codes import get_country_codes
from culqi.utils.validation.helpers import Helpers
from culqi.utils.errors import CustomException

class CustomerValidation:

    def create(self, data):
        if not data.get('first_name'):
            raise CustomException('first name is empty.')
        if not data.get('last_name'):
            raise CustomException('last name is empty.')
        if not data.get('address'):
            raise CustomException('address is empty.')
        if not data.get('address_city'):
            raise CustomException('address_city is empty.')
        Helpers.validate_value(data['country_code'], get_country_codes())
        if not Helpers.is_valid_email(data['email']):
            raise CustomException('Invalid email.')

    def retrieve(self, id):
        Helpers.validate_string_start(id, 'cus')

    def update(self, id):
        Helpers.validate_string_start(id, 'cus')

    def list(self, data):
        if 'email' in data:
            if not Helpers.is_valid_email(data['email']):
                raise CustomException('Invalid email.')
        if 'country_code' in data:
            Helpers.validate_value(data['country_code'], get_country_codes())