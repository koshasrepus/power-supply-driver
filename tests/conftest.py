from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from config import config
from main import app, dispatcher


@pytest.fixture(scope='session')
def http_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope='function')
def test_dispatcher():
    return dispatcher


@pytest.fixture(scope='function')
def create_telemetry_file():
    def _write_telemetry_data(telemetry_data):
        with open(config.telemetry_export_file, 'w') as f:
            f.writelines(telemetry_data)

    yield _write_telemetry_data
    telemetry_file = Path(config.telemetry_export_file)
    telemetry_file.unlink()
