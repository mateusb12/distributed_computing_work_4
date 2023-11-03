import redis


def get_redis_connection() -> redis.client.Redis or None:
    redis_host = "localhost"
    redis_port = 6379
    try:
        redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        redis_conn.ping()  # Ping Redis to check if connection is alive
    except (ConnectionError, redis.exceptions.RedisError):
        redis_conn = None
    return redis_conn
