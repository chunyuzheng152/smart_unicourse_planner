import sys
import threading
from pathlib import Path

import pytest
from werkzeug.serving import make_server

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def live_server():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    server = make_server("127.0.0.1", 0, flask_app)
    port = server.server_port

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join()