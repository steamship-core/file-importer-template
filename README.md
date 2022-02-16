# Steamship File Importer Plugin

This project implements a basic Steamship File Importer that you can customize and deploy for your own use.

In Steamship, **File Importers** are responsible for importing data into the Steamship platform.

This sample project simply imports data from a pre-loaded set of text files, but other file importers might:

* Import a Notion page
* Extract the text from a Wikipedia page
* Fetch the audio track from a video online

Once a File Importer has returned the data's raw bytes and Mime Type to Steamship, a **Converter Plugin** can be used to transform it into Steamship Block Format.

## First Time Setup

We recommend using Python virtual environments for development.
To set one up, run the following command from this directory:

```bash
python3 -m venv .venv
```

Activate your virtual environment by running:

```bash
source .venv/bin/activate
```

Your first time, install the required dependencies with:

```bash
python -m pip install -r requirements.dev.txt
python -m pip install -r requirements.txt
```

## Developing

All the code for this plugin is located in the `src/api.py` file:

* The FileImporterPlugin class
* The `/import_file` endpoint

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
from steamship import Steamship, ImportRequest

MY_PLUGIN_HANDLE = ".. fill this out .."

client = Steamship()
request = ImportRequest() # Provide the appropriate parameters
file = client.create_file(importer=MY_PLUGIN_HANDLE, request=request)
```

## Sharing

Plesae share what you've built with hello@steamship.com! 

We would love take a look, hear your suggestions, help where we can, and share what you've made with the community.