"""Handles the initialisation of shared instances of used extensions."""

import os
from typing import Final

import redis
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instnace
db = SQLAlchemy()

# Redis instance
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_cache = redis.Redis(host=redis_host, port=6379, decode_responses=True)
CACHE_EXPIRATION: Final[int] = 60 * 30
