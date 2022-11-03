import io

from steamship import Block, DocTag, Tag, File, MimeTypes
from steamship.data import TagKind
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput


def create_text_response(plain_text: str) -> RawDataPluginOutput:
    """Example of creating a response that is merely text.

    Use the `string` kwarg in the File.CreateResponse constructor, along with the TXT MIME Type.
    """
    return RawDataPluginOutput(string=plain_text, mime_type=MimeTypes.TXT)


def create_image_response(png_image: bytes) -> RawDataPluginOutput:
    """Example of creating a response containing an image.

    Use the `bytes` kwarg in the File.CreateResponse constructor, along with the appropriate MIME Type.
    """
    return RawDataPluginOutput(bytes=io.BytesIO(png_image), mime_type=MimeTypes.PNG)


def create_markdown_response(markdown_text: str) -> RawDataPluginOutput:
    """Example of creating a response that is merely text.

    Use the `string` kwarg in the File.CreateResponse constructor, along with the MKD MIME Type.
    """
    return RawDataPluginOutput(string=markdown_text, mime_type=MimeTypes.MKD)


def create_block_response() -> RawDataPluginOutput:
    """Example of creating a response using Steamship's internal Block format.

    Block format is merely the JSON serialization of the Steamship File object. This is the ideal response
    type when the FileImporter you are creating has access not just to the raw bytes you are importing, but also
    knowledge of its structure.

    For example, a Notion Page importer could create:

    * A tag for each paragraph
    * A tag for each link
    * A tag for headers

    And so on.
    """
    file = File.CreateRequest(
        blocks=[
            Block.CreateRequest(
                text="This is the header",
                tags=[
                    # If no startIdx and endIdx are specified, the implication is 0, -1 (python slice semantics)
                    Tag.CreateRequest(kind=TagKind.DOCUMENT, name=DocTag.H1)
                ]
            ),
            Block.CreateRequest(
                text="This is the first paragraph. It has a link.",
                tags=[
                    Tag.CreateRequest(kind=TagKind.DOCUMENT, name=DocTag.PARAGRAPH),
                    Tag.CreateRequest(
                        kind=TagKind.DOCUMENT,
                        name="link",  # You can use a custom name
                        value={"href": "https://example.org"},  # Value is always a dict if present
                        startIdx=35,  # Start-inclusive (python slice semantics)
                        endIdx=41  # End-exclusive (python slice semantics)
                    )
                ]
            )
        ]
    )

    return RawDataPluginOutput(json=file, mime_type=MimeTypes.STEAMSHIP_BLOCK_JSON)
