"""Example Steamship Importer Plugin.

An Importer is responsible for fetching data for import into the Steamship platform.
"""

from steamship import Block, BlockTypes, MimeTypes, SteamshipError
from steamship.app import App, post, create_handler, Response
from steamship.plugin.file_importer import FileImporter
from steamship.data.file import FileImportResponse, FileImportRequest
from steamship.plugin.service import PluginResponse, PluginRequest
import os


def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()


class FileImporterPlugin(FileImporter, App):
    """"Example Steamship File Importer plugin."""

    def run(self, request: PluginRequest[FileImportRequest]) -> PluginResponse[FileImportResponse]:
        """Every plugin implements a `run` function.

        This template plugin does an extremely simple import in which:
            - The request is expected to contain an example filename (in the `url` field)
            - The result is the contents of that file read from the `test_data` folder.
        """

        if request.data.url is None:
            return Response(error=SteamshipError(
                message="Set the `url` field to the file name you would like to import."
            ))

        try:
            data = _read_test_file(request.data.url)
        except Exception as error:
            return Response(error=SteamshipError(
                message="There was an error reading that file from disk.",
                error=error
            ))

        mimeType = None
        if request.data.url.endswith(".txt"):
            mimeType = MimeTypes.TXT
        elif request.data.url.endswith(".mkd"):
            mimeType = MimeTypes.MKD
        else:
            mimeType = request.data.defaultMimeType

        return PluginResponse(data=FileImportResponse(data=data, mimeType=mimeType))

    # Note: the path can diverge from the method name, as below.
    @post('/import_file')
    def import_file(self, **kwargs) -> Response:
        """App endpoint for our plugin.

        The `run` method above implements the Plugin interface for a File Importer.
        This `/import_file` method exposes it over an HTTP endpoint as a Steamship App.

        When developing your own plugin, you can almost always leave the below code unchanged.
        """
        request = FileImporter.parse_request(request=kwargs)
        response = self.run(request)
        dict_response = FileImporter.response_to_dict(response)
        return Response(json=dict_response)


handler = create_handler(FileImporterPlugin)
