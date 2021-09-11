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


def load_data(file_id: str) -> Dict[str, Union[str, int, None]]:
    file = conn.get(file_id)
    if file is None:
        return None

    return ujson.loads(file)


def dump_data(file_id: str, file_data: Dict[str, Union[str, int, None]]) -> None:
    conn.set(
        file_id,
        ujson.dumps(file_data),
    )
    conn.expire(file_id, 24 * 60 * 60)


def remove_data(file_id: str) -> None:
    conn.delete(file_id)


create_pool()
