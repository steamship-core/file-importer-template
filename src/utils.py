import io

from steamship import DocTag, TagKind
from steamship.data.file import File
from steamship.data.block import Block
from steamship.data.tags.tag import Tag
from steamship.base import MimeTypes

def create_text_response(plain_text: str) -> File.CreateResponse:
    """Example of creating a response that is merely text.

    Use the `string` kwarg in the File.CreateResponse constructor, along with the TXT MIME Type.
    """
    return File.CreateResponse(string=plain_text, mimeType=MimeTypes.TXT)

def create_image_response(png_image: bytes) -> File.CreateResponse:
    """Example of creating a response containing an image.

    Use the `bytes` kwarg in the File.CreateResponse constructor, along with the appropriate MIME Type.
    """
    return File.CreateResponse(bytes=io.BytesIO(png_image), mimeType=MimeTypes.PNG)

def create_markdown_response(markdown_text: str) -> File.CreateResponse:
    """Example of creating a response that is merely text.

    Use the `string` kwarg in the File.CreateResponse constructor, along with the MKD MIME Type.
    """
    return File.CreateResponse(string=markdown_text, mimeType=MimeTypes.MKD)


def create_block_response() -> File.CreateResponse:
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
                    Tag.CreateRequest(kind=TagKind.doc, name=DocTag.h1)
                ]
            ),
            Block.CreateRequest(
                text="This is the first paragraph. It has a link.",
                tags=[
                    Tag.CreateRequest(kind=TagKind.doc, name=DocTag.paragraph),
                    Tag.CreateRequest(
                        kind=TagKind.doc,
                        name="link", # You can use a custom name
                        value={"href": "https://example.org"}, # Value is always a dict if present
                        startIdx=35, # Start-inclusive (python slice semantics)
                        endIdx=41 # End-exclusive (python slice semantics)
                    )
                ]
            )
        ]
    )

    return File.CreateResponse(json=file, mimeType="steamship/block") # Todo: We'll add this mime type
