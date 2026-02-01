# Automated Exam Room & Faculty Duty Allocation System

## Technology Stack
- Frontend: HTML + CSS
- Backend: Python (Flask)
- Database: Not required (file-based Excel processing)

## Features
- Upload Excel files for classroom, exam timetable, and faculty timetable
- Automated allocation of students to classrooms
- Automated allocation of faculty to exam duties
- Downloadable result Excel

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Backend Setup
1. Navigate to `backend/` directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. No database setup is required. The system reads input Excel files and generates output Excel files.

4. Run the Flask app:
   ```bash
   python app.py
   ```
   
   The server will start at `http://localhost:5000`

### Frontend
1. Once the backend is running, open your browser and navigate to:
   ```
   http://localhost:5000
   ```
   
   Or alternatively, open `frontend/index.html` directly in your browser (ensure backend is running at `http://localhost:5000`).

## Quick Start Commands

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open `http://localhost:5000` in your browser.

## Usage
1. Use Phase 1 form to upload classroom Excel, number of students, and starting USN.
2. Use Phase 2 form to upload classroom allocation, exam timetable, and faculty timetable Excels.
3. Download the result Excel after allocation. 