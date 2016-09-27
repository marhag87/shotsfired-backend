#!/bin/env python
"""
Shotsfired backend
"""
from flask import (
    Flask,
    request,
    session,
)
from flask.json import jsonify
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
)
from data import (
    event,
    users,
)
APP = Flask(__name__)
APP.secret_key = 'dev stuff'


def validate_user():
    """
    Checks if a user is logged in
    """
    if session.get('username') is None:
        raise Unauthorized('You are not logged in')
    return True


@APP.route('/login', methods=['POST'])
def login():
    """
    Login the user
    """
    username = request.form.get('username')
    if username is None:
        raise BadRequest('No data sent')
    else:
        if username in users:
            session['username'] = username
            return jsonify({'success': True})
        else:
            raise Unauthorized('Invalid username or password')


@APP.route('/logout')
def logout():
    """
    Destroy the user session
    """
    session.pop('username', None)
    return jsonify({'success': True})


@APP.route('/event/<int:event_id>')
def get_event(event_id):
    """
    Get entire event
    """
    validate_user()
    try:
        return jsonify(event[event_id])
    except IndexError:
        return "No such event", 404


@APP.route('/sum/<int:event_id>')
def get_sum(event_id):
    """
    Get sums of shots for set
    """
    validate_user()
    try:
        sums = [sum(x.get('shots')) for x in event[event_id].get('sets')]
        return jsonify(sums)
    except IndexError:
        return "No such event", 404


def main():
    """
    Start the application
    """
    APP.run()


if __name__ == '__main__': # pragma: no cover
    main()
