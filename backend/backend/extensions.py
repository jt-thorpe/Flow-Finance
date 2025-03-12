"""Handles the initialisation of shared instances of used extensions."""

import logging
import os

import redis
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instnace
db = SQLAlchemy()

# Redis instance
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_cache = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# Logging
logger = logging.getLogger(__name__)
