import redis
from typing import Dict, Union

import ujson

from .settings import settings


def create_pool():
    global conn
    conn = redis.Redis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )


def close_redis():
    conn.close()


def load_data(key: str) -> Dict[str, Union[str, int, None]]:
    file = conn.get(key)
    if file is None:
        return None

    return ujson.loads(file)


def dump_data(key: str, value: Dict[str, Union[str, int, None]]) -> None:
    conn.set(
        key,
        ujson.dumps(value),
    )
    conn.expire(key, 24 * 60 * 60)


def remove_data(key: str) -> None:
    conn.delete(key)


create_pool()
