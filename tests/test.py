#!/bin/env python
import shotsfired
import unittest
import mock
import json
from werkzeug.exceptions import (
    Unauthorized,
    BadRequest,
)

unittest.util._MAX_LENGTH=2000

def jsonb(data):
    """
    Return json of bytes object
    This can be replaced by json.loads in python 3.6
    """
    return json.loads(data.decode('utf-8'))


class ShotsfiredTestCase(unittest.TestCase):
    def setUp(self):
        shotsfired.APP.config['TESTING'] = True
        self.APP = shotsfired.APP.test_client()

    @mock.patch('shotsfired.APP')
    def test_app_runs(self, mock_flask):
        """
        Test that main function starts app
        """
        shotsfired.main()
        mock_flask.run.assert_called_once_with()

    def test_no_endpoint(self):
        """
        Test that using no endpoint results in fail
        TODO: Replace this with help text or something
        """
        rv = self.APP.get('/')
        self.assertEqual(rv.status_code, 404)

    @mock.patch('shotsfired.session')
    def test_missing_event(self, mock_session):
        """
        Test that missing events don't return bogus data
        """
        rv = self.APP.get('/event/48')
        self.assertEqual(rv.data, b'No such event')
        self.assertEqual(rv.status_code, 404)

    @mock.patch('shotsfired.session')
    def test_sum_sums_shots(self, mock_session):
        """
        Test that the sum endpoint sums shots from a set
        """
        rv = self.APP.get('/sum/1')
        self.assertEqual(jsonb(rv.data), [42, 42, 45, 44, 42, 44, 43, 41, 46, 45, 46, 42])

    @mock.patch('shotsfired.session')
    def test_missing_event_sum(self, mock_session):
        """
        Test that missing events don't return bogus data
        """
        rv = self.APP.get('/sum/100')
        self.assertEqual(rv.data, b'No such event')
        self.assertEqual(rv.status_code, 404)

    @mock.patch('shotsfired.session')
    def test_validate_user(self, mock_session):
        """
        Test that function returns true if user exists
        """
        self.assertTrue(shotsfired.validate_user())

    @mock.patch('shotsfired.session')
    def test_validate_user_unknown(self, mock_session):
        """
        Test that function raises if user doesn't exist
        """
        mock_session.get.return_value = None
        with self.assertRaises(Unauthorized):
            shotsfired.validate_user()

    def test_login_success(self):
        """
        Test that a user can login
        """
        shotsfired.users = ['felix']
        rv = self.APP.post('/login', data={'username': 'felix'})
        self.assertEqual(jsonb(rv.data), {'success': True})
        self.assertEqual(rv.status_code, 200)

    def test_login_no_data(self):
        """
        Test that exception is sent if no data is sent
        """
        rv = self.APP.post('/login')
        self.assertEqual(
            rv.data,
            str.encode(BadRequest('No data sent').get_body()),
        )
        self.assertEqual(rv.status_code, 400)

    def test_login_invalid_user(self):
        """
        Test that exception is sent if user is invalid
        """
        shotsfired.users = ['ralf']
        rv = self.APP.post('/login', data={'username': 'felix'})
        self.assertEqual(
            rv.data,
            str.encode(Unauthorized('Invalid username or password').get_body()),
        )
        self.assertEqual(rv.status_code, 401)

    @mock.patch('shotsfired.session')
    def test_logout(self, mock_session):
        """
        Test that logout destroys the session
        """
        rv = self.APP.get('/logout')
        mock_session.pop.assert_called_with('username', None)
        self.assertEqual(jsonb(rv.data), {'success': True})


if __name__ == '__main__':
    unittest.main()
