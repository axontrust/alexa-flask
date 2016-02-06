#!/usr/bin/env python
from app import create_app
from flask.ext.script import Manager, Shell, Server

app = create_app('production')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command(
    'shell', Shell(make_context=make_shell_context))

manager.add_command(
    'runserver', Server(host='localhost', port=5000, threaded=True))

if __name__ == '__main__':
    manager.run()
