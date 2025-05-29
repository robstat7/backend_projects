import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0,\
				 decode_responses=True)

def get_cache(key):
    """Get cached data by key."""
    data = redis_client.get(key)
    return json.loads(data) if data else None

def set_cache(key, value, expiry=3600):
    """Set cache data with a key and expiry time."""
    redis_client.setex(key, expiry, json.dumps(value))
