from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from pymongo.errors import ConnectionFailure

import certificados.db as db_module


@pytest.fixture(autouse=True)
def cleanup_db():
    db_module.close_db()
    yield
    db_module.close_db()


def test_get_mongo_client_missing_uri():
    app = Flask(__name__)
    app.config["MONGO_URI"] = None

    with app.app_context(), pytest.raises(ValueError, match="MONGO_URI is not configured"):
        db_module.get_mongo_client()



def test_get_mongo_client_configuration():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017"
    app.config["MONGO_SERVER_SELECTION_TIMEOUT_MS"] = 3000
    app.config["MONGO_CONNECT_TIMEOUT_MS"] = 4000
    app.config["MONGO_SOCKET_TIMEOUT_MS"] = 5000
    app.config["MONGO_MAX_IDLE_TIME_MS"] = 60000
    app.config["MONGO_RETRY_WRITES"] = True

    with patch("certificados.db.MongoClient") as mock_client_cls:
        mock_instance = MagicMock()
        mock_client_cls.return_value = mock_instance

        with app.app_context():
            client = db_module.get_mongo_client()
            assert client == mock_instance
            mock_client_cls.assert_called_once_with(
                "mongodb://localhost:27017",
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=4000,
                socketTimeoutMS=5000,
                maxIdleTimeMS=60000,
                retryWrites=True,
            )

            # Second call should reuse existing instance without calling MongoClient constructor again
            second_client = db_module.get_mongo_client()
            assert second_client == mock_instance
            assert mock_client_cls.call_count == 1


def test_get_db():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017"
    app.config["MONGO_DB_NAME"] = "test_custom_db"

    with patch("certificados.db.get_mongo_client") as mock_get_client:
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db
        mock_get_client.return_value = mock_client

        with app.app_context():
            db = db_module.get_db()
            mock_client.__getitem__.assert_called_once_with("test_custom_db")
            assert db == mock_db


def test_ping_db_success():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017"

    with patch("certificados.db.get_mongo_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        with app.app_context():
            is_ok, msg = db_module.ping_db()
            assert is_ok is True
            assert msg == "connected"
            mock_client.admin.command.assert_called_once_with("ping")


def test_ping_db_failure():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017"

    with patch("certificados.db.get_mongo_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.admin.command.side_effect = ConnectionFailure("Timeout connecting to Atlas")
        mock_get_client.return_value = mock_client

        with app.app_context():
            is_ok, msg = db_module.ping_db()
            assert is_ok is False
            assert "Timeout connecting to Atlas" in msg
