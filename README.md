# website_flightfrd
A website for aviation lovers

## Project Structure
```
website_flightfrd/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── run_server.py          # Server startup script
│   ├── requirements.txt       # Python dependencies
│   ├── instance/              # Database directory
│   │   └── aviation.db        # SQLite database
│   ├── models/                # Data models
│   ├── routes/                # API routes
│   ├── utils/                 # Utility functions
│   └── config/                # Configuration files
├── frontend/
│   ├── src/
│   │   └── templates/         # HTML templates
│   ├── public/                # Static assets
│   ├── components/            # Frontend components
│   └── styles/                # CSS stylesheets
└── data/                      # Data files
```

## Getting Started

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend/
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python run_server.py
```

### Frontend
Frontend files are located in the `frontend/` directory.

## Features
- ADS-B Tracker
- ATC Streams
- Appointments Calendar
- Special Flights
