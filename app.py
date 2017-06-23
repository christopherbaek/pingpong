"""
The admin web application
"""
from flask import Flask, render_template


# The Flask application
APP = Flask(__name__)


@APP.route('/')
def index():
    """
    The root route of the Flask application
    """
    return render_template(
        'index.html',
        application_name='Ping Pong Server Admin')


if __name__ == '__main__':
    APP.run()
