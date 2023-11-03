import redis


def get_redis_connection() -> redis.client.Redis or None:
    # When running inside Docker, use "redis" as the hostname which is the service name defined in docker-compose.yml
    redis_host = "redis"  # Changed from "localhost" to "redis"
    redis_port = 6379
    try:
        redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        redis_conn.ping()  # Ping Redis to check if connection is alive
        print("Connected to Redis")
    except (ConnectionError, redis.exceptions.RedisError) as e:
        print(f"Failed to connect to Redis: {e}")
        redis_conn = None
    return redis_conn


def __main():
    test_conn = get_redis_connection()
    return


if __name__ == '__main__':
    __main()
