import os

import pytest
from pytest_mock import mocker
from sqlalchemy.exc import ProgrammingError, OperationalError

import webapp
from webapp.db import session
from webapp.models import AudioFile
from webapp.plot import Plot


@pytest.fixture
def app():
    return webapp.create_app()


@pytest.fixture
def client(app):
    return app.test_client()


def test_homepage(client):
    res = client.get('/')
    assert res.status_code == 200


#
# Test Plot.get_files() method
#
def test_with_not_inizialized_db(client, mocker):
    def raise_exception():
        raise ProgrammingError()

    mocker.patch.object(Plot, 'get_files').side_effect = raise_exception

    res = client.get('/')
    assert res.status_code == 500


def test_with_empty_db(client, mocker):
    mocker.patch.object(Plot, 'get_files')
    Plot.get_files.return_value = []
    res = Plot().get_files()
    assert res == []

    res = client.get('/')
    assert res.status_code == 200
    assert 'no file available' in str(res.data).lower()


def test_with_db_connection_error(client, mocker):
    def raise_exception():
        raise OperationalError()

    mocker.patch.object(Plot, 'get_files').side_effect = raise_exception

    res = client.get('/')
    assert res.status_code == 500


def test_with_wav_file_zero_byte(client, mocker):
    def plot_get_files_with_zero_wav():
        rows = session.query(AudioFile.audio_path).all()
        files = [os.path.basename(file.audio_path) for file in rows]
        files.append('ch-zero.wav')
        return files

    mocker.patch.object(Plot, 'get_files')
    Plot.get_files.return_value = plot_get_files_with_zero_wav()
    files = Plot().get_files()
    assert 'ch-zero.wav' in files

    res = client.get('/')
    assert res.status_code == 200
    assert 'ch-zero.wav - invalid file' in str(res.data).lower()


def test_with_wav_file_invalid_format(client, mocker):
    def plot_get_files_with_zero_wav():
        rows = session.query(AudioFile.audio_path).all()
        files = [os.path.basename(file.audio_path) for file in rows]
        files.append('ch-invalid.wav')
        return files

    mocker.patch.object(Plot, 'get_files')
    Plot.get_files.return_value = plot_get_files_with_zero_wav()
    files = Plot().get_files()
    assert 'ch-invalid.wav' in files

    res = client.get('/')
    assert res.status_code == 200
    assert 'ch-invalid.wav - invalid file' in str(res.data).lower()


def test_with_wav_file_with_empty_peaks_list(client, mocker):
    mocker.patch.object(Plot, 'get_peaks')
    Plot.get_peaks.return_value = []
    peaks = Plot().get_peaks()
    assert peaks == []

    res = client.get('/')
    assert res.status_code == 200
    assert 'peaks missing' in str(res.data).lower()


def test_with_wav_file_with_none_peaks(client, mocker):
    mocker.patch.object(Plot, 'get_peaks')
    Plot.get_peaks.return_value = None
    peaks = Plot().get_peaks()
    assert peaks is None

    res = client.get('/')
    assert res.status_code == 200
    assert 'peaks missing' in str(res.data).lower()

