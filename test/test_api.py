import base64
import os

import pytest
from pydantic import ValidationError
from steamship import MimeTypes
from steamship.base.tasks import TaskState
from steamship.invocable import InvocableResponse
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.request import PluginRequest

from src.api import FileImporterPlugin

__copyright__ = "Steamship"
__license__ = "MIT"


def _base64_decode(base64_message: str) -> str:
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf8')


def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()


def _test_file(filename: str, expect_mime: str):
    importer = FileImporterPlugin(config={"apiKey": "foo"})

    file = _read_test_file(filename)

    request = PluginRequest(data=FileImportPluginInput(url=filename))
    response = importer.run(request)

    # Check that the response types are correct
    assert (response is not None)
    assert (type(response) == InvocableResponse)

    # Check that there is no error
    assert (response.status is not None)
    assert (response.status.state != TaskState.failed)

    # Check the specific response object
    assert (response.data is not None)
    assert (type(response.data) == RawDataPluginOutput)
    assert (response.data.mime_type == expect_mime)
    assert (_base64_decode(response.data.data) == file)


def test_importer():
    _test_file('roses.mkd', MimeTypes.MKD)
    _test_file('king_speech.txt', MimeTypes.TXT)


def test_fails_without_config():
    with pytest.raises(ValidationError):
        FileImporterPlugin()


def test_fails_with_config_but_wrong_content():
    with pytest.raises(ValidationError):
        FileImporterPlugin(config={"unnecessary": "key"})


def test_fails_with_empty_api_key():
    with pytest.raises(ValidationError):
        FileImporterPlugin(config={"apiKey": ""})
