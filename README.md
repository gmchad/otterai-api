# otterai-api

Unofficial Python API for [otter.ai](http://otter.ai)

## Contents

-   [Installation](#installation)
-   [Setup](#setup)
-   [APIs](#apis)
    -   [User](#user)
    -   [Speeches](#speeches)
    -   [Speakers](#speakers)
    -   [Folders](#folders)
    -   [Groups](#groups)
    -   [Notifications](#notifications)
-   [Exceptions](#exceptions)

## Installation

`pip install .`

or in a virtual environment

```bash
python3 -m venv env
source env/bin/activate
pip install .
```

## Setup

```python
from otterai import OtterAI
otter = OtterAI()
otter.login('USERNAME', 'PASSWORD')
```

## APIs

### User

Get user specific data

```python
otter.get_user()
```

### Speeches

Get all speeches

**optional parameters**: folder, page_size, source

```python
otter.get_speeches()
```

Get speech by id

```python
otter.get_speech(SPEECH_ID)
```

Query a speech

```python
otter.query_speech(QUERY, SPEECH_ID)
```

Upload a speech

**optional parameters**: content_type (default audio/mp4)

```python
otter.upload_speech(FILE_NAME)
```

Download a speech

**optional parameters**: filename (defualt id), format (default: all available (txt,pdf,mp3,docx,srt) as zip file)

```python
otter.download_speech(SPEECH_ID, FILE_NAME)
```

Move a speech to trash

```python
otter.move_to_trash_bin(SPEECH_ID)
```

#### TODO

Start a live speech

### Speakers

Get all speakers

```python
otter.get_speakers()
```

Create a speaker

```python
otter.create_speaker(SPEAKER_NAME)
```

#### TODO

Assign a speaker to speech transcript

### Folders

Get all folders

```python
otter.get_folders()
```

### Groups

Get all groups

```python
otter.list_groups()
```

### Notifications

Get notification settings

```python
otter.get_notification_settings()
```

## Exceptions

```python
from otterai import OtterAIException

try:
 ...
except OtterAIException as e:
 ...
```
