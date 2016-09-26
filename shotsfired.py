#!/bin/env python
"""
Shotsfired backend
"""
from flask import Flask
from flask.json import jsonify
from data import event
APP = Flask(__name__)


@APP.route('/event/<int:event_id>')
def get_event(event_id):
    """
    Get entire event
    """
    try:
        return jsonify(event[event_id])
    except IndexError:
        return "No such event", 404


@APP.route('/sum/<int:event_id>')
def get_sum(event_id):
    """
    Get sums of shots for set
    """
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
