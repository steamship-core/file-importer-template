# Steamship File Importer Plugin Template

This project contains a File Importer Plugin Template that you can customize and deploy.

In Steamship, **File Importers** make it easy to import data into the Steamship Engine. For example, you might create a 

* **Notion Importer** to import Notion pages given a Page ID
* **Wikipedia Importer** to import Wikipedia content given a Wikipedia URL
* **YouTube Importer** to import the audio-track of a video given a YouTube URL

## Getting Started

The best way to use this template is with the Steamship CLI

1. Install the Steamship CLI: `npm install -g @steamship.cli`
2. Create a new Steamship Project: `ship create`
3. Choose the **Plugin** project type
4. Choose the **File Importer** plugin type

A copy of this repository will cloned and configured for you.

## Developer Setup

We recommend using a Python virtual environments for development.
To set one up, run the following command from this directory:

**Your first time**, create the virtual environment with:

```bash
python3 -m venv .venv
```

**Each time**, activate your virtual environment with:

```bash
source .venv/bin/activate
```

**Your first time**, install the required dependencies with:

```bash
python -m pip install -r requirements.dev.txt
python -m pip install -r requirements.txt
```

## Developing

All the code for this plugin is located in the `src/api.py` file:

* The `FileImporterPlugin` class
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