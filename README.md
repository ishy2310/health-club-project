# Health & Fitness Club Management System

## Setup (run this to get the same dependencies)

1. Clone the repo
2. Create virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Create PostgreSQL database:
   `createdb fitness_db` (or via pgAdmin)
5. Copy `.env.example` to `.env` and set your local DB credentials
6. Run the app:
   `python app/main.py`

## Project Structure
/models  → SQLAlchemy entity classes
/app     → CLI + business logic
/docs    → ERD.pdf