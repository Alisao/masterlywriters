import unittest
from flask_testing import TestCase
from flask_login import current_user
from project import app, db
from project.models import ClientPosts, User
from werkzeug.utils import cached_property

class BaseTestCase(TestCase):
    
    def create_app(self):
        app.config.from_object("config.TestConfig")
        return app

    def setUp(self):
        db.create_all()
        db.session.add(ClientPosts('manu', 'ni bazenga'))
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
   
    def test_landing_page_loads(self):
        response = self.client.get('/', content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_index_has_text(self):
        response = self.client.get('/', content_type="html/text")
        self.assertTrue(b"place your order now" in response.data)


class UserViewsTests(BaseTestCase):

    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username='admin', pswd='admin'),
                follow_redirects=True
            )
            self.assertTrue(b'logout' in response.data)
            self.assertTrue(current_user.username =='admin')
            self.assertTrue(current_user.is_active)
    
    def test_incorrect_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username='amin', pswd='admin'),
                follow_redirects=True
            )
            self.assertTrue(b'invalid credentials. please try again' in response.data)

    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username='admin', pswd='admin'),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertTrue(b'login', response.data)
            self.assertFalse(current_user.is_active)
        


if __name__ == "__main__":
    unittest.main()
        