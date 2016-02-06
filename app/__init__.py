import logging
import sys

from flask import Flask
from config import config

reload(sys)
sys.setdefaultencoding('utf-8')


def log_remove_root_handlers():
    try:
        root = logging.getLogger()
        for handler in root.handlers:
            root.removeHandler(handler)
    except Exception, e:
        logging.error('exception=%s', repr(e))
        pass


def log_setup(level=None, name=None):
    lformat = '%(asctime)s %(levelname)s  %(message)s'\
        '\t[%(module)s:%(funcName)s()]'\
        '\t[%(pathname)s:%(lineno)d]'
    logging.basicConfig(format=lformat, level=level)


log_remove_root_handlers()
log_setup(level=logging.DEBUG)
logger = logging.getLogger()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .root import root as root_blueprint
    app.register_blueprint(root_blueprint)

    return app
