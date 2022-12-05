"""Example Steamship Importer Plugin.

An Importer is responsible for fetching data for import into the Steamship platform.
"""

import os
from typing import Type

from steamship.base.error import SteamshipError
from steamship.invocable import InvocableResponse, create_handler, Config
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.request import PluginRequest

from utils import create_text_response, create_markdown_response


def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()


class FileImporterPluginConfig(Config):
    """Configures the FileImporterPlugin.

    This configuration **requires** an `apiKey` be supplied to create a plugin instance.
    """
    apiKey: str


class FileImporterPlugin(FileImporter):
    """Example Steamship File Importer plugin."""

    config: FileImporterPluginConfig

    def config_cls(self) -> Type[Config]:
        return FileImporterPluginConfig

    def run(self, request: PluginRequest[FileImportPluginInput]) -> InvocableResponse[RawDataPluginOutput]:
        """Performs the file import or returns a detailed error explaining what went wrong."""

        # Check to make sure the user provided a URL to identify what it is they want imported.
        if request.data.url is None:
            raise SteamshipError(message=f"Missing the `url` field in your FileImport request. Got request: {request}")

        # In this template, we simply return the contents of the file in the `test_data` folder named `url`
        try:
            data = _read_test_file(request.data.url)
        except Exception as error:
            raise SteamshipError(message="There was an error reading that file from disk.", error=error)

        # FileImporter plugins should return a File.CreateResponse object. For example of preparing this object,
        # see the `utils.py` file in this project. The response can be raw bytes, raw bytes with a MIME Type,
        # or parsed Steamship Block format.
        if request.data.url.endswith(".mkd"):
            response = create_markdown_response(data)
        else:
            response = RawDataPluginOutput(string=data, mime_type=None)

        # All plugin responses must be wrapped in the PluginResponse object.
        return InvocableResponse(data=response)


