# Quick Tym - AI-Powered Rental Platform

"Rent it. Use it. Return it."

Quick Tym is an AI-powered rental web application for indoor and outdoor products with time-based billing. The system enables customers to rent products only for the time they need, with intelligent features for recommendations, demand prediction, and optimized delivery routing.

## Features

- **Time-Based Rental System**: Pay only for actual usage time with 1-second precision
- **AI Recommendations**: Personalized product suggestions based on rental history
- **Demand Prediction**: Inventory optimization with 7-day forecasts
- **Smart Delivery Routing**: Optimized delivery assignments for partners
- **Multi-Role Access**: Customer, Delivery Partner, and Admin roles
- **Responsive UI**: Mobile-first design with touch-optimized controls

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python
- **Database**: SQLite + SQLAlchemy
- **AI Services**: Rule-based recommendation and prediction models
- **Deployment**: Ready for cloud deployment (AWS, GCP, Azure)

## Project Structure

```
QuickTym/
├── frontend/          # React + TypeScript frontend application
├── backend/           # FastAPI Python backend
│   └── tests/         # Backend test suite
├── api/              # API specifications and collections
├── database/         # SQLite database files
└── .kiro/            # Project specs and configuration
```

## Getting Started

### Prerequisites

- Node.js 18+ (with npm)
- Python 3.10+ (with pip)
- SQLite3

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd QuickTym
```

#### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Run seed script for sample data
python scripts/seed_data.py

# Start development server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at `http://127.0.0.1:8000` with:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

#### 3. Set Up Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Development

### Running Tests

#### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

#### Frontend Tests

```bash
cd frontend
npm test
```

### Build for Production

#### Backend

```bash
cd backend
# Install production dependencies
pip install -r requirements.txt

# Run with production-grade server (e.g., gunicorn)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend

```bash
cd frontend
npm run build
```

## Environment Variables

See `.env.example` files in root, `backend/`, and `frontend/` directories for configurable options.

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
