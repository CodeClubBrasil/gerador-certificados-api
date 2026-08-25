import logging

from flask import current_app
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

logger = logging.getLogger(__name__)

_mongo_client = None


def get_mongo_client():
    """Returns a shared MongoClient instance with connection pooling and configured timeouts."""
    global _mongo_client
    if _mongo_client is None:
        mongo_uri = current_app.config.get("MONGO_URI")
        if not mongo_uri:
            logger.error("MONGO_URI is not set in application configuration.")
            raise ValueError("MONGO_URI is not configured.")

        server_selection_timeout = current_app.config.get("MONGO_SERVER_SELECTION_TIMEOUT_MS", 5000)
        connect_timeout = current_app.config.get("MONGO_CONNECT_TIMEOUT_MS", 10000)
        socket_timeout = current_app.config.get("MONGO_SOCKET_TIMEOUT_MS", 20000)
        max_idle_time = current_app.config.get("MONGO_MAX_IDLE_TIME_MS", 120000)
        retry_writes = current_app.config.get("MONGO_RETRY_WRITES", True)

        _mongo_client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=server_selection_timeout,
            connectTimeoutMS=connect_timeout,
            socketTimeoutMS=socket_timeout,
            maxIdleTimeMS=max_idle_time,
            retryWrites=retry_writes,
        )
        logger.info("Shared MongoClient connection pool initialized.")
    return _mongo_client


def get_db():
    """Returns the application MongoDB database instance from the shared client."""
    client = get_mongo_client()
    db_name = current_app.config.get("MONGO_DB_NAME", "ccbrcertificados")
    return client[db_name]


def ping_db():
    """Pings the database to verify connectivity. Returns a tuple (is_connected: bool, message: str)."""
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True, "connected"
    except (ConnectionFailure, PyMongoError, ValueError, OSError, RuntimeError) as e:
        logger.warning(f"Database health check failed: {e}")
        return False, str(e)



def close_db(e=None):
    """Closes the shared MongoClient connection pool if active."""
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None
        logger.info("MongoClient connection closed.")
