import json
from typing import Final

from core.extensions import redis_cache
from users.models import User
from users.services import serialise_user_associations

CACHE_EXPIRATION: Final[int] = 60 * 30


def retrieve_user_data(user_id: str) -> dict:
    """Retrieve user data from the Redis cache.

    Deserialise the str to a JSON object and return it.
    """
    return json.loads(redis_cache.get(f"user:{user_id}"))


def cache_user_with_associations(user: User) -> None:
    """Cache user data in Redis.

    Serialise the User object into a JSON object and store it in the Redis cache.

    Args:
        user (User): the User object to cache

    Raises:
        Exception: if the user data cannot be cached
    """
    try:
        serialised_user = serialise_user_associations(user)
        serialised_user_json = json.dumps(serialised_user)
        redis_cache.set(f"user:{user.id}", serialised_user_json, ex=CACHE_EXPIRATION)
    except Exception as e:
        print(f"Unable to cache user data: {e}")
        raise e
