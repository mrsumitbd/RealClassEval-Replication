
from flask import request, jsonify


class BasePagination:
    '''
    The base class each Pagination class should implement.
    '''

    def paginate_query(self, query, request):
        '''
        :param query: SQLAlchemy ``query``.
        :param request: The request from the view
        :return: The paginated date based on the provided query and request.
        '''
        raise NotImplementedError("Subclasses must implement this method")

    def get_paginated_response(self, data):
        '''
        :param data: The paginated data.
        :return: A JSON response with the paginated data.
        '''
        raise NotImplementedError("Subclasses must implement this method")


class Pagination(BasePagination):
    def paginate_query(self, query, request):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        paginated_query = query.paginate(
            page=page, per_page=per_page, error_out=False)
        return {
            'data': paginated_query.items,
            'page': page,
            'per_page': per_page,
            'total': paginated_query.total
        }

    def get_paginated_response(self, data):
        return jsonify({
            'data': [item.to_dict() if hasattr(item, 'to_dict') else item for item in data['data']],
            'pagination': {
                'page': data['page'],
                'per_page': data['per_page'],
                'total': data['total']
            }
        })


# Example usage
if __name__ == "__main__":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)

        def to_dict(self):
            return {'id': self.id, 'name': self.name}

    @app.route('/users', methods=['GET'])
    def get_users():
        pagination = Pagination()
        query = User.query
        paginated_data = pagination.paginate_query(query, request)
        return pagination.get_paginated_response(paginated_data)

    with app.app_context():
        db.create_all()
        # Populate the database with some data
        for i in range(100):
            user = User(name=f'User {i}')
            db.session.add(user)
        db.session.commit()

    app.run(debug=True)
