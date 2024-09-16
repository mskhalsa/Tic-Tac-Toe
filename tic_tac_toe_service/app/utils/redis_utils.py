import redis

# Returns a redis object using the passed in config
def get_redis_connection(Config):
    return redis.Redis(
        host=Config['REDIS_HOST'],
        port=Config['REDIS_PORT'],
        db=Config['REDIS_DB']
    )
