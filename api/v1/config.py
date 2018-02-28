class Config(object):
    """Base config class."""
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


class DevelopmentConfig(Config):
    """Development Configs."""
    DEBUG = True


class ProductionConfig(Config):
    """Production Configs."""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Test Configs"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
