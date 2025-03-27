# Local Events and Activity API

## Project Overview
A comprehensive API for discovering free and low-cost local events, designed to help students and community members find exciting activities.

## Features
-  Multi-source event scraping
-  Advanced event filtering
-  Persistent database storage
-  FastAPI-powered backend

## Prerequisites
- Python 3.9+
- pip
- virtualenv

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/local-events-api.git
cd local-events-api
```

### 2. Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate
# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Initialization
```bash
python -c "from database.models import init_db; init_db()"
```

### 5. Run the Application
```bash
# Start the scraper
python -m scraper.event_scraper

# Run the API server
uvicorn main:app --reload
```

## Running Tests
```bash
pytest tests/
```

## API Endpoints
- `GET /events`: Search events with multiple filters
- `GET /events/{event_id}`: Get specific event details



## Disclaimer
 Always respect website terms of service when scraping the project is not complete as data privacy policies of the websites doesnt allow  us to access the data.
