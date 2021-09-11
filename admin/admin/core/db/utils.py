import psycopg2
import psycopg2.extras
from loguru import logger
from functools import wraps

from ..settings import settings


def connect() -> psycopg2.connect or bool:
    try:
        connection = psycopg2.connect(
            host=settings.psql_host,
            port=settings.psql_port,
            user=settings.psql_user,
            password=settings.psql_password,
            database=settings.psql_db_name,
        )

        return connection

    except Exception as err:
        logger.error("Connection with DB failed")
        logger.warning(err)

        return False


def sql_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = connect()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            result = func(cursor, *args, **kwargs)
        except Exception as err:
            logger.error("SQL task could not be executed")
            logger.warning(err)

            return False

        connection.commit()

        cursor.close()
        connection.close()

        return result

    return wrapper
