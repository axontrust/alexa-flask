import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config = {
    'production': ProductionConfig,
}
