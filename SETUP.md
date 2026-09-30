# Quick Tym - Setup Instructions

## Prerequisites

- Python 3.10+
- Node.js 18+
- pip and npm

## Quick Start

### 1. Backend Setup

\\\ash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_imports.py

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\\\

Backend API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health

### 2. Frontend Setup

\\\ash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
\\\

Frontend: http://localhost:5173

## MVP Features

### Backend API Endpoints

**Authentication:**
- \POST /api/v1/auth/register\ - Register new user
- \POST /api/v1/auth/login\ - Login user

**Products:**
- \GET /api/v1/products\ - List all products
- \GET /api/v1/products/{product_id}\ - Get product details

**Other endpoints:** Placeholder endpoints for rentals, deliveries, payments, admin, and AI features

### Database

- SQLite database automatically created at \database/quicktym.db\
- Tables: users, products, categories, inventory, rental_sessions, bookings

## Project Structure

\\\
QuickTym/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── routers/        # API route handlers
│   │   ├── api/v1/         # API versioning
│   │   │   ├── routes/     # Route implementations
│   │   │   └── schemas/    # Pydantic schemas
│   │   ├── core/           # Core utilities
│   │   │   ├── config.py   # Configuration
│   │   │   ├── security.py # Password hashing
│   │   │   └── jwt.py      # JWT token handling
│   │   ├── db/             # Database setup
│   │   └── services/       # Business logic (future)
│   ├── requirements.txt    # Python dependencies
│   └── test_imports.py     # Import test script
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API clients
│   │   ├── contexts/       # React contexts
│   │   ├── styles/         # Theme & styles
│   │   └── App.tsx         # Main component
│   └── package.json        # Node dependencies
├── database/               # SQLite database (created at runtime)
└── README.md               # Project documentation
\\\

## Testing

### Backend
\\\ash
cd backend
pytest tests/ -v
\\\

### Frontend
\\\ash
cd frontend
npm test
\\\

## Environment Variables

Create \.env\ files in backend/ and frontend/ using the \.env.example\ templates.

## Database

The SQLite database is automatically created when the backend starts. No manual migration setup required for MVP.

## Troubleshooting

**ModuleNotFoundError:**
- Run \pip install -r requirements.txt\ in backend folder

**Port already in use:**
- Backend: Change port with \--port 8001\
- Frontend: Vite will automatically use next available port

**CORS errors:**
- Frontend CORS is configured in \ackend/app/main.py\
- Allowed origins: http://localhost:5173

## Next Steps

1. Start backend: \uvicorn app.main:app --reload\
2. Start frontend: \
pm run dev\
3. Access UI at http://localhost:5173
4. API documentation at http://127.0.0.1:8000/docs
