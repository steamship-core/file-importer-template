"""Example Steamship Importer Plugin.

An Importer is responsible for fetching data for import into the Steamship platform.
"""

import os

from steamship.app import App, Response, post, create_handler
from steamship.base.error import SteamshipError
from steamship.plugin.file_importer import FileImporter
from steamship.plugin.inputs.file_import_plugin_input import FileImportPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.service import PluginRequest

from src.utils import create_text_response, create_markdown_response


def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()


class FileImporterPlugin(FileImporter, App):
    """"Example Steamship File Importer plugin."""

    def run(self, request: PluginRequest[FileImportPluginInput]) -> Response[RawDataPluginOutput]:
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
        elif request.data.url.endswith(".mkd"):
            response = create_text_response(data)
        else:
            response = RawDataPluginOutput(string=data, mime_type=None)

        # All plugin responses must be wrapped in the PluginResponse object.
        return Response(data=response)

    @post('/import_file')
    def import_file(self, **kwargs) -> Response[RawDataPluginOutput]:
        """HTTP endpoint for our plugin.

        When deployed and instantiated in a Space, this endpoint will be served at:

        https://{username}.steamship.run/{space_id}/{plugin_instance_id}/import_file

        When adapting this template, you can almost always leave the below code unchanged.
        """
        request = FileImporter.parse_request(request=kwargs)
        return self.run(request)


handler = create_handler(FileImporterPlugin)
