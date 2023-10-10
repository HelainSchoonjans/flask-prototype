import unittest
import json
from app import create_app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, World!')

    def test_login(self):
        data = json.dumps({'username': 'username', 'password': 'password'})
        response = self.app.post('/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data.decode('utf-8')))

    def test_login_invalid_credentials(self):
        data = json.dumps({'username': 'invalid', 'password': 'invalid'})
        response = self.app.post('/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', json.loads(response.data.decode('utf-8'))['message'])

    def test_protected_endpoint(self):
        # Obtain a JWT token by logging in
        login_data = json.dumps({'username': 'username', 'password': 'password'})
        login_response = self.app.post('/login', data=login_data, content_type='application/json')
        access_token = json.loads(login_response.data.decode('utf-8'))['access_token']

        # Access the protected endpoint using the JWT token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged_in_as', json.loads(response.data.decode('utf-8')))

if __name__ == '__main__':
    unittest.main()
