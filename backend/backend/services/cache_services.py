import json
from typing import Final

from backend.extensions import redis_cache
from backend.models.user_models import User
from backend.services.users_services import serialise_user_associations

CACHE_EXPIRATION: Final[int] = 60 * 30


def cache_user_with_associations(user: User) -> None:
    """Cache user and their associated data in Redis as a hash.

    Serialises the User object and stores it in Redis using separate hash fields.

    Args:
        user (User): The User object to cache.

    Raises:
        Exception: If the user data cannot be cached.
    """
    try:
        serialised_user = serialise_user_associations(user)

        print(f"{__name__} - serialised_user = {serialised_user}")

        user_data = {
            "meta": json.dumps(
                {"id": serialised_user["id"], "alias": serialised_user["alias"]}
            ),
            "transactions": json.dumps(serialised_user["transactions"]),
            "budgets": json.dumps(serialised_user["budgets"]),
        }

        # print(f"{__name__} - caching user_data = {user_data}")

        redis_cache.hset(f"user:{user.id}", mapping=user_data)
        redis_cache.expire(f"user:{user.id}", CACHE_EXPIRATION)

    except Exception as e:
        print(f"{__name__} - Unable to cache user data: {e}")
        raise e


def get_user_cache(user_id: str) -> dict | None:
    """Retrieve user data from Redis and deserialize it."""
    cached_data = redis_cache.hgetall(f"user:{user_id}")

    if not cached_data:
        return None

    return {
        "meta": json.loads(cached_data.get("meta", "{}")),
        "transactions": json.loads(cached_data.get("transactions", "[]")),
        "budgets": json.loads(cached_data.get("budgets", "[]")),
    }


def get_user_cache_field(user_id: str, field: str):
    """Fetches a specific field (e.g., incomes, expenses) from a user's cached Redis hash."""
    cache_field_data = redis_cache.hget(f"user:{user_id}", field)
    return json.loads(cache_field_data) if cache_field_data else None
