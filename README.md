# Steamship File Importer Plugin Template

This project contains a File Importer Plugin Template that you can customize and deploy.

In Steamship, **File Importers** make it easy to import data into the Steamship Engine. For example, you might create a 

* **Notion Importer** to import Notion pages given a Page ID
* **Wikipedia Importer** to import Wikipedia content given a Wikipedia URL
* **YouTube Importer** to import the audio-track of a video given a YouTube URL

## Getting Started

The best way to use this template is with the Steamship CLI:

1. Install the Steamship CLI: `npm install -g @steamship.cli`
2. Create a new Steamship Project: `ship create`
3. Choose the **Plugin** project type
4. Choose the **File Importer** plugin type
5. Select a name for your project, such as `notion-file-importer`

A copy of this repository will downloaded and configured for you.

## Developer Setup

Before you do anything else, we recommend setting up a Python virtual environment.
This will ensure that your plugin:

* Only uses Python modules from the requirements.txt file (which is important at deployment time!)
* Can be easily shared between developers (who may have differing Python environments)

To set up a virtual environment:

1. Create a new environment with: `python3 -m venv .venv`
2. Activate that environment: `source .venv/bin/activate`
3. Install the project's development dependencies: `python -m pip install -r requirements.dev.txt`
4. Install the project's runtime dependencies: `python -m pip install -r requirements.txt`

Any subsequent time you want to develop on the project, start by re-activating the virtual environment:

```
source .venv/bin/activate
```

Any time you need to add a new Python package to your plugin:

1. Add it to the `requirements.txt` file, making sure to specify the version number.
2. Install the package by re-installing the requirements file: `python -m pip install -r requirements.txt`

This process will ensure you never accidentally use a package available on your local machine that is not present in the plugin's runtime environment on Steamship.
## Developing

All the code for this plugin is located in the `src/api.py` file:

* The `FileImporterPlugin` class
* The `run` method that will be invoked when file import has been requested

This project template includes a mock plugin that you can adapt (or delete) as you build your own. For am example of a completed non-trivial File Importer Plugin that does non-trivial work, take a look at the (Wikipedia File Importer)[https://github.com/steamship-plugins/wikipedia-file-importer]

### What is a File Importer

The core purpose of a file importer is to fetch data from somewhere on the internet and return it to Steamship as `(bytes, mime_type)`. This is done by implementing the following
method on your plugin:

```
    def run(self, request: PluginRequest[FileImportPluginInput]) -> Response[RawDataPluginOutput]:
```

Typically, File Importer Plugins are designed to expect some document identifier at `request.data.url`, such  as:

- A Wikipedia URL
- A Notion page URL
- An S3 address

The File Importer Plugin might also use configuration provided to its constructor, such as an API key to allow it to call the Notion or S3 APIs.
It is up to the plugin author to define what this configuration needs to be.

## Testing

Tests are located in the `test/test_api.py` file. You can run them with:

```bash
pytest
```

We have provided sample data in the `test_data/` folder.

## Deploying

Deploy your converter to Steamship by running:

```bash
ship deploy --register-plugin
```

That will deploy your app to Steamship and register it as a plugin for use.

## Using

Once deployed, your File Importer Plugin can be referenced by the handle in your `steamship.json` file.

```python
import mimetypes
from steamship import Steamship, File

MY_PLUGIN_HANDLE = ".. fill this out .."

client = Steamship()

file_url = "./test_data/king_speech.txt"
mime_type, _ = mimetypes.guess_type(file_url)

importer = client.use_plugin(plugin_handle=MY_PLUGIN_HANDLE, config={})
import_task = File.create_with_plugin(client, plugin_instance=importer.handle, url=file_url, mime_type=mime_type)
import_task.wait()

steamship_file = import_task.output
```

## Sharing

Please share what you've built with hello@steamship.com! 

We would love take a look, hear your suggestions, help where we can, and share what you've made with the community.