import os 

class Config:
    SECRET_KEY = 'mehar'
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = 6379
    REDIS_DB = 0
    TTL = 3600   # Set a default ttl of 1 hour

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
