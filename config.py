import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'ccbrcertificados')
    MONGO_SERVER_SELECTION_TIMEOUT_MS = int(os.getenv('MONGO_SERVER_SELECTION_TIMEOUT_MS', '5000'))
    MONGO_CONNECT_TIMEOUT_MS = int(os.getenv('MONGO_CONNECT_TIMEOUT_MS', '10000'))
    MONGO_SOCKET_TIMEOUT_MS = int(os.getenv('MONGO_SOCKET_TIMEOUT_MS', '20000'))
    MONGO_MAX_IDLE_TIME_MS = int(os.getenv('MONGO_MAX_IDLE_TIME_MS', '120000'))
    MONGO_RETRY_WRITES = os.getenv('MONGO_RETRY_WRITES', 'true').lower() in ('true', '1', 't')

