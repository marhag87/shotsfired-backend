#!/bin/env python
import shotsfired
import unittest
import mock
import json

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

    def test_missing_event(self):
        """
        Test that missing events don't return bogus data
        """
        rv = self.APP.get('/event/3')
        self.assertEqual(rv.data, b'No such event')
        self.assertEqual(rv.status_code, 404)

    def test_sum_sums_shots(self):
        """
        Test that the sum endpoint sums shots from a set
        """
        rv = self.APP.get('/sum/1')
        self.assertEqual(jsonb(rv.data), [45, 46])

    def test_missing_event_sum(self):
        """
        Test that missing events don't return bogus data
        """
        rv = self.APP.get('/sum/3')
        self.assertEqual(rv.data, b'No such event')
        self.assertEqual(rv.status_code, 404)


if __name__ == '__main__':
    unittest.main()
