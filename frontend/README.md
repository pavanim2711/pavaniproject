# Quick Tym Frontend

React + Vite + TypeScript application for the Quick Tym rental platform.

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js (v18 or higher) - [Download here](https://nodejs.org/)
- npm (comes with Node.js)

## Installation

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

## Development

```bash
# Start the development server on localhost:5173
npm run dev

# Build for production
npm run build

# Preview the production build
npm run preview

# Run ESLint
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Page-level components
│   ├── hooks/          # Custom React hooks
│   ├── contexts/       # React contexts (Auth, etc.)
│   ├── services/       # API service clients
│   ├── utils/          # Utility functions
│   ├── styles/         # Global styles & themes
│   ├── App.tsx         # Main app component
│   ├── main.tsx        # Entry point
│   └── vite-env.d.ts   # Vite type declarations
├── public/             # Static assets
├── index.html          # HTML template
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Available Routes

- `/` - Homepage
- `/products/:id` - Product details
- `/login` - User login
- `/register` - User registration

## Development Server

The development server runs on `localhost:5173` and includes:
- Hot Module Replacement (HMR)
- TypeScript support
- Proxy configuration for backend API (`/api` → `http://localhost:8000/api/v1`)

## Build

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Type Checking

TypeScript is configured with strict mode enabled for better type safety.

## Linting

```bash
npm run lint
```

## Environment Variables

Create a `.env` file in the frontend directory if needed:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Integration with Backend

The frontend is configured to proxy API requests to the backend:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

All `/api` requests will be proxied to the backend server.
