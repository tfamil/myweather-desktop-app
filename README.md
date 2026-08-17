# MyWeather Desktop App

A Python weather application with a command-line location manager and a Tkinter desktop interface for viewing live current-weather data from OpenWeather.

## Highlights

- Manage saved cities from a CLI: add, list, search, view, and delete locations.
- Resolve city names to latitude/longitude with the OpenWeather Geocoding API.
- Display live weather in a Tkinter desktop GUI.
- Show temperature, feels-like temperature, humidity, wind speed/direction, sunrise, sunset, and condition icons.
- Navigate between saved locations without restarting the application.
- Cache fetched weather responses in memory for the current GUI session.
- Persist saved locations locally as JSON.

## Tech Stack

- Python 3
- Tkinter
- OpenWeather Geocoding API
- OpenWeather Current Weather API
- JSON
- `urllib`
- Pillow / `PIL`

## Project Structure

```text
.
├── admin.py          # CLI location manager
├── weather.py        # Tkinter weather GUI
├── images/           # OpenWeather condition icons
├── pseudocode.pdf    # Design/pseudocode document
├── .gitignore
└── README.md
```

## How It Works

### 1. Location administration

`admin.py` searches OpenWeather's geocoding service and stores the selected location with its name, country, optional state, latitude, and longitude.

Saved locations are written to:

```text
locations.txt
```

The file is intentionally ignored by Git because it is local application data.

### 2. Weather display

`weather.py` loads the saved locations and fetches current conditions using their coordinates. The Tkinter interface then presents the weather and lets the user move through saved locations with previous/next controls.

## Setup

### Prerequisites

- Python 3.10+
- Tkinter
- Pillow
- An OpenWeather API key

Install Pillow:

```bash
python -m pip install Pillow
```

### API key

Before publishing or running the project, replace the hard-coded key approach with an environment variable.

Recommended pattern:

```python
import os

API_KEY = os.environ["OPENWEATHER_API_KEY"]
```

Then set the variable before starting the programs.

**Windows PowerShell**

```powershell
$env:OPENWEATHER_API_KEY="your_api_key"
```

**macOS / Linux**

```bash
export OPENWEATHER_API_KEY="your_api_key"
```

## Run

Manage locations first:

```bash
python admin.py
```

Then launch the GUI:

```bash
python weather.py
```

## Engineering Notes

The project separates administration from presentation: the CLI owns location management, while the GUI focuses on retrieving and displaying weather. Utility functions handle location formatting, wind-direction conversion, and timezone-aware sunrise/sunset formatting.

## What I Practised

- Third-party REST API integration
- JSON parsing
- URL encoding and HTTP requests
- Local persistence
- Desktop GUI development
- Input validation
- Timezone-aware date/time formatting
- Breaking application logic into reusable functions

## Before Publishing

- Rotate the OpenWeather API key currently present in the source and remove it from Git history.
- Load the API key from an environment variable.
- Do not commit `.venv/`.
- Keep `locations.txt` ignored.
- Update the name/student-number placeholders if the assignment version is being retained.
