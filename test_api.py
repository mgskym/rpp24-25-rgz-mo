from app import app
from db import db
from db.models import users, operations, actions
import unittest
import os

class TestIntegrations(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.secret_key = os.environ.get('APP_SECRET_KEY')
        user_db = os.environ.get('USER_DB')
        host_ip = "localhost"
        host_port = "5432"
        database_name = os.environ.get('DATABASE_NAME')
        password = os.environ.get('PASSWORD')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
        self.app = app.test_client()
        # db.create_all()

    def test_thing(self):
    #    newUser = users(
    #             username = 'test_user',
    #             email = 'mail@mail.com',
    #             password = '000000'
    #         )
    #     db.session.add(newUser)
    #     db.session.commit()
        response = self.app.post('/delete', {
            'id': 4
        })
        print(response)
        self.assertGreaterEqual(response, 'OK')
    
    # def tearDown(self):
    #     # db.session.remove()
    #     # db.drop_all()


if __name__ == '__main__':
    unittest.main()