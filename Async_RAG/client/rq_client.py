from rq import Queue
from redis import Redis
import os

queue = Queue(connection=Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
))  # Assuming Redis is running on localhost with default port