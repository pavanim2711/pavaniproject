# Quick Tym Technical Design Document

## Overview

Quick Tym is an AI-powered rental web application with the tagline "Rent it. Use it. Return it." This document outlines the comprehensive technical design for implementing a full-stack rental system with time-based billing, intelligent product recommendations, demand prediction, and optimized delivery workflows.

### Purpose

This technical design document serves as the blueprint for implementing Quick Tym, covering system architecture, component design, data models, API specifications, AI features, and operational considerations. The system is designed for local development deployment with a clear path to production scalability.

### Scope

The design covers the following functional areas:
- User management and authentication with role-based access control
- Product catalog management with inventory tracking
- Time-based rental session management with precise billing
- Delivery logistics with partner assignment and route optimization
- Payment processing with mock gateway for MVP
- AI-powered recommendations, demand prediction, and rental assistant

## Architecture

### High-Level Architecture

Quick Tym follows a clean, separated full-stack architecture with distinct layers for frontend, backend, API, and database components.

### Core Design Principles

1. **User-Centric Experience**: Prioritize intuitive interfaces, responsive design (320px-1920px), touch-optimized mobile interfaces, and seamless rental workflows across all user roles (Customer, Delivery_Partner, Admin) with WCAG compliance and contrast ratios >4.5:1.

2. **AI-Driven Intelligence**: Implement rule-based AI systems for MVP with extensible architecture for future ML integration, focusing on personalization (affinity scores 0-100), optimization (route accuracy within 15 minutes), prediction (confidence intervals), and assistance (response time bounds: 5s initial, 3s follow-up).

3. **Time-Based Precision**: Design accurate time tracking and billing systems with 1-second precision, minimum billable time unit (minutes with rounding rules), immediate timer stop on pickup request, and real-time cost visibility.

4. **Scalable Architecture**: Build with separation of concerns, modular components, and clear API boundaries to support future growth with performance targets (FCP <1.5s, LCP <2.5s, TTI <3s frontend; <200ms CRUD, <500ms complex ops backend).

5. **Data Integrity**: Ensure data consistency with SQLite indexing strategy, transactional safety with ACID compliance, audit trails for all business-critical operations, and proper data retention policies for GDPR/PDPB compliance.

6. **Brand Consistency**: Apply "Urban Tech + Rental" visual theme consistently across all interfaces with brand colors (#0F172A primary, #A3E635 accent, #2563EB secondary), accessible color schemes, and responsive typography.

7. **Security & Compliance**: Implement robust security measures including AES-256-GCM encryption for payment data, TLS 1.3, JWT with 24-hour tokens, bcrypt password hashing (work factor 12), multi-factor authentication, and quarterly security assessments.

8. **Resilience & Reliability**: Design for system availability >99.5% with circuit breaker pattern implementation, graceful degradation for critical failures, structured logging with JSON format, and comprehensive error handling.

### System Vision

Quick Tym transforms traditional rental models by introducing:
- **Pay-per-use billing**: Customers pay only for actual usage time, with rental timers stopping immediately upon pickup request
- **AI-powered discovery**: Personalized recommendations based on rental history, browsing behavior, and local trends
- **Optimized logistics**: Intelligent delivery assignment considering partner availability, proximity, and traffic patterns
- **Predictive inventory**: Demand forecasting to optimize stock levels and reduce stockouts
- **Assisted decision-making**: AI rental assistant for product suitability, timing, and pricing guidance

### Technology Stack

- **Frontend**: React 19 + Vite + TypeScript with React Router for navigation
- **Backend**: FastAPI (Python 3.10+) with SQLAlchemy ORM and Pydantic validation
- **Database**: SQLite (quick_tym.db) with SQLAlchemy for local development
- **AI Components**: Python-based rule engines for MVP with ML-ready architecture
- **Styling**: CSS-in-JS (Styled Components) with responsive design system
- **Authentication**: JWT-based authentication with role-based access control
- **Payment Processing**: Mock payment system for MVP with extensible gateway integration

### Deployment Strategy

- **Local Development**: Frontend on localhost:5173, Backend on 127.0.0.1:8000
- **Development Workflow**: Hot module replacement, auto-reload, comprehensive debugging tools
- **Environment Configuration**: Environment-specific settings (development, staging, production)
- **Testing**: Unit tests (pytest), integration tests, and end-to-end testing

### Success Metrics

#### Performance Targets
- **Frontend Performance**: 
  - First Contentful Paint (FCP): <1.5 seconds
  - Largest Contentful Paint (LCP): <2.5 seconds  
  - Time to Interactive (TTI): <3 seconds
  - Dashboard load: <2 seconds
  - Search results: <1 second
  - Mobile responsiveness: 320px to 1920px with touch-optimized interfaces

- **Backend Performance**:
  - API response times: <200ms for CRUD operations, <500ms for complex operations
  - Database queries: <100ms with proper indexing strategy
  - AI service responses: <5 seconds initial, <3 seconds follow-up queries
  - Rental assistant response: <5 seconds initial, <3 seconds for follow-up queries

- **System Reliability**:
  - System availability: >99.5% uptime
  - Data consistency: ACID compliance with SQLite transactions
  - Transaction integrity: All critical operations wrapped in transactions
  - Error rate: <1% for all API endpoints
  - Recovery time objective (RTO): <15 minutes for critical failures
  - Recovery point objective (RPO): <5 minutes data loss

#### Business Metrics
- **Customer Satisfaction**:
  - Customer rating: >4.2/5.0 average rating
  - Rental completion rate: >95% successful rentals
  - Repeat customer rate: >40% returning customers
  - Support resolution time: <2 hours for critical issues

- **Operational Efficiency**:
  - Delivery route accuracy: Within 15 minutes of estimated time
  - Inventory optimization: <10% stockout rate with demand predictions
  - Recommendation accuracy: >70% click-through rate on AI recommendations
  - Demand prediction accuracy: >80% within confidence intervals

- **Financial Metrics**:
  - Payment success rate: >90% first-time success
  - Average rental duration: 4-6 hours per rental
  - Revenue per rental: ₹500-₹2000 per transaction
  - Customer acquisition cost: <₹500 per customer

#### Quality Metrics
- **Code Quality**:
  - Test coverage: >80% unit test coverage
  - Code maintainability: <10% cyclomatic complexity
  - Security vulnerabilities: Zero high-severity vulnerabilities
  - Accessibility compliance: WCAG 2.1 AA compliance
  
- **Monitoring & Observability**:
  - Log coverage: 100% structured JSON logging
  - Metric collection: All business and performance metrics tracked
  - Alerting: Critical issues alerted within 1 minute
  - Traceability: Full request tracing with OpenTelemetry

This design document provides the architectural blueprint for implementing Quick Tym, balancing immediate MVP requirements with long-term scalability and extensibility.

## System Architecture

### High-Level Architecture

Quick Tym follows a clean, separated full-stack architecture with distinct layers for frontend, backend, API, and database components.

```mermaid
graph TB
    subgraph "Frontend Layer"
        F1[React/Vite App<br/>localhost:5173]
        F2[React Components]
        F3[React Router]
        F4[State Management]
        F5[UI Components]
    end
    
    subgraph "Backend Layer"
        B1[FastAPI Server<br/>127.0.0.1:8000]
        B2[API Routes]
        B3[Services Layer]
        B4[Models & Schemas]
        B5[AI Services]
    end
    
    subgraph "Data Layer"
        D1[SQLite Database<br/>quick_tym.db]
        D2[SQLAlchemy ORM]
        D3[Database Migrations]
    end
    
    F1 -->|HTTP REST API| B1
    B1 -->|ORM Queries| D1
    B3 -->|AI Processing| B5
    
    style F1 fill:#A3E635
    style B1 fill:#2563EB
    style D1 fill:#0F172A
```

## Components and Interfaces

### Component Hierarchy

```
QuickTym/
├── frontend/                    # React/Vite application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Page-level components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── contexts/          # React contexts for state
│   │   ├── services/          # API service clients
│   │   ├── utils/             # Utility functions
│   │   └── styles/            # Global styles & themes
│   ├── public/                # Static assets
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/               # API route definitions
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic services
│   │   ├── core/              # Core configurations
│   │   ├── dependencies/      # FastAPI dependencies
│   │   └── utils/             # Utility functions
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Backend tests
│   ├── requirements.txt
│   └── main.py
│
├── api/                       # API contract definitions
│   ├── openapi.yaml          # OpenAPI specification
│   ├── postman/              # Postman collections
│   └── examples/             # API usage examples
│
├── database/                  # Database management
│   ├── migrations/           # SQL migration scripts
│   ├── seeds/               # Seed data scripts
│   └── quick_tym.db         # SQLite database file
│
├── shared/                    # Shared utilities
│   ├── types/                # TypeScript/Python type definitions
│   └── config/               # Shared configuration
│
├── scripts/                   # Development scripts
│   ├── setup.sh              # Environment setup
│   ├── seed.py               # Database seeding
│   └── dev.sh                # Development startup
│
├── docs/                      # Documentation
├── tests/                     # End-to-end tests
├── .env.example              # Environment variables
├── docker-compose.yml        # Docker setup
├── README.md
└── .kiro/specs/quick-tym/    # Requirements & design docs
```

### Component Architecture

#### Frontend Architecture
- **Component Hierarchy**: Atomic design pattern with atoms, molecules, organisms, templates, and pages
- **State Management**: React Context + useReducer for global state, local state for component-specific data
- **Routing**: React Router 7 with nested routes, protected routes, and lazy loading
- **Styling**: CSS-in-JS with theme provider, responsive design utilities
- **API Integration**: Axios-based service layer with interceptors for auth, error handling

#### Backend Architecture
- **API Layer**: FastAPI with automatic OpenAPI documentation at `/docs` and `/redoc`
- **Service Layer**: Business logic separation with service classes for each domain
- **Data Layer**: SQLAlchemy ORM with declarative models, session management
- **Validation Layer**: Pydantic schemas for request/response validation
- **Authentication**: JWT-based auth with role-based permissions middleware

#### Database Architecture
- **Database**: SQLite for local development with migration path to PostgreSQL for production
- **Schema Design**: Normalized schema (3rd normal form) with appropriate indexes
- **Relationships**: Foreign key constraints with cascade rules for data integrity
- **Transactions**: ACID-compliant transaction management for critical operations

#### AI Services Architecture
- **Modular Design**: Separate services for recommendations, demand prediction, delivery optimization, rental assistant
- **Rule-Based MVP**: Initial implementation with rule-based logic and extensible interfaces
- **Data Pipelines**: Scheduled jobs for model training, data preprocessing, and prediction updates
- **Monitoring**: Performance tracking, accuracy metrics, and model drift detection

### Communication Patterns

#### Frontend-Backend Communication
- **REST API**: JSON-based RESTful endpoints with consistent error handling
- **WebSocket**: Real-time updates for rental timer, delivery status, notifications
- **File Uploads**: Multipart form data for delivery/pickup photo evidence

#### Service-Service Communication
- **Synchronous**: Direct service method calls within same process
- **Background Tasks**: Celery or FastAPI BackgroundTasks for async processing
- **Event-Driven**: Internal event bus for decoupled service communication

### Scalability Considerations

#### Horizontal Scaling
- **Stateless Services**: Backend services designed to be stateless for horizontal scaling
- **Load Balancing**: Reverse proxy (nginx) for distributing requests across multiple instances
- **Database Scaling**: Read replicas, connection pooling, query optimization

#### Performance Optimization
- **Caching Strategy**: Redis for session storage, API response caching, and query result caching
- **Database Indexing**: Strategic indexes on frequently queried columns and foreign keys
- **Query Optimization**: Pagination, eager loading, and selective field retrieval

#### Monitoring & Observability
- **Logging**: Structured JSON logging with context (user_id, request_id, trace_id)
- **Metrics**: Prometheus metrics for API response times, error rates, and business metrics
- **Tracing**: Distributed tracing with OpenTelemetry for request flow analysis

### Security Architecture

#### Authentication & Authorization
- **JWT Tokens**: Short-lived access tokens (24h) with refresh token rotation
- **Role-Based Access Control**: Granular permissions for Customer, Delivery Partner, Admin roles
- **Multi-Factor Authentication**: OTP for sensitive operations and payment verification

#### Data Protection
- **Encryption**: AES-256 encryption for sensitive data at rest, TLS 1.3 for data in transit
- **Data Minimization**: Only collect and store necessary user data with clear retention policies
- **Compliance**: GDPR/PDPB compliance with user consent management and data subject rights

#### API Security
- **Rate Limiting**: Per-user and per-IP rate limiting to prevent abuse
- **Input Validation**: Comprehensive validation at API boundary using Pydantic
- **SQL Injection Prevention**: Parameterized queries through SQLAlchemy ORM

## Database Design

### Database Schema Overview

Quick Tym uses a normalized SQLite database (`quick_tym.db`) with 15 tables organized into logical domains: User Management, Product Catalog, Rental Operations, Delivery Logistics, Payment Processing, and AI Analytics.

```mermaid
erDiagram
    users ||--o{ rental_sessions : "creates"
    users ||--o{ deliveries : "assigned_to"
    users ||--o{ reviews : "writes"
    users ||--o{ notifications : "receives"
    
    products ||--o{ rental_sessions : "rented_in"
    products ||--o{ inventory : "tracks"
    products ||--o{ ai_recommendations : "recommended_in"
    
    categories ||--o{ products : "categorizes"
    
    rental_sessions ||--o{ bookings : "contains"
    rental_sessions ||--o{ deliveries : "requires"
    rental_sessions ||--o{ payments : "generates"
    
    deliveries ||--o{ delivery_tasks : "consists_of"
    deliveries ||--o{ pickup_requests : "handles"
    
    ai_recommendations }|--|| products : "recommends"
    demand_predictions }|--|| products : "predicts_for"
    
    users {
        uuid id PK
        string email UK
        string password_hash
        string name
        string role "Customer|Delivery_Partner|Admin"
        string phone
        jsonb address
        datetime created_at
        datetime updated_at
        boolean is_active
        decimal rating "4.2"
    }
    
    products {
        uuid id PK
        uuid category_id FK
        string name
        string description
        string category "Indoor|Outdoor"
        decimal price_per_hour "50-500"
        integer min_rental_hours
        jsonb specifications
        string image_url
        datetime created_at
    }
    
    rental_sessions {
        uuid id PK
        uuid user_id FK
        uuid product_id FK
        string status "pending|active|completed|cancelled"
        datetime start_time
        datetime end_time
        integer total_seconds
        decimal total_amount
        datetime created_at
        datetime updated_at
    }
```

### Table Definitions

#### 1. Users Table
**Purpose**: Store all system users with role-based permissions (Customer, Delivery_Partner, Admin)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- bcrypt hashed with work factor 12
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Customer', 'Delivery_Partner', 'Admin')),
    phone VARCHAR(15) UNIQUE,
    address JSONB NOT NULL DEFAULT '{}',
    location VARCHAR(100) DEFAULT 'Bengaluru',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(100),
    verification_expires TIMESTAMP,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(100),
    rating DECIMAL(3,2) DEFAULT 5.0 CHECK (rating >= 0 AND rating <= 5),
    total_rentals INTEGER DEFAULT 0,
    total_spent DECIMAL(12,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    last_password_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP,
    
    -- Role-specific fields
    delivery_partner_fields JSONB DEFAULT '{}', -- For Delivery_Partner role: vehicle_type, license_number, etc.
    admin_permissions JSONB DEFAULT '{}', -- For Admin role: specific permissions
    
    CONSTRAINT chk_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_phone_format CHECK (phone ~* '^[0-9]{10,15}$'),
    
    INDEX idx_users_email (email),
    INDEX idx_users_role (role),
    INDEX idx_users_rating (rating),
    INDEX idx_users_location (location),
    INDEX idx_users_is_active (is_active),
    INDEX idx_users_created_at (created_at)
);
```

#### 2. Roles Table (for permission management)
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    permissions JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. Products Table
**Purpose**: Catalog of rentable products with pricing and specifications (price bounds: ₹50-₹500)

```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID REFERENCES categories(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(20) NOT NULL CHECK (category IN ('Indoor', 'Outdoor')),
    price_per_hour DECIMAL(10,2) NOT NULL CHECK (price_per_hour BETWEEN 50 AND 500),
    min_rental_hours INTEGER DEFAULT 1 CHECK (min_rental_hours >= 1),
    max_rental_hours INTEGER DEFAULT 24 CHECK (max_rental_hours <= 168), -- 7 days max
    specifications JSONB NOT NULL DEFAULT '{}',
    features TEXT[] DEFAULT '{}',
    tags VARCHAR(50)[] DEFAULT '{}',
    image_url VARCHAR(500),
    gallery_urls VARCHAR(500)[] DEFAULT '{}',
    popularity_score DECIMAL(5,4) DEFAULT 0.0 CHECK (popularity_score >= 0 AND popularity_score <= 1),
    rental_count INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0 CHECK (average_rating >= 0 AND average_rating <= 5),
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    requires_delivery BOOLEAN DEFAULT TRUE,
    delivery_fee DECIMAL(10,2) DEFAULT 0.00,
    cleaning_fee DECIMAL(10,2) DEFAULT 0.00,
    security_deposit DECIMAL(10,2) DEFAULT 0.00,
    
    CONSTRAINT chk_price_range CHECK (price_per_hour >= 50 AND price_per_hour <= 500),
    CONSTRAINT chk_rental_hours CHECK (min_rental_hours <= max_rental_hours),
    
    INDEX idx_products_category (category),
    INDEX idx_products_price (price_per_hour),
    INDEX idx_products_category_id (category_id),
    INDEX idx_products_popularity (popularity_score),
    INDEX idx_products_rental_count (rental_count),
    INDEX idx_products_is_active (is_active),
    INDEX idx_products_tags (tags),
    INDEX idx_products_created_at (created_at)
);
```

#### 4. Categories Table
```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. Inventory Table
**Purpose**: Track physical product availability and stock levels

```sql
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    location VARCHAR(100) DEFAULT 'Bengaluru',
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    available_quantity INTEGER NOT NULL DEFAULT 0 CHECK (available_quantity >= 0),
    low_stock_threshold INTEGER DEFAULT 2,
    last_restocked TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(product_id, location),
    INDEX idx_inventory_product_id (product_id),
    INDEX idx_inventory_location (location),
    INDEX idx_inventory_availability (available_quantity)
);
```

#### 6. Rental Sessions Table
**Purpose**: Core table for time-based rental tracking with precise timing (1-second precision)

```sql
CREATE TABLE rental_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'active', 'completed', 'cancelled', 'overdue', 'paid')),
    -- Precise timing columns with 1-second precision
    start_time TIMESTAMP(0), -- Rounded to seconds
    end_time TIMESTAMP(0), -- Rounded to seconds
    total_seconds INTEGER CHECK (total_seconds >= 0),
    billable_seconds INTEGER CHECK (billable_seconds >= 0),
    -- Billing information
    base_amount DECIMAL(12,2) CHECK (base_amount >= 0),
    tax_amount DECIMAL(12,2) CHECK (tax_amount >= 0),
    delivery_fee DECIMAL(12,2) DEFAULT 0.00 CHECK (delivery_fee >= 0),
    cleaning_fee DECIMAL(12,2) DEFAULT 0.00 CHECK (cleaning_fee >= 0),
    security_deposit DECIMAL(12,2) DEFAULT 0.00 CHECK (security_deposit >= 0),
    deposit_returned BOOLEAN DEFAULT FALSE,
    total_amount DECIMAL(12,2) CHECK (total_amount >= 0),
    -- Location and delivery
    location VARCHAR(100) DEFAULT 'Bengaluru',
    delivery_address JSONB NOT NULL DEFAULT '{}',
    pickup_address JSONB DEFAULT '{}',
    -- Delivery tracking
    delivery_id UUID REFERENCES deliveries(id),
    pickup_request_id UUID REFERENCES pickup_requests(id),
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    cancelled_by UUID REFERENCES users(id),
    -- Payment tracking
    payment_id UUID REFERENCES payments(id),
    invoice_number VARCHAR(50) UNIQUE,
    -- Extensions
    extensions INTEGER DEFAULT 0,
    total_extended_seconds INTEGER DEFAULT 0,
    -- Audit fields
    timer_started_at TIMESTAMP,
    timer_stopped_at TIMESTAMP,
    last_timer_update TIMESTAMP,
    -- Constraints
    CONSTRAINT chk_timing CHECK (
        (end_time IS NULL) OR (end_time >= start_time)
    ),
    CONSTRAINT chk_billable_seconds CHECK (
        (billable_seconds IS NULL) OR (billable_seconds <= total_seconds)
    ),
    CONSTRAINT chk_status_transitions CHECK (
        status IN ('pending', 'active', 'completed', 'cancelled', 'overdue', 'paid')
    ),
    
    INDEX idx_rental_sessions_user_id (user_id),
    INDEX idx_rental_sessions_product_id (product_id),
    INDEX idx_rental_sessions_status (status),
    INDEX idx_rental_sessions_dates (start_time, end_time),
    INDEX idx_rental_sessions_created_at (created_at),
    INDEX idx_rental_sessions_location (location),
    INDEX idx_rental_sessions_payment_id (payment_id),
    INDEX idx_rental_sessions_invoice_number (invoice_number)
);
```

#### 7. Bookings Table
**Purpose**: Scheduled bookings for future rentals

```sql
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rental_session_id UUID REFERENCES rental_sessions(id) ON DELETE CASCADE,
    scheduled_start TIMESTAMP NOT NULL,
    scheduled_end TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('confirmed', 'pending', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_bookings_rental_session_id (rental_session_id),
    INDEX idx_bookings_scheduled_times (scheduled_start, scheduled_end)
);
```

#### 8. Payments Table
**Purpose**: Payment transaction records with mock payment system support

```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rental_session_id UUID REFERENCES rental_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
    currency VARCHAR(3) DEFAULT 'INR',
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'processing', 'success', 'failed', 'refunded', 'partially_refunded', 'disputed')),
    payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('credit_card', 'debit_card', 'upi', 'net_banking', 'wallet')),
    payment_gateway VARCHAR(50) DEFAULT 'mock', -- 'mock' for MVP, 'razorpay', 'stripe' for production
    -- Encrypted payment data (AES-256-GCM encrypted)
    card_number_encrypted VARCHAR(500), -- Encrypted card number
    card_expiry_encrypted VARCHAR(500), -- Encrypted expiry
    card_cvv_encrypted VARCHAR(500), -- Encrypted CVV
    upi_id_encrypted VARCHAR(500), -- Encrypted UPI ID
    -- Transaction details
    transaction_id VARCHAR(100) UNIQUE,
    gateway_transaction_id VARCHAR(200),
    gateway_response JSONB DEFAULT '{}',
    card_last4 VARCHAR(4),
    card_brand VARCHAR(20),
    card_country VARCHAR(2),
    -- Receipt and documentation
    receipt_url VARCHAR(500),
    invoice_url VARCHAR(500),
    tax_invoice_url VARCHAR(500),
    -- Refund information
    refund_amount DECIMAL(12,2) DEFAULT 0.00 CHECK (refund_amount >= 0),
    refund_reason TEXT,
    refunded_at TIMESTAMP,
    -- Security and compliance
    ip_address INET,
    user_agent TEXT,
    pci_compliant BOOLEAN DEFAULT TRUE,
    gdpr_compliant BOOLEAN DEFAULT TRUE,
    data_retention_until TIMESTAMP, -- GDPR/PDPB compliance
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    failed_at TIMESTAMP,
    -- Retry logic
    retry_count INTEGER DEFAULT 0 CHECK (retry_count >= 0),
    max_retries INTEGER DEFAULT 3 CHECK (max_retries >= 0),
    next_retry_at TIMESTAMP,
    last_retry_at TIMESTAMP,
    -- Constraints
    CONSTRAINT chk_refund_amount CHECK (refund_amount <= amount),
    CONSTRAINT chk_card_last4 CHECK (
        (card_last4 IS NULL) OR (card_last4 ~ '^[0-9]{4}$')
    ),
    CONSTRAINT chk_encrypted_fields CHECK (
        (card_number_encrypted IS NOT NULL AND payment_method IN ('credit_card', 'debit_card')) OR
        (upi_id_encrypted IS NOT NULL AND payment_method = 'upi') OR
        (payment_method NOT IN ('credit_card', 'debit_card', 'upi'))
    ),
    
    INDEX idx_payments_rental_session_id (rental_session_id),
    INDEX idx_payments_user_id (user_id),
    INDEX idx_payments_status (status),
    INDEX idx_payments_created_at (created_at),
    INDEX idx_payments_payment_method (payment_method),
    INDEX idx_payments_transaction_id (transaction_id),
    INDEX idx_payments_gateway (payment_gateway),
    INDEX idx_payments_data_retention (data_retention_until)
);
```

#### 9. Delivery Tasks Table
**Purpose**: Individual delivery/pickup tasks within a delivery

```sql
CREATE TABLE delivery_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    delivery_id UUID REFERENCES deliveries(id) ON DELETE CASCADE,
    task_type VARCHAR(20) NOT NULL CHECK (task_type IN ('delivery', 'pickup')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'assigned', 'in_progress', 'completed', 'failed')),
    assigned_to UUID REFERENCES users(id),
    scheduled_time TIMESTAMP,
    completed_time TIMESTAMP,
    address JSONB NOT NULL,
    notes TEXT,
    distance_km DECIMAL(8,2),
    estimated_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    photo_evidence_url VARCHAR(500),
    customer_signature_url VARCHAR(500),
    
    INDEX idx_delivery_tasks_delivery_id (delivery_id),
    INDEX idx_delivery_tasks_assigned_to (assigned_to),
    INDEX idx_delivery_tasks_status (status),
    INDEX idx_delivery_tasks_scheduled_time (scheduled_time)
);
```

#### 10. Deliveries Table
**Purpose**: Delivery assignments and tracking

```sql
CREATE TABLE deliveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rental_session_id UUID REFERENCES rental_sessions(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'assigned', 'in_transit', 'delivered', 'pickup_requested', 'completed')),
    assigned_partner_id UUID REFERENCES users(id),
    total_distance_km DECIMAL(10,2),
    total_estimated_minutes INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    route_coordinates JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_deliveries_rental_session_id (rental_session_id),
    INDEX idx_deliveries_assigned_partner_id (assigned_partner_id),
    INDEX idx_deliveries_status (status)
);
```

#### 11. Pickup Requests Table
```sql
CREATE TABLE pickup_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rental_session_id UUID REFERENCES rental_sessions(id) ON DELETE CASCADE,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'assigned', 'completed')),
    assigned_partner_id UUID REFERENCES users(id),
    completed_at TIMESTAMP,
    notes TEXT,
    
    INDEX idx_pickup_requests_rental_session_id (rental_session_id),
    INDEX idx_pickup_requests_status (status)
);
```

#### 12. Reviews Table
```sql
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    rental_session_id UUID REFERENCES rental_sessions(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, rental_session_id),
    INDEX idx_reviews_product_id (product_id),
    INDEX idx_reviews_rating (rating)
);
```

#### 13. Notifications Table
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_notifications_user_id (user_id),
    INDEX idx_notifications_is_read (is_read),
    INDEX idx_notifications_created_at (created_at)
);
```

#### 14. AI Recommendations Table
**Purpose**: Store personalized product recommendations with affinity scores (0-100), fallback to popular items, timeout handling

```sql
CREATE TABLE ai_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    recommendation_type VARCHAR(50) NOT NULL CHECK (recommendation_type IN ('similarity', 'popularity', 'collaborative', 'contextual', 'trending')),
    affinity_score INTEGER NOT NULL CHECK (affinity_score >= 0 AND affinity_score <= 100), -- 0-100 score
    confidence_score DECIMAL(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    -- Recommendation factors
    similarity_score DECIMAL(5,4) DEFAULT 0.0,
    popularity_score DECIMAL(5,4) DEFAULT 0.0,
    trending_score DECIMAL(5,4) DEFAULT 0.0,
    contextual_score DECIMAL(5,4) DEFAULT 0.0,
    -- Fallback tracking
    is_fallback BOOLEAN DEFAULT FALSE,
    fallback_reason VARCHAR(100),
    primary_recommendation_failed BOOLEAN DEFAULT FALSE,
    -- Timeout handling
    generation_time_ms INTEGER CHECK (generation_time_ms >= 0),
    timeout_occurred BOOLEAN DEFAULT FALSE,
    fallback_to_popular BOOLEAN DEFAULT FALSE,
    -- Context and metadata
    reason VARCHAR(200),
    context JSONB DEFAULT '{}', -- User context, session data, etc.
    metadata JSONB DEFAULT '{}',
    -- Performance tracking
    was_shown BOOLEAN DEFAULT FALSE,
    was_clicked BOOLEAN DEFAULT FALSE,
    click_position INTEGER CHECK (click_position >= 1),
    dwell_time_ms INTEGER CHECK (dwell_time_ms >= 0),
    conversion BOOLEAN DEFAULT FALSE,
    -- Timestamps
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    shown_at TIMESTAMP,
    clicked_at TIMESTAMP,
    converted_at TIMESTAMP,
    -- Model information
    model_version VARCHAR(50),
    model_parameters JSONB DEFAULT '{}',
    
    CONSTRAINT chk_affinity_score CHECK (affinity_score >= 0 AND affinity_score <= 100),
    CONSTRAINT chk_fallback_logic CHECK (
        (is_fallback = TRUE AND fallback_reason IS NOT NULL) OR
        (is_fallback = FALSE)
    ),
    CONSTRAINT chk_generation_time CHECK (
        (generation_time_ms IS NULL) OR (generation_time_ms <= 5000) -- Max 5 seconds
    ),
    
    INDEX idx_ai_recommendations_user_id (user_id),
    INDEX idx_ai_recommendations_product_id (product_id),
    INDEX idx_ai_recommendations_affinity_score (affinity_score),
    INDEX idx_ai_recommendations_type (recommendation_type),
    INDEX idx_ai_recommendations_expires_at (expires_at),
    INDEX idx_ai_recommendations_generated_at (generated_at),
    INDEX idx_ai_recommendations_was_clicked (was_clicked),
    INDEX idx_ai_recommendations_is_fallback (is_fallback),
    UNIQUE (user_id, product_id, recommendation_type, DATE(generated_at))
);
```

#### 15. Demand Predictions Table
**Purpose**: Store demand forecasts for inventory planning with time-series forecasting, confidence intervals, daily updates at 2 AM

```sql
CREATE TABLE demand_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    location VARCHAR(100) DEFAULT 'Bengaluru',
    prediction_date DATE NOT NULL,
    -- Time-series forecasting results
    predicted_demand INTEGER NOT NULL CHECK (predicted_demand >= 0),
    confidence_interval_lower INTEGER CHECK (confidence_interval_lower >= 0),
    confidence_interval_upper INTEGER CHECK (confidence_interval_upper >= 0),
    prediction_std_dev DECIMAL(10,2) CHECK (prediction_std_dev >= 0),
    -- Historical data for model training
    historical_mean DECIMAL(10,2) CHECK (historical_mean >= 0),
    historical_std_dev DECIMAL(10,2) CHECK (historical_std_dev >= 0),
    historical_trend DECIMAL(10,4),
    -- Seasonality factors
    weekday_factor DECIMAL(6,4) CHECK (weekday_factor >= 0),
    weekend_factor DECIMAL(6,4) CHECK (weekend_factor >= 0),
    holiday_factor DECIMAL(6,4) CHECK (holiday_factor >= 0),
    weather_factor DECIMAL(6,4) CHECK (weather_factor >= 0),
    -- Model information
    model_version VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) CHECK (model_type IN ('arima', 'sarima', 'exponential_smoothing', 'prophet', 'lstm', 'rule_based')),
    model_parameters JSONB DEFAULT '{}',
    model_accuracy DECIMAL(5,4) CHECK (model_accuracy >= 0 AND model_accuracy <= 1),
    -- Update schedule tracking
    update_schedule VARCHAR(50) DEFAULT 'daily_2am',
    last_training_date DATE,
    next_training_date DATE,
    -- Generation metadata
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generation_duration_ms INTEGER CHECK (generation_duration_ms >= 0),
    training_data_points INTEGER CHECK (training_data_points >= 0),
    -- Validation tracking
    actual_demand INTEGER CHECK (actual_demand >= 0),
    prediction_error INTEGER,
    absolute_error INTEGER,
    squared_error INTEGER,
    validated BOOLEAN DEFAULT FALSE,
    validated_at TIMESTAMP,
    -- Constraints
    CONSTRAINT chk_confidence_interval CHECK (
        confidence_interval_lower <= predicted_demand AND 
        predicted_demand <= confidence_interval_upper
    ),
    CONSTRAINT chk_historical_stats CHECK (
        historical_std_dev >= 0
    ),
    CONSTRAINT chk_factors CHECK (
        weekday_factor >= 0 AND weekend_factor >= 0 AND 
        holiday_factor >= 0 AND weather_factor >= 0
    ),
    CONSTRAINT chk_update_schedule CHECK (
        update_schedule IN ('daily_2am', 'weekly', 'monthly', 'on_demand')
    ),
    
    UNIQUE(product_id, location, prediction_date, model_version),
    INDEX idx_demand_predictions_product_id (product_id),
    INDEX idx_demand_predictions_date (prediction_date),
    INDEX idx_demand_predictions_location (location),
    INDEX idx_demand_predictions_model_version (model_version),
    INDEX idx_demand_predictions_generated_at (generated_at),
    INDEX idx_demand_predictions_update_schedule (update_schedule),
    INDEX idx_demand_predictions_validated (validated),
    INDEX idx_demand_predictions_confidence (confidence_interval_lower, confidence_interval_upper)
);
```

### Database Relationships

#### Foreign Key Constraints
- **Cascade Deletes**: User deletion cascades to their rental sessions, reviews, notifications
- **Restrict Deletes**: Product deletion restricted if active rentals exist
- **Set Null**: Category deletion sets product.category_id to NULL

#### Indexing Strategy
- **Primary Keys**: All tables use UUID primary keys for distributed system compatibility
- **Foreign Keys**: Index on all foreign key columns for join performance
- **Search Columns**: Index on email, product names, categories for fast searches
- **Date Columns**: Index on created_at, updated_at for time-based queries
- **Status Columns**: Index on status fields for filtering

### Data Integrity Rules

#### Business Logic Constraints
1. **Rental Time Validation**: `end_time` must be after `start_time` if both exist
2. **Price Range**: Product prices must be between ₹50 and ₹500 per hour
3. **Rating Boundaries**: User/product ratings between 0-5 with 2 decimal precision
4. **Quantity Non-Negative**: Inventory quantities cannot be negative
5. **Status Transitions**: Enforce valid state transitions (e.g., pending → active → completed)

#### Transaction Management
- **ACID Compliance**: All critical operations wrapped in transactions
- **Isolation Levels**: READ COMMITTED for balance between consistency and performance
- **Optimistic Locking**: Version columns for concurrent updates
- **Deadlock Prevention**: Consistent access patterns and transaction ordering

### Seed Data Strategy

#### Bengaluru Initial Data
```python
# Sample seed data for Bengaluru launch
SEED_PRODUCTS = [
    {
        "name": "Portable Projector",
        "category": "Indoor",
        "price_per_hour": 150,
        "description": "HD portable projector for indoor entertainment",
        "quantity": 10
    },
    {
        "name": "Mountain Bike",
        "category": "Outdoor", 
        "price_per_hour": 200,
        "description": "21-speed mountain bike for outdoor adventures",
        "quantity": 15
    }
    # ... more products
]

SEED_USERS = [
    {
        "email": "admin@quicktym.com",
        "name": "Admin User",
        "role": "Admin",
        "password": "secure_password"
    },
    {
        "email": "delivery@quicktym.com", 
        "name": "Delivery Partner",
        "role": "Delivery_Partner",
        "password": "secure_password"
    }
]
```

### Migration Strategy

#### Version Control
- **Alembic Migrations**: Version-controlled database migrations
- **Rollback Support**: Every migration has reversible downgrade
- **Environment-Specific**: Separate migration paths for dev/staging/prod

#### Data Migration
- **Zero-Downtime**: Blue-green deployment for schema changes
- **Data Backfill**: Background jobs for populating new columns
- **Validation Scripts**: Pre/post migration validation

## Frontend Architecture

### Component Hierarchy and Structure

Quick Tym's frontend follows Atomic Design principles with clear separation between reusable UI components, page layouts, and business logic.

```mermaid
graph TB
    subgraph "Atoms - Basic UI Elements"
        A1[Button]
        A2[Input]
        A3[Icon]
        A4[Typography]
        A5[Badge]
    end
    
    subgraph "Molecules - Component Groups"
        M1[SearchBar]
        M2[ProductCard]
        M3[UserMenu]
        M4[TimerDisplay]
        M5[PaymentForm]
    end
    
    subgraph "Organisms - Complex Components"
        O1[ProductGrid]
        O2[RentalTimer]
        O3[DeliveryMap]
        O4[CheckoutWizard]
        O5[AdminDashboard]
    end
    
    subgraph "Templates - Page Layouts"
        T1[MainLayout]
        T2[AuthLayout]
        T3[DashboardLayout]
        T4[CheckoutLayout]
    end
    
    subgraph "Pages - Route Components"
        P1[HomePage]
        P2[ProductPage]
        P3[RentalPage]
        P4[AdminPage]
    end
    
    A1 --> M1
    A2 --> M1
    A3 --> M2
    A4 --> M2
    M1 --> O1
    M2 --> O1
    M4 --> O2
    O1 --> P2
    O2 --> P3
    T1 --> P1
    T2 --> P4
```

### Directory Structure Detail

```
frontend/src/
├── components/                 # Reusable UI components
│   ├── atoms/                 # Basic building blocks
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.styles.ts
│   │   │   └── index.ts
│   │   ├── Input/
│   │   ├── Typography/
│   │   └── Icon/
│   ├── molecules/             # Component groups
│   │   ├── SearchBar/
│   │   ├── ProductCard/
│   │   ├── UserMenu/
│   │   └── TimerDisplay/
│   ├── organisms/             # Complex components
│   │   ├── ProductGrid/
│   │   ├── RentalTimer/
│   │   ├── DeliveryMap/
│   │   └── CheckoutWizard/
│   └── layouts/               # Layout components
│       ├── MainLayout/
│       ├── AuthLayout/
│       └── DashboardLayout/
│
├── pages/                     # Page components
│   ├── HomePage/
│   ├── ProductsPage/
│   ├── ProductDetailPage/
│   ├── CartPage/
│   ├── CheckoutPage/
│   ├── RentalTrackingPage/
│   ├── AdminDashboardPage/
│   ├── DeliveryPartnerPage/
│   ├── AuthPage/
│   └── NotFoundPage/
│
├── hooks/                     # Custom React hooks
│   ├── useAuth.ts
│   ├── useProducts.ts
│   ├── useRentalTimer.ts
│   ├── useWebSocket.ts
│   └── useFormValidation.ts
│
├── contexts/                  # React contexts
│   ├── AuthContext/
│   ├── CartContext/
│   ├── ThemeContext/
│   └── NotificationContext/
│
├── services/                  # API service clients
│   ├── apiClient.ts          # Base axios instance
│   ├── authService.ts
│   ├── productService.ts
│   ├── rentalService.ts
│   ├── deliveryService.ts
│   ├── paymentService.ts
│   └── aiService.ts
│
├── utils/                     # Utility functions
│   ├── formatters.ts         # Date, currency, string formatting
│   ├── validators.ts         # Form validation rules
│   ├── constants.ts          # App constants
│   └── helpers.ts            # General helpers
│
├── styles/                    # Global styles & themes
│   ├── theme.ts              # Design tokens
│   ├── globalStyles.ts       # Global CSS
│   ├── animations.ts         # CSS animations
│   └── breakpoints.ts        # Responsive breakpoints
│
├── types/                     # TypeScript definitions
│   ├── index.ts
│   ├── api.types.ts
│   ├── product.types.ts
│   └── user.types.ts
│
├── assets/                    # Static assets
│   ├── images/
│   ├── icons/
│   └── fonts/
│
└── App.tsx                    # Root component
```

### State Management Strategy

#### Global State Management
- **Auth Context**: User authentication, roles, permissions
- **Cart Context**: Shopping cart state, rental selections
- **Theme Context**: Light/dark mode, theme preferences
- **Notification Context**: Toast notifications, alerts

#### Local State Management
- **useState**: Component-specific UI state
- **useReducer**: Complex component state with actions
- **Custom Hooks**: Encapsulated state logic for reusability

#### Server State Management
- **React Query**: Data fetching, caching, synchronization
- **Optimistic Updates**: UI updates before server confirmation
- **Background Refetching**: Automatic data refresh

### Routing Architecture

#### Route Configuration
```typescript
// routes.tsx
const routes = [
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'products', element: <ProductsPage /> },
      { path: 'products/:id', element: <ProductDetailPage /> },
      { path: 'cart', element: <CartPage /> },
      { path: 'checkout', element: <CheckoutPage /> },
      { path: 'rental/:id', element: <RentalTrackingPage /> },
    ]
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
    ]
  },
  {
    path: '/admin',
    element: <ProtectedRoute role="Admin" />,
    children: [
      { index: true, element: <AdminDashboardPage /> },
      { path: 'users', element: <UserManagementPage /> },
      { path: 'inventory', element: <InventoryPage /> },
    ]
  },
  {
    path: '/delivery',
    element: <ProtectedRoute role="Delivery_Partner" />,
    children: [
      { index: true, element: <DeliveryPartnerPage /> },
      { path: 'tasks', element: <DeliveryTasksPage /> },
    ]
  }
];
```

#### Route Protection
- **ProtectedRoute**: Wrapper component for role-based access control
- **Auth Guards**: Redirect unauthenticated users to login
- **Role Guards**: Restrict access based on user role
- **Lazy Loading**: Code splitting for better performance

### Component Design Patterns

#### 1. Container-Presenter Pattern
```typescript
// Container (logic)
const ProductListContainer = () => {
  const { data: products, isLoading } = useProducts();
  const { addToCart } = useCart();
  
  return <ProductListPresentation 
    products={products}
    isLoading={isLoading}
    onAddToCart={addToCart}
  />;
};

// Presenter (UI)
const ProductListPresentation = ({ products, isLoading, onAddToCart }) => {
  if (isLoading) return <LoadingSpinner />;
  
  return (
    <div className="product-grid">
      {products.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onAddToCart={() => onAddToCart(product)}
        />
      ))}
    </div>
  );
};
```

#### 2. Compound Components
```typescript
const RentalTimer = ({ children }) => {
  const [time, setTime] = useState(0);
  
  return (
    <RentalTimerContext.Provider value={{ time, setTime }}>
      <div className="rental-timer">{children}</div>
    </RentalTimerContext.Provider>
  );
};

RentalTimer.Display = () => {
  const { time } = useContext(RentalTimerContext);
  return <div className="timer-display">{formatTime(time)}</div>;
};

RentalTimer.Controls = () => {
  const { setTime } = useContext(RentalTimerContext);
  return <button onClick={() => setTime(0)}>Reset</button>;
};

// Usage
<RentalTimer>
  <RentalTimer.Display />
  <RentalTimer.Controls />
</RentalTimer>
```

#### 3. Custom Hooks Pattern
```typescript
const useRentalTimer = (rentalId: string) => {
  const [time, setTime] = useState(0);
  const [isActive, setIsActive] = useState(false);
  
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isActive) {
      interval = setInterval(() => {
        setTime(prev => prev + 1);
      }, 1000);
    }
    
    return () => clearInterval(interval);
  }, [isActive]);
  
  const start = () => setIsActive(true);
  const stop = () => setIsActive(false);
  const reset = () => setTime(0);
  
  return { time, isActive, start, stop, reset };
};
```

### Styling System

#### Design Tokens
```typescript
// theme.ts
export const theme = {
  colors: {
    primary: {
      50: '#f8fafc',
      100: '#f1f5f9',
      // ... gradient
      900: '#0F172A', // Brand primary
    },
    accent: {
      50: '#f7fee7',
      100: '#ecfccb',
      // ... gradient  
      500: '#A3E635', // Brand accent
    },
    secondary: {
      50: '#eff6ff',
      100: '#dbeafe',
      // ... gradient
      600: '#2563EB', // Brand secondary
    }
  },
  typography: {
    fontFamily: "'Inter', sans-serif",
    fontSize: {
      base: '16px',
      sm: '14px',
      lg: '18px',
      xl: '24px',
      '2xl': '30px'
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75
    }
  },
  spacing: {
    base: '4px',
    xs: '8px',
    sm: '12px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px'
  },
  breakpoints: {
    mobile: '320px',
    tablet: '768px',
    desktop: '1024px',
    wide: '1440px'
  }
};
```

#### Responsive Design Approach
```typescript
// Mobile-first responsive utilities
const media = {
  mobile: `@media (min-width: ${theme.breakpoints.mobile})`,
  tablet: `@media (min-width: ${theme.breakpoints.tablet})`,
  desktop: `@media (min-width: ${theme.breakpoints.desktop})`,
};

// Usage in styled components
const Container = styled.div`
  padding: ${theme.spacing.md};
  
  ${media.tablet} {
    padding: ${theme.spacing.lg};
  }
  
  ${media.desktop} {
    padding: ${theme.spacing.xl};
  }
`;
```

### Performance Optimizations

#### Code Splitting
```typescript
// Lazy load heavy components
const ProductDetailPage = lazy(() => import('./pages/ProductDetailPage'));
const AdminDashboardPage = lazy(() => import('./pages/AdminDashboardPage'));

// Route-based code splitting
const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <HomePage /> },
      { 
        path: 'products/:id',
        element: (
          <Suspense fallback={<LoadingSpinner />}>
            <ProductDetailPage />
          </Suspense>
        )
      }
    ]
  }
]);
```

#### Image Optimization
- **Lazy Loading**: Images load as they enter viewport
- **Responsive Images**: srcset for different screen sizes
- **WebP Format**: Modern image format with better compression
- **Blur Placeholders**: Low-quality image placeholders during load

#### Bundle Optimization
- **Tree Shaking**: Remove unused code from production bundle
- **Code Splitting**: Split by route and feature
- **Chunk Optimization**: Vendor chunk separation
- **Compression**: Gzip/Brotli compression for assets

### Real-time Features

#### WebSocket Integration
```typescript
const useRentalWebSocket = (rentalId: string) => {
  const [timerData, setTimerData] = useState(null);
  
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/rental/${rentalId}`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setTimerData(data);
    };
    
    return () => ws.close();
  }, [rentalId]);
  
  return timerData;
};
```

#### Push Notifications
```typescript
// Service worker for push notifications
const registerServiceWorker = async () => {
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    const registration = await navigator.serviceWorker.register('/sw.js');
    
    // Request notification permission
    const permission = await Notification.requestPermission();
    
    if (permission === 'granted') {
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: VAPID_PUBLIC_KEY
      });
      
      // Send subscription to backend
      await saveSubscription(subscription);
    }
  }
};
```

### Accessibility Considerations

#### ARIA Attributes
- **Semantic HTML**: Proper heading hierarchy, landmark regions
- **ARIA Labels**: Descriptive labels for interactive elements
- **Keyboard Navigation**: Full keyboard support, focus management
- **Screen Reader Compatibility**: ARIA live regions for dynamic content

#### Color Contrast
- **WCAG Compliance**: Minimum 4.5:1 contrast ratio for normal text
- **Color Blind Mode**: Alternative color schemes for accessibility
- **Focus Indicators**: Clear visual focus for keyboard navigation

#### Responsive Touch Targets
- **Minimum Size**: 44×44px touch targets for mobile
- **Spacing**: Adequate spacing between interactive elements
- **Gesture Support**: Swipe, pinch, and tap gestures optimized

## Backend Architecture

### FastAPI Application Structure

Quick Tym's backend follows a clean, modular architecture with separation of concerns between API routes, business logic services, data models, and utilities.

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/                      # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py              # Application configuration
│   │   ├── database.py            # Database session management
│   │   ├── security.py            # Authentication & authorization
│   │   └── dependencies.py        # FastAPI dependencies
│   │
│   ├── api/                       # API route definitions
│   │   ├── __init__.py
│   │   ├── v1/                    # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main router
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── products.py        # Product endpoints
│   │   │   ├── rentals.py         # Rental endpoints
│   │   │   ├── deliveries.py      # Delivery endpoints
│   │   │   ├── payments.py        # Payment endpoints
│   │   │   ├── ai.py              # AI service endpoints
│   │   │   └── admin.py           # Admin endpoints
│   │   └── websocket.py           # WebSocket endpoints
│   │
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py                # Base model class
│   │   ├── user.py                # User model
│   │   ├── product.py             # Product model
│   │   ├── rental.py              # Rental session model
│   │   ├── delivery.py            # Delivery model
│   │   ├── payment.py             # Payment model
│   │   └── ai.py                  # AI models
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── base.py                # Base schemas
│   │   ├── user.py                # User schemas
│   │   ├── product.py             # Product schemas
│   │   ├── rental.py              # Rental schemas
│   │   ├── delivery.py            # Delivery schemas
│   │   ├── payment.py             # Payment schemas
│   │   └── ai.py                  # AI schemas
│   │
│   ├── services/                  # Business logic services
│   │   ├── __init__.py
│   │   ├── base.py                # Base service class
│   │   ├── auth_service.py        # Authentication service
│   │   ├── product_service.py     # Product management
│   │   ├── rental_service.py      # Rental operations
│   │   ├── timer_service.py       # Time-based billing
│   │   ├── delivery_service.py    # Delivery operations
│   │   ├── payment_service.py     # Payment processing
│   │   ├── inventory_service.py   # Inventory management
│   │   └── ai_service.py          # AI services
│   │
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py          # Data validation
│   │   ├── formatters.py          # Data formatting
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── logging.py             # Structured logging
│   │
│   └── workers/                   # Background workers
│       ├── __init__.py
│       ├── tasks.py               # Celery tasks
│       └── scheduler.py           # Scheduled jobs
│
├── alembic/                       # Database migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Test fixtures
│   ├── test_models.py
│   ├── test_services.py
│   └── test_api.py
│
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── .env.example                   # Environment variables
└── Dockerfile                     # Container configuration
```

### Core Application Configuration

#### FastAPI Application Setup
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine, Base

# Create FastAPI app
app = FastAPI(
    title="Quick Tym API",
    description="AI-powered rental system API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Create database tables (development only)
@app.on_event("startup")
async def startup_event():
    if settings.DEBUG:
        Base.metadata.create_all(bind=engine)
    
    # Initialize services
    await initialize_services()
```

#### Configuration Management
```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Application
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./quick_tym.db"
    DATABASE_POOL_SIZE: int = 5
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # Payment
    PAYMENT_MOCK_MODE: bool = True
    PAYMENT_SUCCESS_RATE: float = 0.9
    
    # AI Services
    AI_RECOMMENDATION_ENABLED: bool = True
    AI_DEMAND_PREDICTION_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Database Layer

#### SQLAlchemy ORM Setup
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Model Base Class
```python
# app/models/base.py
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

### Service Layer Architecture

#### Base Service Pattern
```python
# app/services/base.py
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType, db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: str) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = dict(obj_in)
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: str, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.get(id)
        if not db_obj:
            return None
        
        update_data = dict(obj_in)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: str) -> bool:
        db_obj = self.get(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
```

#### Rental Service Implementation
```python
# app/services/rental_service.py
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.rental import RentalSession
from app.models.product import Product
from app.schemas.rental import RentalCreate, RentalUpdate
from app.services.base import BaseService
from app.utils.exceptions import RentalException

class RentalService(BaseService[RentalSession, RentalCreate, RentalUpdate]):
    def __init__(self, db: Session):
        super().__init__(RentalSession, db)
    
    def start_rental(self, rental_id: str, delivery_time: datetime) -> RentalSession:
        """Start rental timer when product is delivered."""
        rental = self.get(rental_id)
        if not rental:
            raise RentalException("Rental not found")
        
        if rental.status != "pending":
            raise RentalException(f"Cannot start rental in status: {rental.status}")
        
        rental.start_time = delivery_time
        rental.status = "active"
        rental.updated_at = datetime.utcnow()
        
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        
        return rental
    
    def stop_rental(self, rental_id: str, pickup_time: datetime) -> RentalSession:
        """Stop rental timer when pickup is requested."""
        rental = self.get(rental_id)
        if not rental:
            raise RentalException("Rental not found")
        
        if rental.status != "active":
            raise RentalException(f"Cannot stop rental in status: {rental.status}")
        
        rental.end_time = pickup_time
        rental.status = "completed"
        rental.total_seconds = int((pickup_time - rental.start_time).total_seconds())
        rental.updated_at = datetime.utcnow()
        
        # Calculate charges
        rental.total_amount = self._calculate_charges(rental)
        
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        
        return rental
    
    def _calculate_charges(self, rental: RentalSession) -> Decimal:
        """Calculate rental charges based on elapsed time."""
        product = self.db.query(Product).filter(Product.id == rental.product_id).first()
        if not product:
            raise RentalException("Product not found")
        
        # Calculate hours (round up to nearest hour)
        hours = (rental.total_seconds + 3599) // 3600  # Ceiling division
        hours = max(1, hours)  # Minimum 1 hour
        
        total_amount = Decimal(hours) * product.price_per_hour
        
        # Apply taxes (18% GST for India)
        tax_rate = Decimal("0.18")
        tax_amount = total_amount * tax_rate
        
        return total_amount + tax_amount
    
    def get_active_rentals(self, user_id: str) -> List[RentalSession]:
        """Get all active rentals for a user."""
        return self.db.query(RentalSession).filter(
            RentalSession.user_id == user_id,
            RentalSession.status == "active"
        ).all()
    
    def get_rental_timer(self, rental_id: str) -> dict:
        """Get current timer status for a rental."""
        rental = self.get(rental_id)
        if not rental:
            raise RentalException("Rental not found")
        
        if rental.status != "active":
            return {"status": rental.status, "elapsed_seconds": 0}
        
        elapsed_seconds = int((datetime.utcnow() - rental.start_time).total_seconds())
        
        return {
            "status": rental.status,
            "elapsed_seconds": elapsed_seconds,
            "start_time": rental.start_time,
            "estimated_cost": self._calculate_estimated_cost(rental, elapsed_seconds)
        }
    
    def _calculate_estimated_cost(self, rental: RentalSession, elapsed_seconds: int) -> Decimal:
        """Calculate estimated cost based on current elapsed time."""
        product = self.db.query(Product).filter(Product.id == rental.product_id).first()
        if not product:
            return Decimal("0.00")
        
        # Calculate hours (round up to nearest hour)
        hours = (elapsed_seconds + 3599) // 3600  # Ceiling division
        hours = max(1, hours)  # Minimum 1 hour
        
        estimated_amount = Decimal(hours) * product.price_per_hour
        
        # Apply taxes
        tax_rate = Decimal("0.18")
        tax_amount = estimated_amount * tax_rate
        
        return estimated_amount + tax_amount
```

### Authentication & Authorization

#### JWT Authentication Service
```python
# app/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def create_user(self, user_in: UserCreate) -> User:
        """Create new user with hashed password."""
        hashed_password = self.get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            password_hash=hashed_password,
            name=user_in.name,
            role=user_in.role,
            phone=user_in.phone,
            address=user_in.address
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)
    
    def decode_token(self, token: str) -> Optional[TokenData]:
        """Decode and validate JWT token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            role: str = payload.get("role")
            if user_id is None or role is None:
                return None
            return TokenData(user_id=user_id, role=role)
        except JWTError:
            return None
```

#### Role-Based Access Control
```python
# app/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency to get current authenticated user."""
    auth_service = AuthService(db)
    token_data = auth_service.decode_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def require_role(required_role: str):
    """Dependency factory for role-based access control."""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker

# Usage in endpoints
@app.get("/admin/dashboard")
async def admin_dashboard(
    current_user: User = Depends(require_role("Admin"))
):
    return {"message": "Welcome to admin dashboard"}
```

### Background Tasks & Workers

#### Celery Task Configuration
```python
# app/workers/tasks.py
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "quick_tym",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

@celery_app.task
def process_delivery_optimization(delivery_ids: list):
    """Background task for delivery route optimization."""
    from app.services.delivery_service import DeliveryService
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        delivery_service = DeliveryService(db)
        optimized_routes = delivery_service.optimize_routes(delivery_ids)
        return optimized_routes
    finally:
        db.close()

@celery_app.task
def update_demand_predictions():
    """Scheduled task for demand prediction updates."""
    from app.services.ai_service import AIService
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        ai_service = AIService(db)
        predictions = ai_service.generate_demand_predictions()
        return {"predicted": len(predictions)}
    finally:
        db.close()

@celery_app.task
def send_notification(user_id: str, notification_type: str, data: dict):
    """Task for sending async notifications."""
    from app.services.notification_service import NotificationService
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        notification_service.send(user_id, notification_type, data)
        return {"sent": True}
    finally:
        db.close()
```

### Error Handling & Logging

#### Custom Exceptions
```python
# app/utils/exceptions.py
class QuickTymException(Exception):
    """Base exception for Quick Tym application."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class RentalException(QuickTymException):
    """Exception for rental-related errors."""
    pass

class PaymentException(QuickTymException):
    """Exception for payment-related errors."""
    pass

class DeliveryException(QuickTymException):
    """Exception for delivery-related errors."""
    pass

class AIException(QuickTymException):
    """Exception for AI service errors."""
    pass
```

#### Structured Logging
```python
# app/utils/logging.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler()
        handler.setFormatter(self._get_formatter())
        self.logger.addHandler(handler)
    
    def _get_formatter(self):
        """Get JSON formatter for structured logging."""
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "module": record.module,
                    "function": record.funcName,
                    "line": record.lineno,
                }
                
                # Add extra fields if present
                if hasattr(record, 'extra'):
                    log_data.update(record.extra)
                
                return json.dumps(log_data)
        
        return JSONFormatter()
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message with extra context."""
        self.logger.info(message, extra={"extra": extra} if extra else {})
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message with extra context."""
        self.logger.error(message, extra={"extra": extra} if extra else {})
    
    def warn(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message with extra context."""
        self.logger.warning(message, extra={"extra": extra} if extra else {})

# Global logger instance
logger = StructuredLogger("quick_tym")
```

### Testing Strategy

#### Test Structure
```python
# tests/test_rental_service.py
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from app.services.rental_service import RentalService
from app.models.rental import RentalSession
from app.models.product import Product
from app.utils.exceptions import RentalException

class TestRentalService:
    @pytest.fixture
    def rental_service(self, db_session):
        return RentalService(db_session)
    
    @pytest.fixture
    def sample_product(self, db_session):
        product = Product(
            name="Test Product",
            category="Indoor",
            price_per_hour=Decimal("100.00"),
            min_rental_hours=1
        )
        db_session.add(product)
        db_session.commit()
        return product
    
    def test_start_rental(self, rental_service, sample_product):
        # Create rental
        rental = RentalSession(
            user_id="test-user",
            product_id=sample_product.id,
            status="pending"
        )
        rental_service.db.add(rental)
        rental_service.db.commit()
        
        # Start rental
        delivery_time = datetime.utcnow()
        updated_rental = rental_service.start_rental(rental.id, delivery_time)
        
        assert updated_rental.status == "active"
        assert updated_rental.start_time == delivery_time
    
    def test_calculate_charges(self, rental_service, sample_product):
        # Create rental with 2.5 hours elapsed
        rental = RentalSession(
            user_id="test-user",
            product_id=sample_product.id,
            status="active",
            start_time=datetime.utcnow() - timedelta(hours=2, minutes=30),
            end_time=datetime.utcnow(),
            total_seconds=9000  # 2.5 hours
        )
        
        charges = rental_service._calculate_charges(rental)
        
        # Should charge for 3 hours (ceiling of 2.5) + 18% tax
        expected = Decimal("100.00") * 3 * Decimal("1.18")
        assert charges == expected
```

This backend architecture provides a solid foundation for Quick Tym's rental operations, with clear separation of concerns, comprehensive error handling, and extensible service design.

## API Design

### REST API Endpoints

Quick Tym provides a comprehensive REST API with versioned endpoints, consistent error handling, and comprehensive OpenAPI documentation.

#### API Versioning Strategy
- **Base Path**: `/api/v1` for current version
- **Media Type**: `application/json` for requests and responses
- **Version Headers**: `Accept: application/vnd.quicktym.v1+json`
- **Backward Compatibility**: Maintain at least one previous version

#### Authentication Endpoints

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register new user."""
    auth_service = AuthService(db)
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password strength
    if len(user_in.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Create user
    user = auth_service.create_user(user_in)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh JWT token."""
    auth_service = AuthService(db)
    new_token = auth_service.create_access_token(
        data={"sub": str(current_user.id), "role": current_user.role}
    )
    return {"access_token": new_token, "token_type": "bearer"}
```

#### Product Endpoints

```python
# app/api/v1/products.py
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="Filter by category: Indoor/Outdoor"),
    min_price: Optional[float] = Query(None, ge=50, le=500, description="Minimum price per hour"),
    max_price: Optional[float] = Query(None, ge=50, le=500, description="Maximum price per hour"),
    search: Optional[str] = Query(None, description="Search in name/description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get products with filtering and pagination."""
    product_service = ProductService(db)
    filters = {
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "search": search
    }
    products = product_service.get_products_with_filters(filters, skip, limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get product by ID."""
    product_service = ProductService(db)
    product = product_service.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    """Create new product (Admin only)."""
    product_service = ProductService(db)
    product = product_service.create(product_in)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    """Update product (Admin only)."""
    product_service = ProductService(db)
    product = product_service.update(product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/inventory")
async def get_product_inventory(
    product_id: str,
    location: str = Query("Bengaluru", description="Location for inventory check"),
    db: Session = Depends(get_db)
):
    """Get inventory status for a product."""
    inventory_service = InventoryService(db)
    inventory = inventory_service.get_product_inventory(product_id, location)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    return {
        "product_id": product_id,
        "location": location,
        "quantity": inventory.quantity,
        "available_quantity": inventory.available_quantity,
        "status": "Available" if inventory.available_quantity > 0 else "Out of Stock"
    }
```

#### Rental Endpoints

```python
# app/api/v1/rentals.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.rental import RentalCreate, RentalResponse, RentalTimerResponse
from app.services.rental_service import RentalService
from app.services.delivery_service import DeliveryService
from app.workers.tasks import send_notification

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.post("/", response_model=RentalResponse, status_code=201)
async def create_rental(
    rental_in: RentalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks
):
    """Create new rental booking."""
    # Check product availability
    inventory_service = InventoryService(db)
    if not inventory_service.check_availability(rental_in.product_id, rental_in.location):
        raise HTTPException(status_code=400, detail="Product not available")
    
    rental_service = RentalService(db)
    rental = rental_service.create(rental_in)
    
    # Reserve inventory
    inventory_service.reserve(rental_in.product_id, rental_in.location)
    
    # Schedule delivery assignment
    delivery_service = DeliveryService(db)
    background_tasks.add_task(
        delivery_service.assign_delivery,
        rental.id,
        rental_in.delivery_address
    )
    
    # Send confirmation notification
    background_tasks.add_task(
        send_notification,
        current_user.id,
        "rental_confirmed",
        {"rental_id": str(rental.id), "product_name": rental_in.product_name}
    )
    
    return rental

@router.post("/{rental_id}/start")
async def start_rental(
    rental_id: str,
    delivery_confirmation: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Delivery_Partner"))
):
    """Start rental timer when product is delivered."""
    rental_service = RentalService(db)
    delivery_time = datetime.utcnow()
    
    rental = rental_service.start_rental(rental_id, delivery_time)
    
    return {
        "rental_id": rental_id,
        "status": rental.status,
        "start_time": rental.start_time,
        "message": "Rental timer started"
    }

@router.post("/{rental_id}/stop")
async def stop_rental(
    rental_id: str,
    pickup_request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Stop rental timer when pickup is requested."""
    rental_service = RentalService(db)
    pickup_time = datetime.utcnow()
    
    rental = rental_service.stop_rental(rental_id, pickup_time)
    
    return {
        "rental_id": rental_id,
        "status": rental.status,
        "end_time": rental.end_time,
        "total_seconds": rental.total_seconds,
        "total_amount": rental.total_amount,
        "message": "Rental timer stopped"
    }

@router.get("/{rental_id}/timer", response_model=RentalTimerResponse)
async def get_rental_timer(
    rental_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current rental timer status."""
    rental_service = RentalService(db)
    timer_data = rental_service.get_rental_timer(rental_id)
    
    return timer_data

@router.get("/user/active")
async def get_active_rentals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active rentals for current user."""
    rental_service = RentalService(db)
    rentals = rental_service.get_active_rentals(current_user.id)
    
    return rentals

@router.post("/{rental_id}/cancel")
async def cancel_rental(
    rental_id: str,
    reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel rental before delivery."""
    rental_service = RentalService(db)
    
    rental = rental_service.get(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    if rental.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if rental.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot cancel rental in this status")
    
    rental.status = "cancelled"
    rental.cancellation_reason = reason
    rental.updated_at = datetime.utcnow()
    
    db.add(rental)
    db.commit()
    
    # Release inventory
    inventory_service = InventoryService(db)
    inventory_service.release(rental.product_id, rental.location)
    
    return {"message": "Rental cancelled successfully"}
```

#### Payment Endpoints

```python
# app/api/v1/payments.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentReceipt
from app.services.payment_service import PaymentService
from app.services.rental_service import RentalService

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/process", response_model=PaymentResponse)
async def process_payment(
    payment_in: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    background_tasks: BackgroundTasks
):
    """Process rental payment."""
    payment_service = PaymentService(db)
    
    # Validate rental exists and is completed
    rental_service = RentalService(db)
    rental = rental_service.get(payment_in.rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    if rental.status != "completed":
        raise HTTPException(status_code=400, detail="Rental must be completed before payment")
    
    if rental.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate payment amount matches rental total
    if payment_in.amount != rental.total_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Payment amount ({payment_in.amount}) doesn't match rental total ({rental.total_amount})"
        )
    
    # Process payment (mock for MVP)
    payment_result = payment_service.process_payment(payment_in)
    
    if payment_result["status"] == "success":
        # Update rental status
        rental.status = "paid"
        rental.updated_at = datetime.utcnow()
        db.add(rental)
        db.commit()
        
        # Generate receipt
        receipt = payment_service.generate_receipt(payment_result["transaction_id"])
        
        # Send receipt notification
        background_tasks.add_task(
            send_notification,
            current_user.id,
            "payment_success",
            {"transaction_id": payment_result["transaction_id"], "amount": str(payment_in.amount)}
        )
        
        return {
            "status": "success",
            "transaction_id": payment_result["transaction_id"],
            "receipt": receipt
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Payment failed: {payment_result.get('error', 'Unknown error')}"
        )

@router.get("/receipt/{transaction_id}", response_model=PaymentReceipt)
async def get_payment_receipt(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payment receipt by transaction ID."""
    payment_service = PaymentService(db)
    receipt = payment_service.get_receipt(transaction_id)
    
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    # Verify receipt belongs to current user
    if receipt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return receipt
```

#### AI Service Endpoints

```python
# app/api/v1/ai.py
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ai import RecommendationResponse, DemandPredictionResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI Services"])

@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=20)
):
    """Get personalized product recommendations."""
    ai_service = AIService(db)
    recommendations = ai_service.get_recommendations(current_user.id, limit)
    return recommendations

@router.get("/demand/predictions")
async def get_demand_predictions(
    product_id: str = Query(None, description="Filter by product ID"),
    location: str = Query("Bengaluru", description="Location for predictions"),
    days: int = Query(7, ge=1, le=30, description="Number of days to predict"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    """Get demand predictions (Admin only)."""
    ai_service = AIService(db)
    
    if product_id:
        predictions = ai_service.get_product_demand_predictions(product_id, location, days)
    else:
        predictions = ai_service.get_all_demand_predictions(location, days)
    
    return predictions

@router.post("/rental-assistant/query")
async def rental_assistant_query(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Query rental assistant with natural language."""
    ai_service = AIService(db)
    response = ai_service.process_rental_assistant_query(query, current_user.id)
    return response

@router.get("/delivery/optimize")
async def optimize_delivery_routes(
    location: str = Query("Bengaluru", description="Location for optimization"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    """Optimize delivery routes (Admin only)."""
    ai_service = AIService(db)
    optimized_routes = ai_service.optimize_delivery_routes(location)
    return optimized_routes
```

#### Admin Endpoints

```python
# app/api/v1/admin.py
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.admin import DashboardMetrics, UserManagementResponse
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
    timeframe: str = Query("today", enum=["today", "week", "month", "year"])
):
    """Get admin dashboard metrics."""
    admin_service = AdminService(db)
    metrics = admin_service.get_dashboard_metrics(timeframe)
    return metrics

@router.get("/users")
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
    role: str = Query(None, description="Filter by role"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get users with filtering (Admin only)."""
    admin_service = AdminService(db)
    users = admin_service.get_users(role, skip, limit)
    return users

@router.post("/users/{user_id}/suspend")
async def suspend_user(
    user_id: str,
    reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    """Suspend user account (Admin only)."""
    admin_service = AdminService(db)
    result = admin_service.suspend_user(user_id, reason, current_user.id)
    return result

@router.get("/inventory/report")
async def get_inventory_report(
    location: str = Query("Bengaluru", description="Location for report"),
    low_stock_only: bool = Query(False, description="Only show low stock items"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    """Get inventory report (Admin only)."""
    admin_service = AdminService(db)
    report = admin_service.get_inventory_report(location, low_stock_only)
    return report
```

### WebSocket Endpoints

```python
# app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict
import json
from app.core.database import get_db
from app.services.rental_service import RentalService
from app.services.notification_service import NotificationService

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/rental/{rental_id}")
async def rental_timer_websocket(websocket: WebSocket, rental_id: str):
    """WebSocket for real-time rental timer updates."""
    await websocket.accept()
    
    try:
        while True:
            # Wait for client messages (if any)
            data = await websocket.receive_text()
            
            # Get current timer status
            rental_service = RentalService(next(get_db()))
            timer_data = rental_service.get_rental_timer(rental_id)
            
            # Send timer update
            await websocket.send_json(timer_data)
            
            # Wait 1 second before next update
            import asyncio
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        # Clean up connection
        pass

@router.websocket("/ws/notifications")
async def notification_websocket(websocket: WebSocket, token: str):
    """WebSocket for real-time notifications."""
    # Validate token and get user_id
    auth_service = AuthService(next(get_db()))
    token_data = auth_service.decode_token(token)
    
    if not token_data:
        await websocket.close(code=1008)  # Policy violation
        return
    
    user_id = token_data.user_id
    
    await manager.connect(websocket, user_id)
    
    try:
        # Send any pending notifications
        notification_service = NotificationService(next(get_db()))
        pending = notification_service.get_pending_notifications(user_id)
        
        for notification in pending:
            await websocket.send_json(notification.to_dict())
        
        # Keep connection alive
        while True:
            await websocket.receive_text()  # Keep-alive
            await asyncio.sleep(30)  # Send ping every 30 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
```

### API Error Handling

#### Standard Error Responses
```python
from fastapi import HTTPException
from typing import Dict, Any

def create_error_response(
    status_code: int,
    detail: str,
    error_code: str = None,
    additional_info: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Create standardized error response."""
    response = {
        "error": {
            "code": error_code or f"ERR_{status_code}",
            "message": detail,
            "status": status_code
        }
    }
    
    if additional_info:
        response["error"]["details"] = additional_info
    
    return response

# Usage in endpoints
@router.get("/{id}")
async def get_item(id: str):
    item = get_item_from_db(id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=create_error_response(
                status_code=404,
                detail="Item not found",
                error_code="ITEM_NOT_FOUND",
                additional_info={"item_id": id}
            )
        )
    return item
```

#### Common Error Codes
- `AUTH_INVALID_CREDENTIALS`: Invalid email/password
- `AUTH_TOKEN_EXPIRED`: JWT token expired
- `AUTH_INSUFFICIENT_PERMISSIONS`: User lacks required role
- `RENTAL_NOT_FOUND`: Rental session not found
- `RENTAL_INVALID_STATUS`: Invalid status transition
- `PAYMENT_FAILED`: Payment processing failed
- `PRODUCT_UNAVAILABLE`: Product out of stock
- `DELIVERY_ASSIGNMENT_FAILED`: No delivery partners available
- `VALIDATION_ERROR`: Request data validation failed

### Rate Limiting

```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply rate limits
@router.get("/public-endpoint")
@limiter.limit("100/hour")
async def public_endpoint():
    return {"message": "Public endpoint"}

@router.get("/auth-endpoint")
@limiter.limit("1000/hour")
async def auth_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": "Authenticated endpoint"}

@router.post("/sensitive-operation")
@limiter.limit("10/minute")
async def sensitive_operation(current_user: User = Depends(get_current_user)):
    return {"message": "Sensitive operation"}
```

### API Documentation

#### OpenAPI Specification
- **Auto-generated Docs**: Available at `/docs` (Swagger UI) and `/redoc`
- **API Descriptions**: Detailed endpoint descriptions with examples
- **Request/Response Schemas**: Automatic schema generation from Pydantic models
- **Authentication**: Clear documentation of auth requirements

#### API Examples
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Quick Tym API",
    description="AI-powered rental system API",
    version="1.0.0",
    contact={
        "name": "Quick Tym Support",
        "email": "support@quicktym.com",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://quicktym.com/terms",
    },
)

class ProductResponse(BaseModel):
    """Product response model."""
    id: str
    name: str
    category: str
    price_per_hour: float
    description: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Portable Projector",
                "category": "Indoor",
                "price_per_hour": 150.00,
                "description": "HD portable projector for indoor entertainment"
            }
        }
```

This API design provides comprehensive functionality for Quick Tym's rental operations with proper authentication, error handling, rate limiting, and documentation.

## AI Features Design

### AI Architecture Overview

Quick Tym implements four core AI systems with detailed specifications:

1. **Recommendation Engine**: 
   - Affinity scores: 0-100 scale for personalized recommendations
   - Fallback mechanism: Automatic fallback to popular items when personalized recommendations fail
   - Timeout handling: Maximum 5-second response time with graceful degradation
   - Hybrid approach: Combines similarity, popularity, and contextual signals

2. **Demand Predictor**:
   - Time-series forecasting: ARIMA/SARIMA models with daily updates at 2 AM
   - Confidence intervals: 80% confidence bounds for demand predictions
   - Multi-factor analysis: Incorporates weekday/weekend patterns, holidays, weather
   - Model accuracy: >80% accuracy within confidence intervals

3. **Delivery Optimizer**:
   - k-means clustering: Groups deliveries by geographic proximity
   - Nearest neighbor algorithm: Optimizes delivery routes
   - Route accuracy: Within 15 minutes of estimated delivery time
   - Real-time updates: Adjusts routes based on traffic and partner availability

4. **Rental Assistant**:
   - Response time bounds: 5 seconds initial response, 3 seconds follow-up queries
   - Context maintenance: Maintains conversation context across multiple queries
   - Intent classification: Rule-based intent detection with keyword matching
   - Graceful degradation: Falls back to predefined responses when uncertain

All systems use rule-based logic for MVP with extensible interfaces for future ML integration, comprehensive monitoring, and performance tracking.

```mermaid
graph TB
    subgraph "AI Services Layer"
        A1[AI Service Orchestrator]
        A2[Recommendation Engine]
        A3[Demand Predictor]
        A4[Delivery Optimizer]
        A5[Rental Assistant]
    end
    
    subgraph "Data Sources"
        D1[Rental History]
        D2[User Profiles]
        D3[Product Catalog]
        D4[Location Data]
        D5[External APIs]
    end
    
    subgraph "Output Channels"
        O1[Personalized Recommendations]
        O2[Demand Forecasts]
        O3[Optimized Routes]
        O4[AI Chat Responses]
    end
    
    D1 --> A2
    D2 --> A2
    D3 --> A2
    D1 --> A3
    D4 --> A3
    D5 --> A3
    D4 --> A4
    D2 --> A4
    A1 --> O1
    A1 --> O2
    A1 --> O3
    A1 --> O4
    
    style A1 fill:#A3E635
    style A2 fill:#2563EB
    style A3 fill:#0F172A
    style A4 fill:#A3E635
```

### 1. Recommendation Engine

#### Architecture with Timeout Handling and Affinity Scores
```python
# app/services/ai/recommendation_engine.py
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product import Product
from app.models.rental import RentalSession
from app.models.ai import AIRecommendation

class RecommendationEngine:
    """Rule-based recommendation engine with affinity scores (0-100), timeout handling, and fallback mechanisms."""
    
    def __init__(self, db: Session, timeout_seconds: int = 5):
        self.db = db
        self.timeout_seconds = timeout_seconds
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def get_recommendations(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get personalized product recommendations with timeout handling and fallback."""
        start_time = time.time()
        
        try:
            # Try personalized recommendations with timeout
            future = self.executor.submit(self._get_recommendations_with_timeout, user_id, limit)
            recommendations = future.result(timeout=self.timeout_seconds)
            
            generation_time = int((time.time() - start_time) * 1000)
            
            # Save recommendations with metadata
            self._save_recommendations(user_id, recommendations, generation_time, False)
            
            return recommendations
            
        except TimeoutError:
            # Timeout occurred - use fallback to popular items
            generation_time = int((time.time() - start_time) * 1000)
            fallback_recommendations = self._get_fallback_recommendations(limit)
            
            # Save fallback recommendations
            self._save_recommendations(user_id, fallback_recommendations, generation_time, True)
            
            return fallback_recommendations
    
    def _get_recommendations_with_timeout(self, user_id: str, limit: int) -> List[Dict]:
        """Internal method for recommendation generation with timeout protection."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return self._get_popular_recommendations(limit, is_fallback=True)
        
        # Check user rental history
        rental_count = self.db.query(RentalSession).filter(
            RentalSession.user_id == user_id,
            RentalSession.status.in_(["completed", "active"])
        ).count()
        
        if rental_count < 3:  # Minimum history threshold
            return self._get_hybrid_recommendations(user_id, limit, is_fallback=False)
        
        # Generate personalized recommendations
        return self._generate_personalized_recommendations(user_id, limit)
    
    def _get_popular_recommendations(self, limit: int, is_fallback: bool = False) -> List[Dict]:
        """Get popular products based on rental frequency with affinity scores (0-100)."""
        from sqlalchemy import func
        
        # Query most rented products in last 30 days with rental statistics
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        popular_products = self.db.query(
            Product,
            func.count(RentalSession.id).label('rental_count'),
            func.avg(RentalSession.total_seconds).label('avg_duration'),
            func.avg(Product.price_per_hour).label('avg_price')
        ).join(
            RentalSession, RentalSession.product_id == Product.id
        ).filter(
            RentalSession.created_at >= thirty_days_ago,
            RentalSession.status.in_(["completed", "active"]),
            Product.is_active == True
        ).group_by(
            Product.id
        ).order_by(
            func.count(RentalSession.id).desc(),
            Product.popularity_score.desc()
        ).limit(limit * 2).all()
        
        recommendations = []
        for product, rental_count, avg_duration, avg_price in popular_products:
            # Calculate affinity score (0-100)
            popularity_score = min(100, int(rental_count * 2))  # Scale rental count to 0-100
            duration_score = min(30, int(avg_duration / 3600 * 5)) if avg_duration else 15  # Max 30 points
            price_score = 20 if avg_price and avg_price <= 200 else 10  # Price affordability
            
            affinity_score = popularity_score + duration_score + price_score
            affinity_score = min(100, max(0, affinity_score))  # Clamp to 0-100
            
            recommendations.append({
                "product": product,
                "affinity_score": affinity_score,
                "confidence_score": 0.8 if not is_fallback else 0.6,  # Lower confidence for fallback
                "similarity_score": 0.0,
                "popularity_score": popularity_score / 100.0,
                "trending_score": 0.7,
                "contextual_score": 0.5,
                "reason": "Popular in your area" if not is_fallback else "Popular fallback recommendation",
                "type": "popular",
                "is_fallback": is_fallback,
                "fallback_reason": "timeout" if is_fallback else None
            })
        
        # Sort by affinity score and limit
        recommendations.sort(key=lambda x: x["affinity_score"], reverse=True)
        return recommendations[:limit]
    
    def _get_hybrid_recommendations(self, user_id: str, limit: int) -> List[Dict]:
        """Get hybrid recommendations (personalized + popular)."""
        personalized = self._generate_personalized_recommendations(user_id, limit // 2)
        popular = self._get_popular_recommendations(limit - len(personalized))
        
        # Combine and deduplicate
        seen_ids = set()
        combined = []
        
        for rec in personalized + popular:
            product_id = rec["product"].id
            if product_id not in seen_ids:
                seen_ids.add(product_id)
                combined.append(rec)
        
        return combined[:limit]
    
    def _generate_personalized_recommendations(self, user_id: str, limit: int) -> List[Dict]:
        """Generate personalized recommendations based on user history."""
        # Get user's rental history
        user_rentals = self.db.query(RentalSession).filter(
            RentalSession.user_id == user_id,
            RentalSession.status.in_(["completed", "active"])
        ).all()
        
        if not user_rentals:
            return []
        
        # Extract categories from rented products
        rented_product_ids = [rental.product_id for rental in user_rentals]
        rented_products = self.db.query(Product).filter(
            Product.id.in_(rented_product_ids)
        ).all()
        
        rented_categories = set(product.category for product in rented_products)
        
        # Find similar products in same categories
        similar_products = self.db.query(Product).filter(
            Product.category.in_(rented_categories),
            ~Product.id.in_(rented_product_ids)
        ).order_by(
            Product.price_per_hour
        ).limit(limit * 2).all()
        
        # Score products based on similarity
        recommendations = []
        for product in similar_products:
            score = self._calculate_similarity_score(product, rented_products)
            
            if score >= 0.6:  # Minimum similarity threshold
                recommendations.append({
                    "product": product,
                    "score": score,
                    "reason": "Similar to previously rented items",
                    "type": "similarity"
                })
        
        # Sort by score and limit
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]
    
    def _calculate_similarity_score(self, product: Product, rented_products: List[Product]) -> float:
        """Calculate similarity score between product and rented products."""
        if not rented_products:
            return 0.0
        
        # Simple rule-based scoring for MVP
        scores = []
        
        for rented in rented_products:
            # Category match (40% weight)
            category_score = 0.4 if product.category == rented.category else 0.0
            
            # Price similarity (30% weight)
            price_diff = abs(product.price_per_hour - rented.price_per_hour)
            price_score = max(0, 0.3 * (1.0 - price_diff / 100.0))
            
            # Description similarity (30% weight) - simple keyword matching
            desc_similarity = self._text_similarity(product.description, rented.description)
            desc_score = 0.3 * desc_similarity
            
            scores.append(category_score + price_score + desc_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (MVP implementation)."""
        if not text1 or not text2:
            return 0.0
        
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _get_fallback_recommendations(self, limit: int) -> List[Dict]:
        """Get fallback recommendations when primary recommendation fails."""
        fallback_recommendations = self._get_popular_recommendations(limit, is_fallback=True)
        
        # Add metadata for fallback
        for rec in fallback_recommendations:
            rec["timeout_occurred"] = True
            rec["generation_time_exceeded"] = True
        
        return fallback_recommendations
    
    def _save_recommendations(self, user_id: str, recommendations: List[Dict], 
                            generation_time_ms: int, is_fallback: bool) -> None:
        """Save recommendations to database for tracking and analysis."""
        from app.models.ai import AIRecommendation
        
        for rec in recommendations:
            # Calculate affinity score from various components
            affinity_score = int(rec.get("affinity_score", 0))
            if affinity_score == 0:
                # Calculate from component scores
                similarity = rec.get("similarity_score", 0.0) * 100
                popularity = rec.get("popularity_score", 0.0) * 100
                trending = rec.get("trending_score", 0.0) * 100
                contextual = rec.get("contextual_score", 0.0) * 100
                affinity_score = int((similarity + popularity + trending + contextual) / 4)
            
            db_recommendation = AIRecommendation(
                user_id=user_id,
                product_id=rec["product"].id,
                recommendation_type=rec["type"],
                affinity_score=affinity_score,
                confidence_score=rec.get("confidence_score", 0.7),
                similarity_score=rec.get("similarity_score", 0.0),
                popularity_score=rec.get("popularity_score", 0.0),
                trending_score=rec.get("trending_score", 0.0),
                contextual_score=rec.get("contextual_score", 0.0),
                is_fallback=is_fallback,
                fallback_reason="timeout" if is_fallback else None,
                primary_recommendation_failed=is_fallback,
                generation_time_ms=generation_time_ms,
                timeout_occurred=is_fallback,
                fallback_to_popular=is_fallback,
                reason=rec.get("reason", "Personalized recommendation"),
                context={"generation_time_ms": generation_time_ms, "is_fallback": is_fallback},
                generated_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            self.db.add(db_recommendation)
        
        self.db.commit()
    
    def save_recommendations(self, user_id: str, recommendations: List[Dict]):
        """Save recommendations to database for tracking and analysis."""
        for rec in recommendations:
            db_recommendation = AIRecommendation(
                user_id=user_id,
                product_id=rec["product"].id,
                recommendation_type=rec["type"],
                score=rec["score"],
                reason=rec["reason"],
                generated_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=7)  # Recommendations expire in 7 days
            )
            self.db.add(db_recommendation)
        
        self.db.commit()
```

### 2. Demand Prediction System

#### Architecture
```python
# app/services/ai/demand_predictor.py
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import statistics
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.product import Product
from app.models.rental import RentalSession
from app.models.demand_prediction import DemandPrediction

class DemandPredictor:
    """Rule-based demand prediction for MVP with time-series analysis."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_predictions(self, location: str = "Bengaluru", days: int = 7) -> List[DemandPrediction]:
        """Generate demand predictions for next N days."""
        predictions = []
        
        # Get all products
        products = self.db.query(Product).all()
        
        for product in products:
            # Generate prediction for each day
            for day_offset in range(1, days + 1):
                prediction_date = datetime.utcnow().date() + timedelta(days=day_offset)
                
                # Get historical data for this product
                historical_data = self._get_historical_data(product.id, location, days=90)
                
                if not historical_data:
                    # No history, use default prediction
                    predicted_demand = 1
                    confidence_lower = 0
                    confidence_upper = 3
                else:
                    # Apply time-series analysis
                    predicted_demand = self._predict_demand(
                        product.id, 
                        historical_data, 
                        prediction_date
                    )
                    
                    # Calculate confidence intervals
                    confidence_lower, confidence_upper = self._calculate_confidence_intervals(
                        historical_data, 
                        predicted_demand
                    )
                
                # Create prediction record
                prediction = DemandPrediction(
                    product_id=product.id,
                    location=location,
                    prediction_date=prediction_date,
                    predicted_demand=predicted_demand,
                    confidence_interval_lower=confidence_lower,
                    confidence_interval_upper=confidence_upper,
                    model_version="rule_based_v1",
                    generated_at=datetime.utcnow()
                )
                
                predictions.append(prediction)
        
        # Save predictions to database
        self.db.add_all(predictions)
        self.db.commit()
        
        return predictions
    
    def _get_historical_data(self, product_id: str, location: str, days: int) -> List[Dict]:
        """Get historical rental data for product."""
        start_date = datetime.utcnow().date() - timedelta(days=days)
        
        historical = self.db.query(
            func.date(RentalSession.start_time).label('date'),
            func.count(RentalSession.id).label('count')
        ).filter(
            RentalSession.product_id == product_id,
            RentalSession.start_time >= start_date,
            RentalSession.status.in_(["completed", "active"])
        ).group_by(
            func.date(RentalSession.start_time)
        ).order_by(
            func.date(RentalSession.start_time)
        ).all()
        
        return [{"date": h.date, "count": h.count} for h in historical]
    
    def _predict_demand(self, product_id: str, historical_data: List[Dict], target_date: datetime.date) -> int:
        """Predict demand using rule-based time-series analysis."""
        if not historical_data:
            return 1  # Default minimum
        
        # Extract day of week pattern
        day_of_week = target_date.weekday()  # 0=Monday, 6=Sunday
        
        # Filter historical data for same day of week
        same_day_data = []
        for data in historical_data:
            if data["date"].weekday() == day_of_week:
                same_day_data.append(data["count"])
        
        if same_day_data:
            # Use median of same day of week historical data
            base_prediction = int(statistics.median(same_day_data))
        else:
            # Use overall median
            all_counts = [data["count"] for data in historical_data]
            base_prediction = int(statistics.median(all_counts)) if all_counts else 1
        
        # Apply seasonal adjustments (simple weekend multiplier)
        if day_of_week >= 5:  # Saturday or Sunday
            base_prediction = int(base_prediction * 1.5)
        
        # Apply trend (simple moving average)
        if len(historical_data) >= 7:
            recent_counts = [data["count"] for data in historical_data[-7:]]
            recent_avg = sum(recent_counts) / len(recent_counts)
            trend_adjustment = recent_avg / (sum([data["count"] for data in historical_data]) / len(historical_data))
            base_prediction = int(base_prediction * trend_adjustment)
        
        # Ensure minimum prediction
        return max(1, base_prediction)
    
    def _calculate_confidence_intervals(self, historical_data: List[Dict], predicted: int) -> tuple:
        """Calculate 80% confidence intervals for prediction."""
        if len(historical_data) < 5:
            return max(0, predicted - 1), predicted + 2
        
        counts = [data["count"] for data in historical_data]
        std_dev = statistics.stdev(counts) if len(counts) > 1 else 1.0
        
        # 80% confidence interval (z-score ≈ 1.28 for 80%)
        margin = 1.28 * std_dev
        
        lower = max(0, int(predicted - margin))
        upper = int(predicted + margin)
        
        return lower, upper
    
    def get_recommended_stock_levels(self, product_id: str, location: str) -> Dict:
        """Get recommended stock levels based on predictions."""
        # Get latest predictions
        predictions = self.db.query(DemandPrediction).filter(
            DemandPrediction.product_id == product_id,
            DemandPrediction.location == location,
            DemandPrediction.prediction_date >= datetime.utcnow().date()
        ).order_by(
            DemandPrediction.prediction_date
        ).limit(7).all()
        
        if not predictions:
            return {"recommended_stock": 5, "buffer_percentage": 20}
        
        # Calculate max predicted demand in next 7 days
        max_demand = max(pred.predicted_demand for pred in predictions)
        
        # Add 20% buffer
        recommended_stock = int(max_demand * 1.2)
        
        return {
            "product_id": product_id,
            "location": location,
            "recommended_stock": recommended_stock,
            "buffer_percentage": 20,
            "max_predicted_demand": max_demand,
            "predictions": [
                {
                    "date": pred.prediction_date.isoformat(),
                    "predicted": pred.predicted_demand,
                    "confidence_lower": pred.confidence_interval_lower,
                    "confidence_upper": pred.confidence_interval_upper
                }
                for pred in predictions
            ]
        }
```

### 3. Delivery Optimization System

#### Architecture
```python
# app/services/ai/delivery_optimizer.py
from typing import List, Dict, Tuple
from datetime import datetime
import math
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.delivery import Delivery, DeliveryTask
from app.models.rental import RentalSession

class DeliveryOptimizer:
    """Rule-based delivery optimization using VRP algorithms."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def optimize_delivery_routes(self, location: str = "Bengaluru") -> List[Dict]:
        """Optimize delivery routes for pending deliveries."""
        # Get pending deliveries
        pending_deliveries = self.db.query(Delivery).filter(
            Delivery.status == "pending",
            Delivery.location == location
        ).all()
        
        if not pending_deliveries:
            return []
        
        # Get available delivery partners
        available_partners = self.db.query(User).filter(
            User.role == "Delivery_Partner",
            User.is_active == True,
            User.location == location,
            User.current_load < 3  # Partners with less than 3 active deliveries
        ).order_by(
            User.rating.desc()
        ).all()
        
        if not available_partners:
            return []
        
        # Group deliveries by geographic clusters
        clusters = self._cluster_deliveries(pending_deliveries, len(available_partners))
        
        # Assign clusters to partners and optimize routes
        optimized_routes = []
        for i, (partner, cluster_deliveries) in enumerate(zip(available_partners, clusters)):
            if i >= len(clusters):
                break
            
            route = self._optimize_single_route(partner, cluster_deliveries)
            optimized_routes.append(route)
        
        return optimized_routes
    
    def _cluster_deliveries(self, deliveries: List[Delivery], num_clusters: int) -> List[List[Delivery]]:
        """Cluster deliveries using k-means (simplified for MVP)."""
        if len(deliveries) <= num_clusters:
            return [[d] for d in deliveries]
        
        # Simple geographic clustering by dividing area into grid
        # For MVP, use rental session addresses
        clusters = [[] for _ in range(min(num_clusters, len(deliveries)))]
        
        # Sort deliveries by creation time and distribute
        sorted_deliveries = sorted(deliveries, key=lambda d: d.created_at)
        
        for i, delivery in enumerate(sorted_deliveries):
            cluster_idx = i % len(clusters)
            clusters[cluster_idx].append(delivery)
        
        return clusters
    
    def _optimize_single_route(self, partner: User, deliveries: List[Delivery]) -> Dict:
        """Optimize route for single delivery partner using Nearest Neighbor algorithm."""
        if not deliveries:
            return {
                "partner_id": partner.id,
                "partner_name": partner.name,
                "route": [],
                "total_distance_km": 0,
                "estimated_duration_minutes": 0
            }
        
        # Start from partner's current location (or depot)
        start_location = self._get_partner_location(partner)
        
        # Convert deliveries to locations
        locations = [(start_location, "depot")]  # (coordinates, delivery_id)
        for delivery in deliveries:
            location = self._get_delivery_location(delivery)
            locations.append((location, delivery.id))
        
        # Apply Nearest Neighbor algorithm
        route = []
        unvisited = locations[1:]  # Exclude depot
        current = locations[0]  # Start at depot
        
        while unvisited:
            # Find nearest unvisited location
            nearest = min(
                unvisited,
                key=lambda loc: self._calculate_distance(current[0], loc[0])
            )
            
            route.append(nearest[1])  # Add delivery ID to route
            current = nearest
            unvisited.remove(nearest)
        
        # Return to depot (optional)
        return_to_depot = True
        if return_to_depot:
            route.append("depot")
        
        # Calculate total distance and estimated time
        total_distance = self._calculate_route_distance([start_location] + [
            self._get_delivery_location_by_id(delivery_id)
            for delivery_id in route if delivery_id != "depot"
        ])
        
        # Estimate time (assuming 30 km/h average speed + 10 minutes per stop)
        estimated_time = (total_distance / 30 * 60) + (len(deliveries) * 10)
        
        return {
            "partner_id": partner.id,
            "partner_name": partner.name,
            "partner_rating": float(partner.rating),
            "route": route,
            "deliveries": [{"id": d.id, "address": d.delivery_address} for d in deliveries],
            "total_distance_km": round(total_distance, 2),
            "estimated_duration_minutes": int(estimated_time),
            "optimized_at": datetime.utcnow().isoformat()
        }
    
    def _get_partner_location(self, partner: User) -> Tuple[float, float]:
        """Get partner's current location (simplified for MVP)."""
        # For MVP, use fixed depot location in Bengaluru
        # In production, would use GPS coordinates from mobile app
        return (12.9716, 77.5946)  # Bangalore coordinates
    
    def _get_delivery_location(self, delivery: Delivery) -> Tuple[float, float]:
        """Extract coordinates from delivery address (simplified for MVP)."""
        # For MVP, use mock coordinates based on delivery ID
        # In production, would geocode the address
        import hashlib
        
        # Generate deterministic "coordinates" from delivery ID
        hash_obj = hashlib.md5(str(delivery.id).encode())
        hash_int = int(hash_obj.hexdigest()[:8], 16)
        
        # Generate coordinates within Bengaluru area
        lat = 12.97 + (hash_int % 1000) / 10000  # 12.97 to 13.07
        lng = 77.59 + (hash_int % 1000) / 10000  # 77.59 to 77.69
        
        return (lat, lng)
    
    def _get_delivery_location_by_id(self, delivery_id: str) -> Tuple[float, float]:
        """Get location for delivery ID."""
        if delivery_id == "depot":
            return self._get_partner_location(None)
        
        delivery = self.db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if delivery:
            return self._get_delivery_location(delivery)
        
        # Default location
        return (12.9716, 77.5946)
    
    def _calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between coordinates (simplified)."""
        lat1, lng1 = coord1
        lat2, lng2 = coord2
        
        # Simple Euclidean distance (not accurate for Earth, but sufficient for MVP)
        return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2) * 111  # Approx km per degree
    
    def _calculate_route_distance(self, locations: List[Tuple[float, float]]) -> float:
        """Calculate total distance for a route."""
        if len(locations) < 2:
            return 0.0
        
        total_distance = 0.0
        for i in range(len(locations) - 1):
            total_distance += self._calculate_distance(locations[i], locations[i + 1])
        
        return total_distance
    
    def assign_delivery(self, rental_id: str, delivery_address: str) -> Optional[str]:
        """Assign delivery to optimal partner."""
        # Get available partners
        available_partners = self.db.query(User).filter(
            User.role == "Delivery_Partner",
            User.is_active == True,
            User.current_load < 3
        ).order_by(
            User.rating.desc()
        ).all()
        
        if not available_partners:
            return None
        
        # Simple assignment: partner with highest rating and lowest load
        best_partner = min(
            available_partners,
            key=lambda p: (p.current_load, -p.rating)  # Lower load, higher rating
        )
        
        # Update partner's current load
        best_partner.current_load += 1
        
        # Create delivery record
        delivery = Delivery(
            rental_session_id=rental_id,
            assigned_partner_id=best_partner.id,
            status="assigned",
            delivery_address=delivery_address,
            created_at=datetime.utcnow()
        )
        
        self.db.add(delivery)
        self.db.commit()
        
        return best_partner.id
```

### 4. Rental Assistant

#### Architecture
```python
# app/services/ai/rental_assistant.py
from typing import Dict, List, Optional
import re
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.rental import RentalSession
from app.models.user import User

class RentalAssistant:
    """Rule-based rental assistant for customer support."""
    
    def __init__(self, db: Session):
        self.db = db
        self.context = {}  # Conversation context
    
    def process_query(self, query: str, user_id: str) -> Dict:
        """Process natural language query and generate response."""
        # Clean and analyze query
        clean_query = query.lower().strip()
        
        # Check for intent
        intent = self._classify_intent(clean_query)
        
        # Process based on intent
        if intent == "product_recommendation":
            response = self._handle_product_recommendation(clean_query, user_id)
        elif intent == "rental_duration":
            response = self._handle_rental_duration(clean_query, user_id)
        elif intent == "pricing":
            response = self._handle_pricing(clean_query, user_id)
        elif intent == "availability":
            response = self._handle_availability(clean_query, user_id)
        elif intent == "delivery":
            response = self._handle_delivery(clean_query, user_id)
        elif intent == "help":
            response = self._handle_help(clean_query)
        else:
            response = self._handle_unknown(clean_query)
        
        # Store context for follow-up questions
        self.context[user_id] = {
            "last_query": query,
            "last_intent": intent,
            "timestamp": datetime.utcnow()
        }
        
        return response
    
    def _classify_intent(self, query: str) -> str:
        """Classify query intent using keyword matching."""
        intent_keywords = {
            "product_recommendation": [
                "recommend", "suggest", "what should i", "which one", "best for",
                "looking for", "need help choosing", "can't decide"
            ],
            "rental_duration": [
                "how long", "duration", "time needed", "hours", "minimum",
                "maximum", "time limit"
            ],
            "pricing": [
                "price", "cost", "how much", "expensive", "cheap", "rate",
                "charges", "billing", "pay"
            ],
            "availability": [
                "available", "in stock", "out of stock", "when available",
                "restock", "waiting list", "reserve"
            ],
            "delivery": [
                "delivery", "pickup", "shipping", "transport", "bring",
                "collect", "drop off", "time to deliver"
            ],
            "help": [
                "help", "assist", "support", "guide", "explain", "how to",
                "what is", "tell me about"
            ]
        }
        
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return intent
        
        return "unknown"
    
    def _handle_product_recommendation(self, query: str, user_id: str) -> Dict:
        """Handle product recommendation queries."""
        # Extract product type from query
        product_type = self._extract_product_type(query)
        
        if product_type:
            # Find products matching the type
            products = self.db.query(Product).filter(
                Product.category.ilike(f"%{product_type}%") |
                Product.name.ilike(f"%{product_type}%") |
                Product.description.ilike(f"%{product_type}%")
            ).limit(3).all()
            
            if products:
                product_list = "\n".join([
                    f"- {p.name}: ₹{p.price_per_hour}/hour ({p.category})"
                    for p in products
                ])
                
                return {
                    "response": f"Based on your interest in {product_type}, I recommend:\n\n{product_list}\n\nYou can click on any product for more details or ask me specific questions about them.",
                    "confidence": 0.85,
                    "suggested_actions": [
                        {"action": "view_products", "label": "View all products"},
                        {"action": "filter", "label": f"Filter by {product_type}"}
                    ]
                }
        
        # General recommendation
        return {
            "response": "I'd be happy to help you find the perfect product! Could you tell me:\n1. What you'll be using it for?\n2. Your budget range?\n3. How long you need it?\n\nOr you can browse our categories: Indoor Rentals or Outdoor Rentals.",
            "confidence": 0.7,
            "suggested_actions": [
                {"action": "browse_indoor", "label": "Browse Indoor Rentals"},
                {"action": "browse_outdoor", "label": "Browse Outdoor Rentals"}
            ]
        }
    
    def _handle_pricing(self, query: str, user_id: str) -> Dict:
        """Handle pricing queries."""
        # Extract product name from query
        product_name = self._extract_product_name(query)
        
        if product_name:
            product = self.db.query(Product).filter(
                Product.name.ilike(f"%{product_name}%")
            ).first()
            
            if product:
                return {
                    "response": f"{product.name} costs ₹{product.price_per_hour} per hour.\n\nRental charges are calculated based on actual usage time, with a minimum of 1 hour. The timer stops immediately when you request pickup.",
                    "confidence": 0.95,
                    "data": {
                        "product_name": product.name,
                        "price_per_hour": float(product.price_per_hour),
                        "min_rental_hours": product.min_rental_hours
                    }
                }
        
        # General pricing information
        return {
            "response": "Quick Tym uses time-based billing:\n\n• Prices range from ₹50 to ₹500 per hour\n• You only pay for actual usage time\n• Minimum charge is for 1 hour\n• Rental timer stops immediately when pickup is requested\n• All prices include GST\n\nYou can view specific product prices on their detail pages.",
            "confidence": 0.9,
            "suggested_actions": [
                {"action": "view_pricing", "label": "View pricing guide"},
                {"action": "calculator", "label": "Try cost calculator"}
            ]
        }
    
    def _extract_product_type(self, query: str) -> Optional[str]:
        """Extract product type from query."""
        product_types = [
            "projector", "bike", "camera", "speaker", "tent", "grill",
            "game", "console", "tool", "equipment", "indoor", "outdoor"
        ]
        
        for product_type in product_types:
            if product_type in query:
                return product_type
        
        return None
    
    def _extract_product_name(self, query: str) -> Optional[str]:
        """Extract product name from query."""
        # Look for product names in query
        products = self.db.query(Product.name).all()
        product_names = [p[0].lower() for p in products]
        
        for name in product_names:
            if name in query:
                return name
        
        return None
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for user."""
        # In production, would query from database
        # For MVP, return empty list
        return []
```

### AI Service Integration

```python
# app/services/ai_service.py
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.services.ai.recommendation_engine import RecommendationEngine
from app.services.ai.demand_predictor import DemandPredictor
from app.services.ai.delivery_optimizer import DeliveryOptimizer
from app.services.ai.rental_assistant import RentalAssistant

class AIService:
    """Orchestrator for all AI services."""
    
    def __init__(self, db: Session):
        self.db = db
        self.recommendation_engine = RecommendationEngine(db)
        self.demand_predictor = DemandPredictor(db)
        self.delivery_optimizer = DeliveryOptimizer(db)
        self.rental_assistant = RentalAssistant(db)
    
    def get_recommendations(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get personalized product recommendations."""
        return self.recommendation_engine.get_recommendations(user_id, limit)
    
    def generate_demand_predictions(self, location: str = "Bengaluru", days: int = 7) -> List[Dict]:
        """Generate demand predictions."""
        return self.demand_predictor.generate_predictions(location, days)
    
    def optimize_delivery_routes(self, location: str = "Bengaluru") -> List[Dict]:
        """Optimize delivery routes."""
        return self.delivery_optimizer.optimize_delivery_routes(location)
    
    def process_rental_assistant_query(self, query: str, user_id: str) -> Dict:
        """Process rental assistant query."""
        return self.rental_assistant.process_query(query, user_id)
    
    def get_ai_metrics(self) -> Dict:
        """Get AI system performance metrics."""
        # Calculate recommendation accuracy (placeholder)
        total_recommendations = self.db.query(AIRecommendation).count()
        clicked_recommendations = self.db.query(AIRecommendation).filter(
            AIRecommendation.was_clicked == True
        ).count()
        
        accuracy = (clicked_recommendations / total_recommendations * 100) if total_recommendations > 0 else 0
        
        return {
            "recommendation_accuracy": round(accuracy, 2),
            "total_recommendations": total_recommendations,
            "demand_predictions_generated": self.db.query(DemandPrediction).count(),
            "routes_optimized": self.db.query(Delivery).filter(
                Delivery.optimization_score.isnot(None)
            ).count(),
            "assistant_queries_processed": 0  # Would track in production
        }
```

### Future ML Integration Points

1. **Recommendation Engine**
   - Collaborative filtering with matrix factorization
   - Deep learning for content-based recommendations
   - Reinforcement learning for recommendation optimization

2. **Demand Prediction**
   - LSTM/GRU networks for time-series forecasting
   - XGBoost for feature-based predictions
   - Ensemble methods combining multiple models

3. **Delivery Optimization**
   - Genetic algorithms for complex VRP
   - Reinforcement learning for dynamic routing
   - Graph neural networks for traffic prediction

4. **Rental Assistant**
   - Transformer models (BERT, GPT) for NLP
   - Intent classification with deep learning
   - Dialogue management with reinforcement learning

This AI architecture provides a solid foundation for Quick Tym's intelligent features while maintaining simplicity for MVP implementation.

## Rental Workflow Design

### Complete Rental Lifecycle

Quick Tym implements a comprehensive rental workflow from discovery to return, with precise time-based billing and AI-driven optimizations.

```mermaid
stateDiagram-v2
    [*] --> ProductDiscovery
    ProductDiscovery --> CartAddition : Add to cart
    CartAddition --> BookingCreation : Checkout
    BookingCreation --> DeliveryAssignment : Confirm booking
    
    state DeliveryAssignment {
        [*] --> PartnerSelection
        PartnerSelection --> RouteOptimization
        RouteOptimization --> DeliveryDispatch
        DeliveryDispatch --> ProductDelivery
    }
    
    ProductDelivery --> RentalActive : Timer starts
    RentalActive --> PickupRequested : Customer requests pickup
    PickupRequested --> TimerStopped : Timer stops immediately
    TimerStopped --> BillingCalculation : Calculate charges
    BillingCalculation --> PaymentProcessing : Generate invoice
    PaymentProcessing --> RentalCompleted : Payment successful
    RentalCompleted --> [*]
    
    RentalActive --> ExtensionRequested : Extend rental
    ExtensionRequested --> RentalActive : Timer continues
    
    BookingCreation --> BookingCancelled : Cancel before delivery
    DeliveryAssignment --> DeliveryFailed : Delivery issues
    PaymentProcessing --> PaymentFailed : Payment issues
    
    BookingCancelled --> [*]
    DeliveryFailed --> [*]
    PaymentFailed --> [*]
```

### 1. Product Discovery Phase

#### Search & Filter Flow
```python
# Simplified search flow implementation
class ProductDiscovery:
    def search_products(self, filters: Dict) -> List[Product]:
        """
        Search products with multiple filters:
        - Category (Indoor/Outdoor/Both)
        - Price range (₹50-₹500)
        - Availability status
        - Location (Bengaluru)
        - Search keywords
        """
        query = self.db.query(Product)
        
        # Apply filters
        if filters.get('category'):
            query = query.filter(Product.category == filters['category'])
        
        if filters.get('min_price'):
            query = query.filter(Product.price_per_hour >= filters['min_price'])
        
        if filters.get('max_price'):
            query = query.filter(Product.price_per_hour <= filters['max_price'])
        
        if filters.get('availability') == 'available':
            query = query.join(Inventory).filter(Inventory.available_quantity > 0)
        
        if filters.get('search'):
            search_term = f"%{filters['search']}%"
            query = query.filter(
                Product.name.ilike(search_term) |
                Product.description.ilike(search_term)
            )
        
        # Location filtering (Bengaluru for MVP)
        query = query.join(Inventory).filter(Inventory.location == 'Bengaluru')
        
        return query.all()
    
    def get_product_details(self, product_id: str) -> Dict:
        """Get complete product details with availability."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        inventory = self.db.query(Inventory).filter(
            Inventory.product_id == product_id,
            Inventory.location == 'Bengaluru'
        ).first()
        
        return {
            'product': product,
            'inventory': inventory,
            'availability_status': self._calculate_availability_status(inventory),
            'estimated_delivery_time': self._estimate_delivery_time(product_id)
        }
```

### 2. Booking & Reservation

#### Booking Creation
```python
class BookingSystem:
    def create_booking(self, user_id: str, product_id: str, delivery_address: Dict) -> Booking:
        """Create rental booking with inventory reservation."""
        # Check product availability
        inventory = self._check_availability(product_id, 'Bengaluru')
        if not inventory or inventory.available_quantity <= 0:
            raise ValueError("Product not available")
        
        # Create rental session
        rental = RentalSession(
            user_id=user_id,
            product_id=product_id,
            status='pending',
            delivery_address=delivery_address,
            created_at=datetime.utcnow()
        )
        
        # Reserve inventory
        inventory.available_quantity -= 1
        inventory.reserved_quantity += 1
        
        # Create booking record
        booking = Booking(
            rental_session_id=rental.id,
            scheduled_start=datetime.utcnow() + timedelta(hours=2),  # Default 2 hours for delivery
            status='confirmed',
            created_at=datetime.utcnow()
        )
        
        self.db.add(rental)
        self.db.add(booking)
        self.db.commit()
        
        # Trigger delivery assignment
        self._assign_delivery(rental.id, delivery_address)
        
        return booking
    
    def cancel_booking(self, booking_id: str, reason: str) -> bool:
        """Cancel booking and release inventory."""
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            return False
        
        if booking.status != 'confirmed':
            return False  # Cannot cancel non-confirmed bookings
        
        rental = self.db.query(RentalSession).filter(
            RentalSession.id == booking.rental_session_id
        ).first()
        
        # Release inventory
        inventory = self.db.query(Inventory).filter(
            Inventory.product_id == rental.product_id,
            Inventory.location == 'Bengaluru'
        ).first()
        
        if inventory:
            inventory.available_quantity += 1
            inventory.reserved_quantity -= 1
        
        # Update booking status
        booking.status = 'cancelled'
        booking.cancellation_reason = reason
        booking.updated_at = datetime.utcnow()
        
        self.db.commit()
        return True
```

### 3. Delivery & Pickup Workflow

#### Delivery State Machine
```python
class DeliveryWorkflow:
    """State machine for delivery operations."""
    
    STATES = {
        'pending': ['assigned', 'cancelled'],
        'assigned': ['dispatched', 'cancelled'],
        'dispatched': ['in_transit', 'delayed'],
        'in_transit': ['delivered', 'failed'],
        'delivered': ['completed'],
        'pickup_requested': ['pickup_assigned'],
        'pickup_assigned': ['pickup_in_transit'],
        'pickup_in_transit': ['picked_up', 'pickup_failed'],
        'picked_up': ['completed'],
        'failed': ['retry', 'cancelled'],
        'cancelled': ['closed'],
        'completed': ['closed']
    }
    
    def transition_state(self, delivery_id: str, new_state: str) -> bool:
        """Transition delivery to new state with validation."""
        delivery = self.db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if not delivery:
            return False
        
        # Check valid transition
        valid_transitions = self.STATES.get(delivery.status, [])
        if new_state not in valid_transitions:
            return False
        
        # Perform state-specific actions
        if new_state == 'delivered':
            self._on_delivered(delivery)
        elif new_state == 'picked_up':
            self._on_picked_up(delivery)
        
        # Update state
        delivery.status = new_state
        delivery.updated_at = datetime.utcnow()
        
        # Log state change
        self._log_state_change(delivery_id, delivery.status, new_state)
        
        self.db.commit()
        return True
    
    def _on_delivered(self, delivery: Delivery):
        """Actions when delivery is marked as delivered."""
        # Start rental timer
        rental = self.db.query(RentalSession).filter(
            RentalSession.id == delivery.rental_session_id
        ).first()
        
        if rental:
            rental.status = 'active'
            rental.start_time = datetime.utcnow()
            rental.updated_at = datetime.utcnow()
            
            # Notify customer
            self._send_notification(
                rental.user_id,
                'delivery_completed',
                {'delivery_id': str(delivery.id), 'rental_started': True}
            )
    
    def _on_picked_up(self, delivery: Delivery):
        """Actions when pickup is completed."""
        # Stop rental timer
        rental = self.db.query(RentalSession).filter(
            RentalSession.id == delivery.rental_session_id
        ).first()
        
        if rental and rental.status == 'active':
            rental.status = 'completed'
            rental.end_time = datetime.utcnow()
            rental.total_seconds = int((rental.end_time - rental.start_time).total_seconds())
            rental.updated_at = datetime.utcnow()
            
            # Calculate charges
            rental.total_amount = self._calculate_charges(rental)
            
            # Notify customer
            self._send_notification(
                rental.user_id,
                'pickup_completed',
                {
                    'delivery_id': str(delivery.id),
                    'rental_ended': True,
                    'total_amount': float(rental.total_amount)
                }
            )
```

### 4. Time-Based Billing Engine

#### Precise Timer Implementation
```python
class RentalTimer:
    """Precise time-based billing with 1-second accuracy."""
    
    def __init__(self):
        self.active_timers = {}  # rental_id -> start_time
    
    def start_timer(self, rental_id: str) -> bool:
        """Start rental timer with precise timestamp."""
        if rental_id in self.active_timers:
            return False  # Timer already running
        
        self.active_timers[rental_id] = {
            'start_time': datetime.utcnow(),
            'paused': False,
            'paused_at': None,
            'total_paused_seconds': 0
        }
        
        # Start background thread for this timer
        threading.Thread(
            target=self._timer_thread,
            args=(rental_id,),
            daemon=True
        ).start()
        
        return True
    
    def stop_timer(self, rental_id: str) -> Optional[int]:
        """Stop rental timer and return total seconds."""
        if rental_id not in self.active_timers:
            return None
        
        timer_data = self.active_timers[rental_id]
        end_time = datetime.utcnow()
        
        # Calculate elapsed time
        if timer_data['paused']:
            actual_end = timer_data['paused_at']
        else:
            actual_end = end_time
        
        elapsed = (actual_end - timer_data['start_time']).total_seconds()
        elapsed -= timer_data['total_paused_seconds']
        
        # Remove timer
        del self.active_timers[rental_id]
        
        return int(elapsed)
    
    def pause_timer(self, rental_id: str) -> bool:
        """Pause rental timer."""
        if rental_id not in self.active_timers or self.active_timers[rental_id]['paused']:
            return False
        
        self.active_timers[rental_id]['paused'] = True
        self.active_timers[rental_id]['paused_at'] = datetime.utcnow()
        
        return True
    
    def resume_timer(self, rental_id: str) -> bool:
        """Resume paused rental timer."""
        if rental_id not in self.active_timers or not self.active_timers[rental_id]['paused']:
            return False
        
        timer_data = self.active_timers[rental_id]
        paused_duration = (datetime.utcnow() - timer_data['paused_at']).total_seconds()
        
        timer_data['paused'] = False
        timer_data['paused_at'] = None
        timer_data['total_paused_seconds'] += paused_duration
        
        return True
    
    def get_elapsed_time(self, rental_id: str) -> Optional[int]:
        """Get current elapsed time for active rental."""
        if rental_id not in self.active_timers:
            return None
        
        timer_data = self.active_timers[rental_id]
        
        if timer_data['paused']:
            current_time = timer_data['paused_at']
        else:
            current_time = datetime.utcnow()
        
        elapsed = (current_time - timer_data['start_time']).total_seconds()
        elapsed -= timer_data['total_paused_seconds']
        
        return int(elapsed)
    
    def _timer_thread(self, rental_id: str):
        """Background thread for timer updates."""
        while rental_id in self.active_timers:
            # Update database every 30 seconds
            elapsed = self.get_elapsed_time(rental_id)
            if elapsed:
                self._update_rental_duration(rental_id, elapsed)
            
            time.sleep(30)  # Update interval
```

#### Billing Calculation
```python
class BillingEngine:
    """Calculate rental charges with precise time-based billing."""
    
    def calculate_charges(self, rental: RentalSession, elapsed_seconds: int) -> Decimal:
        """Calculate rental charges based on elapsed time."""
        product = self.db.query(Product).filter(Product.id == rental.product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        # Calculate billable hours (round up to nearest hour)
        billable_hours = self._calculate_billable_hours(elapsed_seconds)
        
        # Ensure minimum billing (1 hour)
        billable_hours = max(1, billable_hours)
        
        # Calculate base amount
        base_amount = Decimal(billable_hours) * product.price_per_hour
        
        # Apply taxes (18% GST for India)
        tax_rate = Decimal("0.18")
        tax_amount = base_amount * tax_rate
        
        # Calculate total
        total_amount = base_amount + tax_amount
        
        # Round to 2 decimal places
        total_amount = total_amount.quantize(Decimal('0.01'))
        
        return total_amount
    
    def _calculate_billable_hours(self, elapsed_seconds: int) -> int:
        """Calculate billable hours from elapsed seconds."""
        # Round up to nearest hour
        hours = (elapsed_seconds + 3599) // 3600  # Ceiling division
        
        # Apply minimum billing rules
        if elapsed_seconds < 3600:  # Less than 1 hour
            hours = 1
        elif elapsed_seconds < 7200:  # 1-2 hours
            hours = 2
        # Continue with other time brackets...
        
        return hours
    
    def generate_invoice(self, rental: RentalSession) -> Dict:
        """Generate detailed invoice for rental."""
        elapsed_seconds = rental.total_seconds or 0
        total_amount = rental.total_amount or self.calculate_charges(rental, elapsed_seconds)
        
        # Calculate billable hours
        billable_hours = self._calculate_billable_hours(elapsed_seconds)
        
        # Get product details
        product = self.db.query(Product).filter(Product.id == rental.product_id).first()
        
        invoice = {
            'invoice_number': f"INV-{rental.id[:8].upper()}",
            'invoice_date': datetime.utcnow().date().isoformat(),
            'customer_id': rental.user_id,
            'rental_period': {
                'start': rental.start_time.isoformat() if rental.start_time else None,
                'end': rental.end_time.isoformat() if rental.end_time else None,
                'total_seconds': elapsed_seconds,
                'formatted_duration': self._format_duration(elapsed_seconds)
            },
            'product_details': {
                'name': product.name if product else 'Unknown',
                'category': product.category if product else 'Unknown',
                'hourly_rate': float(product.price_per_hour) if product else 0.0
            },
            'charges': {
                'billable_hours': billable_hours,
                'hourly_rate': float(product.price_per_hour) if product else 0.0,
                'subtotal': float(Decimal(billable_hours) * product.price_per_hour) if product else 0.0,
                'tax_rate': 18.0,  # GST percentage
                'tax_amount': float(total_amount - (Decimal(billable_hours) * product.price_per_hour)) if product else 0.0,
                'total_amount': float(total_amount)
            },
            'payment_status': 'pending',
            'created_at': datetime.utcnow().isoformat()
        }
        
        return invoice
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in human-readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
```

### 5. Payment Processing Workflow

#### Payment State Machine
```python
class PaymentWorkflow:
    """Payment processing workflow with retry logic."""
    
    def process_payment(self, payment_data: Dict) -> Dict:
        """Process payment with mock gateway for MVP."""
        # Validate payment data
        if not self._validate_payment_data(payment_data):
            return {'status': 'failed', 'error': 'Invalid payment data'}
        
        # Mock payment processing (90% success rate)
        import random
        success = random.random() < 0.9
        
        if success:
            transaction_id = f"TXN-{int(datetime.utcnow().timestamp())}-{random.randint(1000, 9999)}"
            
            return {
                'status': 'success',
                'transaction_id': transaction_id,
                'amount': payment_data['amount'],
                'processed_at': datetime.utcnow().isoformat()
            }
        else:
            # Simulate different failure reasons
            failure_reasons = ['insufficient_funds', 'network_error', 'card_declined']
            reason = random.choice(failure_reasons)
            
            return {
                'status': 'failed',
                'error': reason,
                'retry_allowed': reason != 'card_declined'
            }
    
    def retry_payment(self, payment_id: str, max_retries: int = 2) -> Dict:
        """Retry failed payment with exponential backoff."""
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return {'status': 'failed', 'error': 'Payment not found'}
        
        if payment.retry_count >= max_retries:
            return {'status': 'failed', 'error': 'Max retries exceeded'}
        
        # Increment retry count
        payment.retry_count += 1
        payment.last_retry_at = datetime.utcnow()
        
        # Calculate backoff delay (exponential: 2, 4, 8 minutes...)
        backoff_minutes = 2 ** payment.retry_count
        
        # Schedule retry
        retry_time = datetime.utcnow() + timedelta(minutes=backoff_minutes)
        
        self.db.commit()
        
        return {
            'status': 'scheduled',
            'payment_id': payment_id,
            'retry_count': payment.retry_count,
            'scheduled_for': retry_time.isoformat(),
            'backoff_minutes': backoff_minutes
        }
```

### 6. Exception Handling & Recovery

#### Graceful Degradation
```python
class RentalWorkflowManager:
    """Orchestrate rental workflow with graceful degradation."""
    
    def process_rental_workflow(self, rental_id: str) -> Dict:
        """Process complete rental workflow with error handling."""
        try:
            # Step 1: Validate rental
            rental = self._validate_rental(rental_id)
            
            # Step 2: Process delivery
            delivery_result = self._process_delivery(rental)
            
            # Step 3: Start timer
            timer_result = self._start_rental_timer(rental)
            
            # Step 4: Monitor rental
            monitoring_result = self._monitor_rental(rental)
            
            # Step 5: Process pickup
            pickup_result = self._process_pickup(rental)
            
            # Step 6: Calculate billing
            billing_result = self._calculate_billing(rental)
            
            # Step 7: Process payment
            payment_result = self._process_payment(rental)
            
            return {
                'status': 'completed',
                'steps': {
                    'delivery': delivery_result,
                    'timer': timer_result,
                    'monitoring': monitoring_result,
                    'pickup': pickup_result,
                    'billing': billing_result,
                    'payment': payment_result
                }
            }
            
        except DeliveryException as e:
            # Handle delivery failures
            return self._handle_delivery_failure(rental_id, str(e))
            
        except PaymentException as e:
            # Handle payment failures
            return self._handle_payment_failure(rental_id, str(e))
            
        except Exception as e:
            # General error handling
            return self._handle_general_failure(rental_id, str(e))
    
    def _handle_delivery_failure(self, rental_id: str, error: str) -> Dict:
        """Handle delivery failures with retry logic."""
        # Log failure
        self._log_failure(rental_id, 'delivery', error)
        
        # Attempt to reassign delivery
        reassigned = self._reassign_delivery(rental_id)
        
        if reassigned:
            return {'status': 'recovered', 'action': 'delivery_reassigned'}
        else:
            # Cancel rental and refund if paid
            self._cancel_rental(rental_id)
            return {'status': 'cancelled', 'reason': 'delivery_failed', 'refund_issued': True}
    
    def _handle_payment_failure(self, rental_id: str, error: str) -> Dict:
        """Handle payment failures with retry logic."""
        # Log failure
        self._log_failure(rental_id, 'payment', error)
        
        # Schedule automatic retry
        retry_scheduled = self._schedule_payment_retry(rental_id)
        
        if retry_scheduled:
            return {'status': 'retry_scheduled', 'next_attempt': '2_minutes'}
        else:
            # Mark for manual review
            self._flag_for_review(rental_id)
            return {'status': 'requires_review', 'action': 'manual_intervention'}
```

### 7. Performance Monitoring

#### Workflow Metrics
```python
class WorkflowMetrics:
    """Track and analyze rental workflow performance."""
    
    def calculate_metrics(self, timeframe: str = 'today') -> Dict:
        """Calculate workflow performance metrics."""
        if timeframe == 'today':
            start_date = datetime.utcnow().date()
        elif timeframe == 'week':
            start_date = datetime.utcnow().date() - timedelta(days=7)
        elif timeframe == 'month':
            start_date = datetime.utcnow().date() - timedelta(days=30)
        else:
            start_date = datetime.utcnow().date() - timedelta(days=1)
        
        # Query metrics
        total_rentals = self.db.query(RentalSession).filter(
            RentalSession.created_at >= start_date
        ).count()
        
        completed_rentals = self.db.query(RentalSession).filter(
            RentalSession.created_at >= start_date,
            RentalSession.status == 'completed'
        ).count()
        
        cancelled_rentals = self.db.query(RentalSession).filter(
            RentalSession.created_at >= start_date,
            RentalSession.status == 'cancelled'
        ).count()
        
        avg_rental_duration = self.db.query(
            func.avg(RentalSession.total_seconds)
        ).filter(
            RentalSession.created_at >= start_date,
            RentalSession.status == 'completed',
            RentalSession.total_seconds.isnot(None)
        ).scalar() or 0
        
        success_rate = (completed_rentals / total_rentals * 100) if total_rentals > 0 else 0
        
        # Delivery metrics
        avg_delivery_time = self.db.query(
            func.avg(func.extract('epoch', Delivery.completed_at - Delivery.created_at))
        ).filter(
            Delivery.created_at >= start_date,
            Delivery.status == 'completed'
        ).scalar() or 0
        
        return {
            'timeframe': timeframe,
            'total_rentals': total_rentals,
            'completed_rentals': completed_rentals,
            'cancelled_rentals': cancelled_rentals,
            'success_rate': round(success_rate, 2),
            'avg_rental_duration_seconds': round(avg_rental_duration, 2),
            'avg_rental_duration_formatted': self._format_duration(int(avg_rental_duration)),
            'avg_delivery_time_seconds': round(avg_delivery_time, 2),
            'avg_delivery_time_minutes': round(avg_delivery_time / 60, 2),
            'calculated_at': datetime.utcnow().isoformat()
        }
```

This rental workflow design ensures reliable, time-precise operations with comprehensive error handling and performance monitoring.

## Visual Design System

### Brand Identity & Design Tokens

Quick Tym's visual design embodies an "Urban Tech + Rental" aesthetic with a clean, modern interface that communicates reliability, innovation, and user-friendliness.

#### Color Palette
```typescript
// Design tokens for consistent theming
export const colors = {
  // Primary brand colors
  primary: {
    50: '#f8fafc',
    100: '#f1f5f9',
    200: '#e2e8f0',
    300: '#cbd5e1',
    400: '#94a3b8',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    800: '#1e293b',
    900: '#0F172A', // Brand primary - Dark Blue
  },
  
  accent: {
    50: '#f7fee7',
    100: '#ecfccb',
    200: '#d9f99d',
    300: '#bef264',
    400: '#a3e635', // Brand accent - Lime Green
    500: '#84cc16',
    600: '#65a30d',
    700: '#4d7c0f',
    800: '#3f6212',
    900: '#365314',
  },
  
  secondary: {
    50: '#eff6ff',
    100: '#dbeafe',
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#3b82f6',
    600: '#2563EB', // Brand secondary - Bright Blue
    700: '#1d4ed8',
    800: '#1e40af',
    900: '#1e3a8a',
  },
  
  // Semantic colors
  success: {
    light: '#d1fae5',
    medium: '#10b981',
    dark: '#065f46',
  },
  
  warning: {
    light: '#fef3c7',
    medium: '#f59e0b',
    dark: '#92400e',
  },
  
  error: {
    light: '#fee2e2',
    medium: '#ef4444',
    dark: '#991b1b',
  },
  
  // Neutral colors
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
  
  // Background colors
  background: {
    light: '#ffffff',
    dark: '#0F172A',
    card: '#ffffff',
    cardDark: '#1e293b',
  },
  
  // Text colors
  text: {
    primary: '#0F172A',
    secondary: '#475569',
    disabled: '#94a3b8',
    inverse: '#ffffff',
  },
  
  // Border colors
  border: {
    light: '#e2e8f0',
    medium: '#cbd5e1',
    dark: '#94a3b8',
  },
};

// Accessibility contrast verification
export const contrastRatios = {
  primaryText: 15.8, // #0F172A on white = 15.8:1 (AAA)
  accentText: 4.6,   // #A3E635 on #0F172A = 4.6:1 (AA)
  secondaryText: 7.0, // #2563EB on white = 7.0:1 (AAA)
};
```

#### Typography System
```typescript
export const typography = {
  fontFamily: {
    primary: "'Inter', sans-serif",
    mono: "'JetBrains Mono', 'Courier New', monospace",
  },
  
  fontSize: {
    // Base scale (16px = 1rem)
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
    '5xl': '3rem',     // 48px
  },
  
  fontWeight: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  
  lineHeight: {
    tight: 1.25,
    snug: 1.375,
    normal: 1.5,
    relaxed: 1.625,
    loose: 2,
  },
  
  letterSpacing: {
    tighter: '-0.05em',
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
    wider: '0.05em',
  },
  
  // Responsive type scales
  responsiveScales: {
    mobile: {
      h1: '1.875rem', // 30px
      h2: '1.5rem',   // 24px
      h3: '1.25rem',  // 20px
      body: '1rem',   // 16px
      small: '0.875rem', // 14px
    },
    tablet: {
      h1: '2.25rem',  // 36px
      h2: '1.875rem', // 30px
      h3: '1.5rem',   // 24px
      body: '1rem',   // 16px
      small: '0.875rem', // 14px
    },
    desktop: {
      h1: '3rem',     // 48px
      h2: '2.25rem',  // 36px
      h3: '1.875rem', // 30px
      body: '1.125rem', // 18px
      small: '1rem',  // 16px
    },
  },
};
```

### Component Library

#### Button Components
```typescript
// Button variants with consistent styling
export const buttonStyles = {
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 600,
    borderRadius: '8px',
    border: '1px solid transparent',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    '&:disabled': {
      opacity: 0.5,
      cursor: 'not-allowed',
    },
  },
  
  sizes: {
    sm: {
      padding: '8px 16px',
      fontSize: '0.875rem',
      height: '36px',
    },
    md: {
      padding: '12px 24px',
      fontSize: '1rem',
      height: '44px',
    },
    lg: {
      padding: '16px 32px',
      fontSize: '1.125rem',
      height: '52px',
    },
  },
  
  variants: {
    primary: {
      backgroundColor: colors.accent[400],
      color: colors.primary[900],
      '&:hover': {
        backgroundColor: colors.accent[500],
        transform: 'translateY(-1px)',
      },
      '&:active': {
        transform: 'translateY(0)',
      },
    },
    
    secondary: {
      backgroundColor: colors.secondary[600],
      color: colors.text.inverse,
      '&:hover': {
        backgroundColor: colors.secondary[700],
        transform: 'translateY(-1px)',
      },
    },
    
    outline: {
      backgroundColor: 'transparent',
      color: colors.primary[900],
      borderColor: colors.border.medium,
      '&:hover': {
        backgroundColor: colors.primary[50],
        borderColor: colors.primary[300],
      },
    },
    
    ghost: {
      backgroundColor: 'transparent',
      color: colors.primary[900],
      '&:hover': {
        backgroundColor: colors.primary[50],
      },
    },
    
    danger: {
      backgroundColor: colors.error.medium,
      color: colors.text.inverse,
      '&:hover': {
        backgroundColor: colors.error.dark,
      },
    },
  },
};
```

#### Form Components
```typescript
// Form input styling system
export const formStyles = {
  input: {
    base: {
      width: '100%',
      padding: '12px 16px',
      fontSize: '1rem',
      lineHeight: 1.5,
      color: colors.text.primary,
      backgroundColor: colors.background.light,
      border: `1px solid ${colors.border.medium}`,
      borderRadius: '8px',
      transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
      
      '&:focus': {
        outline: 'none',
        borderColor: colors.accent[400],
        boxShadow: `0 0 0 3px ${colors.accent[100]}`,
      },
      
      '&:disabled': {
        backgroundColor: colors.gray[50],
        cursor: 'not-allowed',
      },
      
      '&::placeholder': {
        color: colors.text.disabled,
      },
    },
    
    sizes: {
      sm: {
        padding: '8px 12px',
        fontSize: '0.875rem',
      },
      lg: {
        padding: '16px 20px',
        fontSize: '1.125rem',
      },
    },
    
    states: {
      error: {
        borderColor: colors.error.medium,
        '&:focus': {
          borderColor: colors.error.medium,
          boxShadow: `0 0 0 3px ${colors.error.light}`,
        },
      },
      
      success: {
        borderColor: colors.success.medium,
        '&:focus': {
          borderColor: colors.success.medium,
          boxShadow: `0 0 0 3px ${colors.success.light}`,
        },
      },
    },
  },
  
  label: {
    base: {
      display: 'block',
      marginBottom: '8px',
      fontSize: '0.875rem',
      fontWeight: 500,
      color: colors.text.secondary,
    },
    
    required: {
      '&::after': {
        content: '"*"',
        marginLeft: '4px',
        color: colors.error.medium,
      },
    },
  },
  
  errorMessage: {
    base: {
      marginTop: '4px',
      fontSize: '0.875rem',
      color: colors.error.medium,
    },
  },
  
  select: {
    base: {
      appearance: 'none',
      backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23475569'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E")`,
      backgroundRepeat: 'no-repeat',
      backgroundPosition: 'right 16px center',
      backgroundSize: '20px',
      paddingRight: '48px',
    },
  },
};
```

#### Card Components
```typescript
// Card design for product listings, rental details, etc.
export const cardStyles = {
  base: {
    backgroundColor: colors.background.card,
    borderRadius: '12px',
    border: `1px solid ${colors.border.light}`,
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    transition: 'box-shadow 0.2s ease, transform 0.2s ease',
    
    '&:hover': {
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      transform: 'translateY(-2px)',
    },
  },
  
  variants: {
    elevated: {
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    },
    
    interactive: {
      cursor: 'pointer',
      '&:active': {
        transform: 'translateY(0)',
      },
    },
    
    compact: {
      padding: '16px',
    },
    
    spacious: {
      padding: '24px',
    },
  },
  
  // Product card specific
  productCard: {
    imageContainer: {
      position: 'relative',
      width: '100%',
      height: '200px',
      overflow: 'hidden',
      borderRadius: '8px',
      backgroundColor: colors.gray[100],
    },
    
    badge: {
      position: 'absolute',
      top: '12px',
      right: '12px',
      padding: '4px 8px',
      fontSize: '0.75rem',
      fontWeight: 600,
      borderRadius: '4px',
      textTransform: 'uppercase',
      
      variants: {
        available: {
          backgroundColor: colors.success.light,
          color: colors.success.dark,
        },
        lowStock: {
          backgroundColor: colors.warning.light,
          color: colors.warning.dark,
        },
        outOfStock: {
          backgroundColor: colors.error.light,
          color: colors.error.dark,
        },
      },
    },
    
    priceTag: {
      display: 'inline-flex',
      alignItems: 'center',
      padding: '4px 8px',
      backgroundColor: colors.accent[100],
      color: colors.primary[900],
      borderRadius: '4px',
      fontSize: '0.875rem',
      fontWeight: 600,
    },
  },
};
```

### Layout System

#### Spacing Scale
```typescript
// 4px base unit spacing system
export const spacing = {
  base: '4px',
  
  // Scale
  0: '0',
  1: '4px',    // 4px
  2: '8px',    // 8px
  3: '12px',   // 12px
  4: '16px',   // 16px
  5: '20px',   // 20px
  6: '24px',   // 24px
  8: '32px',   // 32px
  10: '40px',  // 40px
  12: '48px',  // 48px
  16: '64px',  // 64px
  20: '80px',  // 80px
  24: '96px',  // 96px
  32: '128px', // 128px
  
  // Semantic spacing
  container: {
    padding: '24px',
    margin: '0 auto',
    maxWidth: '1280px',
  },
  
  section: {
    paddingY: '48px',
    paddingX: '24px',
  },
  
  card: {
    padding: '24px',
    gap: '16px',
  },
  
  form: {
    gap: '16px',
    groupGap: '24px',
  },
};
```

#### Grid System
```typescript
// Responsive grid system
export const grid = {
  container: {
    maxWidth: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
    
    padding: {
      mobile: '16px',
      tablet: '24px',
      desktop: '32px',
    },
  },
  
  columns: {
    mobile: 4,
    tablet: 8,
    desktop: 12,
  },
  
  gutters: {
    mobile: '16px',
    tablet: '24px',
    desktop: '32px',
  },
  
  breakpoints: {
    mobile: '320px',
    tablet: '768px',
    desktop: '1024px',
    wide: '1440px',
  },
};
```

### Responsive Design Patterns

#### Mobile-First Media Queries
```typescript
// Responsive utility functions
export const breakpoints = {
  mobile: 320,
  tablet: 768,
  desktop: 1024,
  wide: 1440,
};

export const media = {
  mobile: `@media (min-width: ${breakpoints.mobile}px)`,
  tablet: `@media (min-width: ${breakpoints.tablet}px)`,
  desktop: `@media (min-width: ${breakpoints.desktop}px)`,
  wide: `@media (min-width: ${breakpoints.wide}px)`,
  
  // Mobile-only
  mobileOnly: `@media (max-width: ${breakpoints.tablet - 1}px)`,
  
  // Tablet-only
  tabletOnly: `@media (min-width: ${breakpoints.tablet}px) and (max-width: ${breakpoints.desktop - 1}px)`,
};

// Responsive container component
const Container = styled.div`
  width: 100%;
  margin: 0 auto;
  padding: ${spacing.container.padding};
  
  ${media.tablet} {
    padding: ${spacing[6]};
    max-width: ${grid.container.maxWidth.md};
  }
  
  ${media.desktop} {
    max-width: ${grid.container.maxWidth.lg};
  }
  
  ${media.wide} {
    max-width: ${grid.container.maxWidth.xl};
  }
`;

// Responsive grid component
const ProductGrid = styled.div`
  display: grid;
  gap: ${spacing[4]};
  
  ${media.mobile} {
    grid-template-columns: repeat(2, 1fr);
  }
  
  ${media.tablet} {
    grid-template-columns: repeat(3, 1fr);
    gap: ${spacing[6]};
  }
  
  ${media.desktop} {
    grid-template-columns: repeat(4, 1fr);
  }
`;
```

#### Touch Optimization
```typescript
// Touch-friendly component styles
export const touchOptimization = {
  // Minimum touch target size (44×44px as per WCAG)
  minTouchSize: '44px',
  
  // Touch target expansion
  touchTarget: {
    base: {
      minHeight: '44px',
      minWidth: '44px',
      padding: '12px',
    },
    
    // For smaller elements that need larger touch areas
    expanded: {
      position: 'relative',
      '&::after': {
        content: '""',
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '44px',
        height: '44px',
      },
    },
  },
  
  // Gesture support
  gestures: {
    swipe: {
      '&[data-swipeable="true"]': {
        touchAction: 'pan-y',
        userSelect: 'none',
      },
    },
    
    pinchZoom: {
      '&[data-zoomable="true"]': {
        touchAction: 'manipulation',
      },
    },
  },
  
  // Hover states for touch devices
  hoverStates: {
    // Disable hover effects on touch devices
    '@media (hover: none) and (pointer: coarse)': {
      '&:hover': {
        transform: 'none',
      },
    },
  },
};
```

### Animation & Transitions

#### Motion Design System
```typescript
// Animation timing and easing
export const motion = {
  duration: {
    fast: '150ms',
    normal: '250ms',
    slow: '350ms',
    slower: '500ms',
  },
  
  easing: {
    linear: 'linear',
    ease: 'ease',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    spring: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
  },
  
  // Common animations
  animations: {
    fadeIn: `
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
    `,
    
    slideUp: `
      @keyframes slideUp {
        from { 
          opacity: 0;
          transform: translateY(20px);
        }
        to { 
          opacity: 1;
          transform: translateY(0);
        }
      }
    `,
    
    slideInRight: `
      @keyframes slideInRight {
        from { 
          opacity: 0;
          transform: translateX(20px);
        }
        to { 
          opacity: 1;
          transform: translateX(0);
        }
      }
    `,
    
    pulse: `
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    `,
    
    spin: `
      @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
    `,
  },
  
  // Animation classes
  classes: {
    fadeIn: `
      animation: fadeIn ${motion.duration.normal} ${motion.easing.easeOut};
    `,
    
    slideUp: `
      animation: slideUp ${motion.duration.slow} ${motion.easing.easeOut};
    `,
    
    loading: `
      animation: pulse ${motion.duration.slower} ${motion.easing.easeInOut} infinite;
    `,
  },
};
```

#### Loading States
```typescript
// Skeleton loading components
export const loadingStates = {
  skeleton: {
    base: {
      backgroundColor: colors.gray[200],
      borderRadius: '8px',
      position: 'relative',
      overflow: 'hidden',
      
      '&::after': {
        content: '""',
        position: 'absolute',
        top: 0,
        right: 0,
        bottom: 0,
        left: 0,
        transform: 'translateX(-100%)',
        backgroundImage: `linear-gradient(
          90deg,
          rgba(255, 255, 255, 0) 0,
          rgba(255, 255, 255, 0.2) 20%,
          rgba(255, 255, 255, 0.5) 60%,
          rgba(255, 255, 255, 0)
        )`,
        animation: `${motion.animations.skeletonShine} 2s infinite`,
      },
    },
    
    variants: {
      text: {
        height: '1em',
        width: '100%',
      },
      
      circle: {
        borderRadius: '50%',
        width: '48px',
        height: '48px',
      },
      
      rectangle: {
        width: '100%',
        height: '200px',
      },
      
      card: {
        width: '100%',
        height: '300px',
        borderRadius: '12px',
      },
    },
  },
  
  // Spinner component
  spinner: {
    base: {
      display: 'inline-block',
      border: `3px solid ${colors.gray[200]}`,
      borderTop: `3px solid ${colors.accent[400]}`,
      borderRadius: '50%',
      width: '24px',
      height: '24px',
      animation: `${motion.animations.spin} 1s linear infinite`,
    },
    
    sizes: {
      sm: {
        width: '16px',
        height: '16px',
        borderWidth: '2px',
      },
      lg: {
        width: '32px',
        height: '32px',
        borderWidth: '4px',
      },
    },
  },
};
```

### Iconography

#### Icon System
```typescript
// Icon library and styling
export const icons = {
  sizes: {
    xs: '12px',
    sm: '16px',
    md: '20px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
  },
  
  // Common icon set
  set: {
    // Navigation
    home: '🏠',
    search: '🔍',
    menu: '☰',
    close: '×',
    back: '←',
    
    // Actions
    add: '+',
    remove: '−',
    edit: '✎',
    delete: '🗑',
    share: '↗',
    
    // Status
    check: '✓',
    warning: '⚠',
    error: '✗',
    info: 'ℹ',
    
    // Rental specific
    clock: '⏱',
    location: '📍',
    delivery: '🚚',
    pickup: '📦',
    payment: '💳',
    receipt: '🧾',
    
    // User
    user: '👤',
    settings: '⚙',
    notification: '🔔',
    logout: '↪',
  },
  
  // Styled icon components
  styled: {
    withBadge: {
      position: 'relative',
      
      '&[data-badge]::after': {
        content: 'attr(data-badge)',
        position: 'absolute',
        top: '-4px',
        right: '-4px',
        minWidth: '16px',
        height: '16px',
        padding: '0 4px',
        backgroundColor: colors.error.medium,
        color: colors.text.inverse,
        fontSize: '0.625rem',
        fontWeight: 600,
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      },
    },
    
    interactive: {
      cursor: 'pointer',
      transition: 'color 0.2s ease, transform 0.2s ease',
      
      '&:hover': {
        color: colors.accent[400],
        transform: 'scale(1.1)',
      },
      
      '&:active': {
        transform: 'scale(0.95)',
      },
    },
  },
};
```

### Dark Mode Support

#### Theme Switching
```typescript
// Dark mode theming
export const darkTheme = {
  colors: {
    ...colors,
    background: {
      light: '#0F172A',
      dark: '#020617',
      card: '#1e293b',
      cardDark: '#0f172a',
    },
    
    text: {
      primary: '#f1f5f9',
      secondary: '#cbd5e1',
      disabled: '#64748b',
      inverse: '#0F172A',
    },
    
    border: {
      light: '#334155',
      medium: '#475569',
      dark: '#64748b',
    },
  },
  
  // Dark mode specific overrides
  overrides: {
    card: {
      base: {
        backgroundColor: colors.background.card,
        borderColor: colors.border.light,
        boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2)',
      },
    },
    
    input: {
      base: {
        backgroundColor: colors.gray[800],
        borderColor: colors.border.light,
        color: colors.text.primary,
        
        '&:focus': {
          borderColor: colors.accent[400],
          boxShadow: `0 0 0 3px ${colors.accent[900]}40`,
        },
      },
    },
  },
};

// Theme provider configuration
export const themeConfig = {
  light: colors,
  dark: darkTheme,
  
  // Auto-detect system preference
  autoDetect: true,
  
  // Theme persistence
  storageKey: 'quicktym-theme',
  
  // Theme switch component
  switch: {
    size: 'md',
    iconSize: '20px',
    transition: 'all 0.3s ease',
  },
};
```

This comprehensive visual design system ensures consistent, accessible, and responsive user interfaces across all Quick Tym platforms while maintaining the brand's "Urban Tech + Rental" identity.

## Deployment Architecture

### Development Environment Setup

#### Local Development Configuration
```yaml
# docker-compose.yml - Local development stack
version: '3.8'

services:
  # Frontend - React/Vite
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_BASE_URL=http://localhost:8000/api/v1
      - VITE_WS_URL=ws://localhost:8000/ws
    depends_on:
      - backend
    command: npm run dev

  # Backend - FastAPI
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./database:/data
    environment:
      - DATABASE_URL=sqlite:///data/quick_tym.db
      - DEBUG=True
      - SECRET_KEY=dev-secret-key-change-in-production
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Database - SQLite (development only)
  database:
    image: alpine:latest
    volumes:
      - ./database:/data
    command: sh -c "touch /data/quick_tym.db && tail -f /dev/null"

  # Redis for caching and sessions
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Celery worker for background tasks
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    depends_on:
      - backend
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    command: celery -A app.workers.tasks.celery_app worker --loglevel=info

  # Celery beat for scheduled tasks
  celery_beat:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    depends_on:
      - backend
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    command: celery -A app.workers.tasks.celery_app beat --loglevel=info

volumes:
  redis_data:
```

#### Development Scripts
```bash
#!/bin/bash
# scripts/dev.sh - Development environment setup

echo "Setting up Quick Tym development environment..."

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

# Create environment files
echo "Creating environment files..."
cp .env.example .env.local

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Initialize database
echo "Initializing database..."
docker-compose exec backend python -m app.db.init

# Seed sample data
echo "Seeding sample data..."
docker-compose exec backend python -m app.db.seed

echo "Development environment is ready!"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
```

### Production Deployment Architecture

#### Cloud Infrastructure Design
```mermaid
graph TB
    subgraph "AWS Cloud Infrastructure"
        subgraph "Networking"
            VPC[VPC]
            AZ1[Availability Zone A]
            AZ2[Availability Zone B]
            ALB[Application Load Balancer]
            SG[Security Groups]
        end
        
        subgraph "Frontend Layer"
            S3[S3 Bucket<br/>Static Assets]
            CF[CloudFront<br/>CDN]
            ACM[ACM Certificate]
        end
        
        subgraph "Backend Layer"
            ECS[ECS Fargate Cluster]
            TG1[Target Group<br/>API Service]
            TG2[Target Group<br/>WebSocket]
        end
        
        subgraph "Data Layer"
            RDS[RDS PostgreSQL]
            EC[ElastiCache Redis]
            S3D[S3 for Files]
        end
        
        subgraph "Monitoring"
            CW[CloudWatch]
            XRay[X-Ray Tracing]
            GuardDuty[GuardDuty]
        end
    end
    
    User[User] --> CF
    CF --> S3
    CF --> ALB
    ALB --> TG1
    ALB --> TG2
    TG1 --> ECS
    TG2 --> ECS
    ECS --> RDS
    ECS --> EC
    ECS --> S3D
    ECS --> CW
    ECS --> XRay
```

#### Infrastructure as Code (Terraform)
```hcl
# infra/terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "quicktym-terraform-state"
    key    = "production/terraform.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" {
  region = "ap-south-1" # Mumbai region for India deployment
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "quicktym-vpc"
  }
}

# ECS Cluster for backend services
resource "aws_ecs_cluster" "main" {
  name = "quicktym-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# RDS PostgreSQL Database
resource "aws_db_instance" "main" {
  identifier          = "quicktym-db"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_type        = "gp3"
  
  db_name  = "quicktym"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"
  
  deletion_protection = true
  skip_final_snapshot = false
  
  tags = {
    Name = "quicktym-database"
  }
}

# ElastiCache Redis for caching
resource "aws_elasticache_cluster" "main" {
  cluster_id           = "quicktym-cache"
  engine              = "redis"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  parameter_group_name = "default.redis7"
  port                = 6379
  
  subnet_group_name = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]
  
  tags = {
    Name = "quicktym-redis"
  }
}

# S3 Bucket for frontend static files
resource "aws_s3_bucket" "frontend" {
  bucket = "quicktym-frontend-${var.environment}"
  
  tags = {
    Name = "quicktym-frontend"
  }
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  
  index_document {
    suffix = "index.html"
  }
  
  error_document {
    key = "index.html"
  }
}

# CloudFront CDN
resource "aws_cloudfront_distribution" "frontend" {
  origin {
    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.frontend.id}"
    
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.frontend.cloudfront_access_identity_path
    }
  }
  
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.frontend.id}"
    
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }
  
  price_class = "PriceClass_100" # US/Europe
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = aws_acm_certificate.frontend.arn
    ssl_support_method             = "sni-only"
    minimum_protocol_version       = "TLSv1.2_2021"
  }
  
  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }
  
  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }
}
```

### Containerization Strategy

#### Docker Configuration
```dockerfile
# backend/Dockerfile
FROM python:3.10-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.10-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r quicktym && useradd -r -g quicktym quicktym

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Set permissions
RUN chown -R quicktym:quicktym /app
USER quicktym

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy health check script
COPY healthcheck.sh /healthcheck.sh
RUN chmod +x /healthcheck.sh

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /healthcheck.sh

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### CI/CD Pipeline

#### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy Quick Tym

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: Run backend tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          SECRET_KEY: test-secret-key
          
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          
  build-frontend:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          
      - name: Build frontend
        run: |
          cd frontend
          npm run build
          
      - name: Run frontend tests
        run: |
          cd frontend
          npm test -- --coverage
          
      - name: Upload frontend artifacts
        uses: actions/upload-artifact@v3
        with:
          name: frontend-build
          path: frontend/dist/
          
  build-backend:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
          
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
          
      - name: Build and push backend image
        run: |
          cd backend
          docker build -t ${{ steps.login-ecr.outputs.registry }}/quicktym-backend:latest .
          docker push ${{ steps.login-ecr.outputs.registry }}/quicktym-backend:latest
          
  deploy:
    runs-on: ubuntu-latest
    needs: [build-frontend, build-backend]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
          
      - name: Deploy infrastructure
        run: |
          cd infra/terraform
          terraform init
          terraform plan
          terraform apply -auto-approve
          
      - name: Deploy backend to ECS
        run: |
          aws ecs update-service \
            --cluster quicktym-cluster \
            --service backend-service \
            --force-new-deployment
```

### Database Migration Strategy

#### Alembic Migration Management
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import Base
from app.models import *  # Import all models

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

#### Zero-Downtime Deployment Strategy
```python
# Migration strategy for zero-downtime deployments
class ZeroDowntimeMigration:
    """Implement zero-downtime database migrations."""
    
    def deploy_with_zero_downtime(self, migration_script: str):
        """Execute migration with zero downtime strategy."""
        # Step 1: Deploy new code alongside old code
        self._deploy_parallel_versions()
        
        # Step 2: Run backward-compatible schema changes
        self._apply_backward_compatible_changes(migration_script)
        
        # Step 3: Migrate data in background
        self._migrate_data_background()
        
        # Step 4: Switch traffic to new version
        self._switch_traffic()
        
        # Step 5: Remove old code and incompatible changes
        self._cleanup_old_version()
    
    def _apply_backward_compatible_changes(self, migration_script: str):
        """Apply schema changes that are backward compatible."""
        # Add new columns with NULL default
        # Create new tables
        # Add new indexes (concurrently)
        # These changes don't break existing code
        
        print("Applying backward-compatible schema changes...")
        
        # Example: Adding a new nullable column
        # ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN DEFAULT FALSE;
        
        # Example: Creating a new index concurrently
        # CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);
    
    def _migrate_data_background(self):
        """Migrate data in background without blocking."""
        # Use background jobs to:
        # - Populate new columns
        # - Transform data
        # - Validate consistency
        
        print("Starting background data migration...")
        
        # Example: Populate new column
        # UPDATE users SET phone_verified = TRUE WHERE phone IS NOT NULL;
        
        # Run in batches to avoid locking
        self._migrate_in_batches()
    
    def _switch_traffic(self):
        """Switch traffic from old to new version."""
        print("Switching traffic to new version...")
        
        # Update load balancer configuration
        # Switch feature flags
        # Verify new version is working
    
    def _cleanup_old_version(self):
        """Remove old code and apply breaking changes."""
        print("Cleaning up old version...")
        
        # Now safe to:
        # - Drop old columns
        # - Remove deprecated tables
        # - Apply constraints
        
        # Example: Add NOT NULL constraint after data migration
        # ALTER TABLE users ALTER COLUMN phone_verified SET NOT NULL;
```

### Monitoring & Observability

#### Application Monitoring Stack
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  # Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
  
  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
  
  # Loki for logs
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki-config.yml:/etc/loki/local-config.yml
  
  # Promtail for log collection
  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./monitoring/promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log
    command: -config.file=/etc/promtail/config.yml

volumes:
  prometheus_data:
  grafana_data:
```

#### Key Performance Indicators (KPIs)
```python
# Monitoring metrics and alerts
class PerformanceMonitoring:
    """Monitor system performance and business metrics."""
    
    def collect_metrics(self):
        """Collect key performance indicators."""
        metrics = {
            # System metrics
            'system': {
                'api_response_time_p95': self._get_api_response_time(),
                'error_rate': self._get_error_rate(),
                'uptime': self._get_uptime(),
                'database_connections': self._get_db_connections(),
                'memory_usage': self._get_memory_usage(),
            },
            
            # Business metrics
            'business': {
                'active_rentals': self._get_active_rentals(),
                'daily_revenue': self._get_daily_revenue(),
                'conversion_rate': self._get_conversion_rate(),
                'customer_satisfaction': self._get_customer_satisfaction(),
                'delivery_success_rate': self._get_delivery_success_rate(),
            },
            
            # User metrics
            'user': {
                'active_users': self._get_active_users(),
                'new_registrations': self._get_new_registrations(),
                'session_duration': self._get_session_duration(),
                'feature_adoption': self._get_feature_adoption(),
            },
        }
        
        return metrics
    
    def setup_alerts(self):
        """Configure alerting rules."""
        alerts = [
            {
                'name': 'High Error Rate',
                'condition': 'error_rate > 5%',
                'duration': '5m',
                'severity': 'critical',
                'notification_channels': ['email', 'slack', 'pagerduty'],
            },
            {
                'name': 'Slow API Response',
                'condition': 'api_response_time_p95 > 2s',
                'duration': '10m',
                'severity': 'warning',
                'notification_channels': ['slack'],
            },
            {
                'name': 'Database Connection Exhaustion',
                'condition': 'database_connections > 80%',
                'duration': '5m',
                'severity': 'critical',
                'notification_channels': ['email', 'pagerduty'],
            },
            {
                'name': 'Low Inventory Alert',
                'condition': 'available_products < 10%',
                'duration': '1h',
                'severity': 'warning',
                'notification_channels': ['email'],
            },
        ]
        
        return alerts
```

### Security & Compliance

#### Security Hardening
```python
# Security configuration and hardening
class SecurityConfiguration:
    """Configure security settings for deployment."""
    
    def apply_security_hardening(self):
        """Apply security hardening measures."""
        measures = [
            # Network security
            self._configure_firewall_rules(),
            self._enable_encryption_in_transit(),
            self._setup_vpc_flow_logs(),
            
            # Application security
            self._configure_cors_policy(),
            self._enable_rate_limiting(),
            self._setup_waf_rules(),
            
            # Data security
            self._enable_encryption_at_rest(),
            self._configure_backup_encryption(),
            self._setup_data_retention_policy(),
            
            # Access control
            self._configure_iam_roles(),
            self._enable_multi_factor_auth(),
            self._setup_audit_logging(),
            
            # Compliance
            self._configure_pci_dss_compliance(),
            self._setup_gdpr_compliance(),
            self._enable_vulnerability_scanning(),
        ]
        
        return measures
    
    def _configure_pci_dss_compliance(self):
        """Configure PCI DSS compliance for payment processing."""
        return {
            'network_security': {
                'firewall_configuration': 'enabled',
                'network_segmentation': 'enabled',
                'intrusion_detection': 'enabled',
            },
            'data_protection': {
                'encryption_in_transit': 'TLS 1.3',
                'encryption_at_rest': 'AES-256',
                'key_management': 'AWS KMS',
            },
            'vulnerability_management': {
                'regular_scanning': 'weekly',
                'penetration_testing': 'quarterly',
                'patch_management': 'automated',
            },
            'access_control': {
                'least_privilege': 'enabled',
                'multi_factor_auth': 'required',
                'audit_logging': 'enabled',
            },
        }
```

### Disaster Recovery

#### Backup & Recovery Strategy
```python
class DisasterRecovery:
    """Disaster recovery planning and implementation."""
    
    def create_recovery_plan(self):
        """Create comprehensive disaster recovery plan."""
        plan = {
            'recovery_time_objective': '4 hours',
            'recovery_point_objective': '15 minutes',
            
            'backup_strategy': {
                'database': {
                    'frequency': 'hourly',
                      'retention': '30 days',
                    'encryption': 'AES-256',
                    'storage_location': 'cross-region S3',
                },
                'application': {
                    'frequency': 'daily',
                    'retention': '7 days',
                    'includes': ['code', 'configurations', 'docker_images'],
                },
                'user_data': {
                    'frequency': 'real-time',
                    'retention': '7 years',
                    'compliance': ['GDPR', 'PDPB'],
                },
            },
            
            'recovery_procedures': {
                'database_failure': self._database_recovery_procedure(),
                'application_failure': self._application_recovery_procedure(),
                'region_failure': self._regional_failover_procedure(),
                'security_breach': self._security_incident_procedure(),
            },
            
            'testing_schedule': {
                'backup_restore_test': 'monthly',
                'failover_test': 'quarterly',
                'full_dr_drill': 'biannually',
            },
        }
        
        return plan
    
    def _regional_failover_procedure(self):
        """Procedure for failing over to another AWS region."""
        return [
            '1. Declare disaster and activate DR plan',
            '2. Update DNS to point to secondary region',
            '3. Promote secondary database to primary',
            '4. Launch application stack in secondary region',
            '5. Verify data consistency and application functionality',
            '6. Notify stakeholders of failover completion',
            '7. Monitor secondary region performance',
            '8. Plan and execute failback once primary region is restored',
        ]
```

This deployment architecture provides a robust, scalable, and maintainable infrastructure for Quick Tym with comprehensive monitoring, security, and disaster recovery capabilities.

## Error Handling

### Comprehensive Error Handling Strategy

Quick Tym implements a multi-layered error handling strategy that ensures system resilience, provides clear user feedback, and enables effective debugging while maintaining security.

#### Error Classification
```python
# Error hierarchy and classification
class ErrorClassification:
    """Classify errors by type, severity, and handling strategy."""
    
    ERROR_TYPES = {
        # Client errors (4xx)
        'VALIDATION_ERROR': {
            'status_code': 400,
            'severity': 'low',
            'user_facing': True,
            'retryable': False,
            'logging_level': 'INFO',
        },
        'AUTHENTICATION_ERROR': {
            'status_code': 401,
            'severity': 'medium',
            'user_facing': True,
            'retryable': True,
            'logging_level': 'WARNING',
        },
        'AUTHORIZATION_ERROR': {
            'status_code': 403,
            'severity': 'medium',
            'user_facing': True,
            'retryable': False,
            'logging_level': 'WARNING',
        },
        'NOT_FOUND_ERROR': {
            'status_code': 404,
            'severity': 'low',
            'user_facing': True,
            'retryable': False,
            'logging_level': 'INFO',
        },
        'CONFLICT_ERROR': {
            'status_code': 409,
            'severity': 'medium',
            'user_facing': True,
            'retryable': False,
            'logging_level': 'WARNING',
        },
        
        # Server errors (5xx)
        'INTERNAL_ERROR': {
            'status_code': 500,
            'severity': 'high',
            'user_facing': False,
            'retryable': True,
            'logging_level': 'ERROR',
        },
        'SERVICE_UNAVAILABLE': {
            'status_code': 503,
            'severity': 'high',
            'user_facing': True,
            'retryable': True,
            'logging_level': 'ERROR',
        },
        'DATABASE_ERROR': {
            'status_code': 500,
            'severity': 'critical',
            'user_facing': False,
            'retryable': True,
            'logging_level': 'CRITICAL',
        },
        'NETWORK_ERROR': {
            'status_code': 502,
            'severity': 'high',
            'user_facing': True,
            'retryable': True,
            'logging_level': 'ERROR',
        },
        
        # Business logic errors
        'BUSINESS_RULE_ERROR': {
            'status_code': 422,
            'severity': 'medium',
            'user_facing': True,
            'retryable': False,
            'logging_level': 'WARNING',
        },
        'PAYMENT_ERROR': {
            'status_code': 402,
            'severity': 'high',
            'user_facing': True,
            'retryable': True,
            'logging_level': 'ERROR',
        },
        'DELIVERY_ERROR': {
            'status_code': 424,
            'severity': 'high',
            'user_facing': True,
            'retryable': True,
            'logging_level': 'ERROR',
        },
    }
    
    def classify_error(self, error: Exception) -> dict:
        """Classify error and determine handling strategy."""
        error_name = type(error).__name__
        
        # Map exception types to error classifications
        error_mapping = {
            'ValidationError': 'VALIDATION_ERROR',
            'AuthenticationError': 'AUTHENTICATION_ERROR',
            'AuthorizationError': 'AUTHORIZATION_ERROR',
            'NotFoundError': 'NOT_FOUND_ERROR',
            'ConflictError': 'CONFLICT_ERROR',
            'DatabaseError': 'DATABASE_ERROR',
            'NetworkError': 'NETWORK_ERROR',
            'PaymentError': 'PAYMENT_ERROR',
            'DeliveryError': 'DELIVERY_ERROR',
        }
        
        classification = error_mapping.get(error_name, 'INTERNAL_ERROR')
        return self.ERROR_TYPES.get(classification, self.ERROR_TYPES['INTERNAL_ERROR'])
```

### Structured Error Responses

#### API Error Response Format
```python
# Standardized error response format
def create_error_response(
    error_type: str,
    message: str,
    details: dict = None,
    error_code: str = None,
    request_id: str = None
) -> dict:
    """Create standardized error response for API endpoints."""
    classification = ErrorClassification().ERROR_TYPES.get(
        error_type, 
        ErrorClassification().ERROR_TYPES['INTERNAL_ERROR']
    )
    
    response = {
        'error': {
            'type': error_type,
            'code': error_code or error_type,
            'message': message,
            'status': classification['status_code'],
            'timestamp': datetime.utcnow().isoformat(),
        }
    }
    
    # Add request ID for correlation
    if request_id:
        response['error']['request_id'] = request_id
    
    # Add details if provided
    if details:
        response['error']['details'] = details
    
    # Add user guidance for client errors
    if classification['user_facing']:
        response['error']['user_guidance'] = get_user_guidance(error_type)
    
    # Add retry information if applicable
    if classification['retryable']:
        response['error']['retry_after'] = 60  # seconds
        response['error']['retry_strategy'] = 'exponential_backoff'
    
    return response

def get_user_guidance(error_type: str) -> str:
    """Get user-friendly guidance for different error types."""
    guidance = {
        'VALIDATION_ERROR': 'Please check your input and try again.',
        'AUTHENTICATION_ERROR': 'Please sign in again or check your credentials.',
        'AUTHORIZATION_ERROR': 'You don\'t have permission to perform this action.',
        'NOT_FOUND_ERROR': 'The requested resource was not found.',
        'CONFLICT_ERROR': 'This action conflicts with existing data.',
        'PAYMENT_ERROR': 'Payment failed. Please check your payment details.',
        'DELIVERY_ERROR': 'Delivery could not be completed. Please try again.',
        'SERVICE_UNAVAILABLE': 'Service temporarily unavailable. Please try again later.',
        'NETWORK_ERROR': 'Network connection issue. Please check your connection.',
    }
    
    return guidance.get(error_type, 'An unexpected error occurred. Please try again.')
```

#### Frontend Error Handling
```typescript
// Frontend error handling utilities
class FrontendErrorHandler {
  private errorStore: Error[] = [];
  
  // Handle API errors
  handleApiError(error: AxiosError): void {
    const errorData = error.response?.data;
    
    if (errorData?.error) {
      // Standardized API error
      this.displayUserMessage(errorData.error);
      this.logError(errorData);
      
      // Handle specific error types
      switch (errorData.error.type) {
        case 'AUTHENTICATION_ERROR':
          this.handleAuthError();
          break;
        case 'PAYMENT_ERROR':
          this.handlePaymentError(errorData.error.details);
          break;
        case 'VALIDATION_ERROR':
          this.handleValidationError(errorData.error.details);
          break;
        default:
          this.handleGenericError(errorData.error);
      }
    } else {
      // Network or unknown error
      this.handleNetworkError(error);
    }
  }
  
  private displayUserMessage(error: any): void {
    const message = error.user_guidance || error.message || 'An error occurred';
    
    // Show toast notification
    toast.error(message, {
      position: 'top-right',
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
    });
    
    // Update UI state if needed
    if (error.type === 'VALIDATION_ERROR') {
      this.highlightInvalidFields(error.details);
    }
  }
  
  private handleAuthError(): void {
    // Clear authentication state
    authStore.clear();
    
    // Redirect to login
    router.navigate('/auth/login');
    
    // Show login prompt
    toast.info('Please sign in again to continue', {
      autoClose: 3000,
    });
  }
  
  private handlePaymentError(details: any): void {
    // Update payment form state
    paymentForm.setErrors({
      general: 'Payment failed. Please check your details.',
    });
    
    // Enable retry button
    paymentStore.setRetryAllowed(true);
  }
  
  private handleValidationError(details: any): void {
    // Map validation errors to form fields
    const fieldErrors = this.mapValidationErrors(details);
    
    // Update form state
    currentForm.setErrors(fieldErrors);
    
    // Scroll to first error
    this.scrollToFirstError(fieldErrors);
  }
  
  private handleNetworkError(error: AxiosError): void {
    // Check if offline
    if (!navigator.onLine) {
      toast.error('You are offline. Please check your connection.', {
        autoClose: false,
      });
      
      // Enable offline mode
      appStore.setOfflineMode(true);
    } else {
      toast.error('Network error. Please try again.', {
        autoClose: 5000,
      });
    }
    
    // Log error for debugging
    console.error('Network error:', error);
  }
}
```

### Graceful Degradation

#### Fallback Mechanisms
```python
# Graceful degradation implementation
class GracefulDegradation:
    """Implement graceful degradation for critical failures."""
    
    def __init__(self):
        self.fallback_strategies = {
            'database': self._database_fallback,
            'payment_gateway': self._payment_fallback,
            'ai_services': self._ai_services_fallback,
            'delivery_service': self._delivery_fallback,
            'notification_service': self._notification_fallback,
        }
    
    def handle_failure(self, component: str, error: Exception, context: dict):
        """Handle component failure with graceful degradation."""
        strategy = self.fallback_strategies.get(component)
        
        if not strategy:
            return self._generic_fallback(error, context)
        
        try:
            return strategy(error, context)
        except Exception as fallback_error:
            # Even fallback failed, use last resort
            return self._last_resort_fallback(error, context)
    
    def _database_fallback(self, error: Exception, context: dict):
        """Fallback for database failures."""
        # Use read replicas if available
        if self._has_read_replica():
            return self._switch_to_read_replica()
        
        # Use cached data
        if self._has_cached_data(context):
            return self._use_cached_data(context)
        
        # Return stale data with warning
        return {
            'data': self._get_stale_data(context),
            'warning': 'Showing cached data due to database issues',
            'degraded': True,
        }
    
    def _payment_fallback(self, error: Exception, context: dict):
        """Fallback for payment gateway failures."""
        # Queue payment for later processing
        payment_id = context.get('payment_id')
        
        if payment_id:
            self._queue_payment(payment_id)
            
            return {
                'status': 'queued',
                'message': 'Payment will be processed shortly',
                'payment_id': payment_id,
                'degraded': True,
            }
        
        # Suggest alternative payment methods
        return {
            'status': 'failed',
            'message': 'Payment temporarily unavailable',
            'alternatives': ['cash_on_delivery', 'later_payment'],
            'degraded': True,
        }
    
    def _ai_services_fallback(self, error: Exception, context: dict):
        """Fallback for AI service failures."""
        service_type = context.get('service_type', 'recommendation')
        
        if service_type == 'recommendation':
            # Return popular items instead of personalized recommendations
            return {
                'recommendations': self._get_popular_items(),
                'warning': 'Showing popular items due to technical issues',
                'degraded': True,
            }
        elif service_type == 'demand_prediction':
            # Use historical averages
            return {
                'predictions': self._get_historical_averages(),
                'warning': 'Using historical data for predictions',
                'degraded': True,
            }
        
        return self._generic_fallback(error, context)
    
    def _delivery_fallback(self, error: Exception, context: dict):
        """Fallback for delivery service failures."""
        # Use simple assignment instead of optimized routing
        delivery_id = context.get('delivery_id')
        
        if delivery_id:
            simple_assignment = self._assign_delivery_simple(delivery_id)
            
            return {
                'assignment': simple_assignment,
                'warning': 'Using simple delivery assignment',
                'estimated_time': 'Longer than usual',
                'degraded': True,
            }
        
        return self._generic_fallback(error, context)
```

### Circuit Breaker Pattern

#### Resilient Service Integration
```python
# Circuit breaker implementation
class CircuitBreaker:
    """Implement circuit breaker pattern for external service calls."""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.failure_count = 0
        self.last_failure_time = None
        self.service_name = None
    
    def execute(self, service_call, *args, **kwargs):
        """Execute service call with circuit breaker protection."""
        self.service_name = service_call.__name__
        
        # Check circuit state
        if self.state == 'OPEN':
            if self._should_try_recovery():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenError(
                    f"Circuit breaker OPEN for {self.service_name}. "
                    f"Next retry in {self._time_to_recovery()} seconds."
                )
        
        try:
            # Execute service call
            result = service_call(*args, **kwargs)
            
            # Success - reset circuit if needed
            if self.state == 'HALF_OPEN':
                self._reset_circuit()
            
            return result
            
        except Exception as error:
            # Failure - update circuit state
            self._handle_failure(error)
            
            # Re-raise the error
            raise
    
    def _handle_failure(self, error: Exception):
        """Handle service failure and update circuit state."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        # Log failure
        self._log_failure(error)
        
        # Check if threshold reached
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
            self._log_circuit_opened()
    
    def _should_try_recovery(self) -> bool:
        """Check if recovery should be attempted."""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout
    
    def _time_to_recovery(self) -> int:
        """Calculate time until next recovery attempt."""
        if not self.last_failure_time:
            return 0
        
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        time_left = max(0, self.recovery_timeout - elapsed)
        
        return int(time_left)
    
    def _reset_circuit(self):
        """Reset circuit to CLOSED state."""
        self.state = 'CLOSED'
        self.failure_count = 0
        self.last_failure_time = None
        self._log_circuit_reset()
    
    def get_status(self) -> dict:
        """Get current circuit breaker status."""
        return {
            'service': self.service_name,
            'state': self.state,
            'failure_count': self.failure_count,
            'last_failure': self.last_failure_time.isoformat() if self.last_failure_time else None,
            'time_to_recovery': self._time_to_recovery(),
        }

# Usage example
payment_circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

def process_payment_with_circuit_breaker(payment_data: dict):
    """Process payment with circuit breaker protection."""
    return payment_circuit_breaker.execute(
        payment_gateway.process,
        payment_data
    )
```

### Retry Mechanisms

#### Intelligent Retry Strategies
```python
# Retry with exponential backoff and jitter
class RetryManager:
    """Manage retry logic with exponential backoff and jitter."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        jitter: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
    
    def execute_with_retry(
        self,
        operation,
        *args,
        retry_on_exceptions: tuple = None,
        **kwargs
    ):
        """Execute operation with retry logic."""
        retry_on_exceptions = retry_on_exceptions or (Exception,)
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    self._log_retry_attempt(attempt, operation.__name__)
                
                return operation(*args, **kwargs)
                
            except retry_on_exceptions as error:
                last_exception = error
                
                # Check if we should retry
                if not self._should_retry(error, attempt):
                    break
                
                # Calculate delay with exponential backoff and jitter
                delay = self._calculate_delay(attempt)
                
                # Wait before retry
                self._wait(delay)
        
        # All retries failed
        raise MaxRetriesExceededError(
            f"Operation '{operation.__name__}' failed after {self.max_retries} retries",
            last_exception
        )
    
    def _should_retry(self, error: Exception, attempt: int) -> bool:
        """Determine if operation should be retried."""
        # Don't retry if max retries reached
        if attempt >= self.max_retries:
            return False
        
        # Check error type for retryability
        error_type = type(error).__name__
        
        retryable_errors = [
            'NetworkError',
            'TimeoutError',
            'ConnectionError',
            'ServiceUnavailableError',
            'RateLimitError',
        ]
        
        non_retryable_errors = [
            'ValidationError',
            'AuthenticationError',
            'AuthorizationError',
            'InvalidInputError',
        ]
        
        if error_type in non_retryable_errors:
            return False
        
        # Check for specific error codes or messages
        error_message = str(error).lower()
        
        if 'permanent' in error_message or 'fatal' in error_message:
            return False
        
        if 'retry' in error_message or 'temporary' in error_message:
            return True
        
        # Default: retry for network and server errors
        return error_type in retryable_errors
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and optional jitter."""
        # Exponential backoff: base_delay * 2^attempt
        delay = self.base_delay * (2 ** attempt)
        
        # Cap at max_delay
        delay = min(delay, self.max_delay)
        
        # Add jitter (random variation)
        if self.jitter:
            jitter_amount = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
            delay = max(0.1, delay)  # Ensure positive delay
        
        return delay
    
    def _wait(self, delay: float):
        """Wait for specified delay."""
        time.sleep(delay)

# Usage example
retry_manager = RetryManager(max_retries=3, base_delay=1.0)

def send_notification_with_retry(user_id: str, notification: dict):
    """Send notification with automatic retry on failure."""
    return retry_manager.execute_with_retry(
        notification_service.send,
        user_id,
        notification,
        retry_on_exceptions=(NetworkError, TimeoutError)
    )
```

### Error Monitoring & Alerting

#### Real-time Error Tracking
```python
# Error monitoring and alerting system
class ErrorMonitor:
    """Monitor errors and trigger alerts based on thresholds."""
    
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.error_timestamps = defaultdict(list)
        self.alert_thresholds = {
            'critical': {'count': 10, 'window': 60},  # 10 errors in 60 seconds
            'high': {'count': 50, 'window': 300},     # 50 errors in 5 minutes
            'medium': {'count': 100, 'window': 1800}, # 100 errors in 30 minutes
        }
        self.active_alerts = set()
    
    def track_error(self, error_type: str, context: dict = None):
        """Track error occurrence and check for alert conditions."""
        timestamp = datetime.utcnow()
        
        # Update error counts
        self.error_counts[error_type] += 1
        self.error_timestamps[error_type].append(timestamp)
        
        # Clean old timestamps
        self._clean_old_timestamps(error_type)
        
        # Check alert conditions
        self._check_alerts(error_type, context)
        
        # Log error for monitoring
        self._log_error(error_type, context, timestamp)
    
    def _check_alerts(self, error_type: str, context: dict):
        """Check if error thresholds have been exceeded."""
        timestamps = self.error_timestamps[error_type]
        
        for severity, threshold in self.alert_thresholds.items():
            # Count errors in time window
            window_start = datetime.utcnow() - timedelta(seconds=threshold['window'])
            recent_errors = sum(1 for ts in timestamps if ts >= window_start)
            
            if recent_errors >= threshold['count']:
                alert_key = f"{error_type}_{severity}"
                
                if alert_key not in self.active_alerts:
                    self._trigger_alert(error_type, severity, recent_errors, context)
                    self.active_alerts.add(alert_key)
    
    def _trigger_alert(self, error_type: str, severity: str, count: int, context: dict):
        """Trigger alert for error threshold exceeded."""
        alert = {
            'type': 'error_threshold_exceeded',
            'severity': severity,
            'error_type': error_type,
            'error_count': count,
            'timestamp': datetime.utcnow().isoformat(),
            'context': context or {},
        }
        
        # Send alert to different channels based on severity
        if severity == 'critical':
            self._send_critical_alert(alert)
        elif severity == 'high':
            self._send_high_alert(alert)
        else:
            self._send_medium_alert(alert)
        
        # Log alert
        self._log_alert(alert)
    
    def _send_critical_alert(self, alert: dict):
        """Send critical alert (immediate attention required)."""
        # Page on-call engineer
        pagerduty_client.create_incident(
            title=f"CRITICAL: {alert['error_type']} threshold exceeded",
            details=alert,
            urgency='high'
        )
        
        # Send SMS
        sms_client.send(
            to=on_call_phone_number,
            message=f"CRITICAL ALERT: {alert['error_type']} - {alert['error_count']} errors"
        )
        
        # Post to Slack emergency channel
        slack_client.post_message(
            channel='#alerts-critical',
            text=f"🚨 CRITICAL: {alert['error_type']} - {alert['error_count']} errors"
        )
    
    def get_error_metrics(self, time_window: int = 3600) -> dict:
        """Get error metrics for specified time window."""
        window_start = datetime.utcnow() - timedelta(seconds=time_window)
        
        metrics = {
            'window_seconds': time_window,
            'total_errors': 0,
            'error_types': {},
            'error_rate_per_minute': 0,
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        for error_type, timestamps in self.error_timestamps.items():
            recent_errors = [ts for ts in timestamps if ts >= window_start]
            
            if recent_errors:
                metrics['error_types'][error_type] = {
                    'count': len(recent_errors),
                    'first_error': min(recent_errors).isoformat(),
                    'last_error': max(recent_errors).isoformat(),
                }
                metrics['total_errors'] += len(recent_errors)
        
        # Calculate error rate
        minutes_in_window = time_window / 60
        if minutes_in_window > 0:
            metrics['error_rate_per_minute'] = metrics['total_errors'] / minutes_in_window
        
        return metrics
```

### User Experience During Errors

#### User-Friendly Error States
```typescript
// User-friendly error components
const ErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [hasError, setHasError] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      setHasError(true);
      setError(event.error);
      
      // Log error
      errorLogger.logFrontendError(event.error);
    };

    window.addEventListener('error', handleError);
    
    return () => {
      window.removeEventListener('error', handleError);
    };
  }, []);

  if (hasError) {
    return <ErrorDisplay error={error} />;
  }

  return <>{children}</>;
};

const ErrorDisplay: React.FC<{ error: Error | null }> = ({ error }) => {
  const [showDetails, setShowDetails] = useState(false);
  
  const getErrorType = () => {
    if (!error) return 'Unknown Error';
    
    if (error.message.includes('network')) return 'Network Error';
    if (error.message.includes('auth')) return 'Authentication Error';
    if (error.message.includes('payment')) return 'Payment Error';
    
    return 'Application Error';
  };
  
  const getRecoverySteps = () => {
    const errorType = getErrorType();
    
    switch (errorType) {
      case 'Network Error':
        return [
          'Check your internet connection',
          'Try refreshing the page',
          'If using mobile data, try switching to Wi-Fi',
        ];
      case 'Authentication Error':
        return [
          'Sign out and sign back in',
          'Clear browser cookies and cache',
          'Try a different browser',
        ];
      case 'Payment Error':
        return [
          'Check your payment details',
          'Try a different payment method',
          'Contact your bank if issue persists',
        ];
      default:
        return [
          'Refresh the page',
          'Clear browser cache',
          'Try again in a few minutes',
          'Contact support if issue persists',
        ];
    }
  };
  
  return (
    <div className="error-container">
      <div className="error-icon">
        <Icon name="warning" size="xl" />
      </div>
      
      <h1 className="error-title">Something went wrong</h1>
      <p className="error-message">
        We encountered a {getErrorType().toLowerCase()}. Don't worry, your data is safe.
      </p>
      
      <div className="recovery-steps">
        <h3>Try these steps:</h3>
        <ul>
          {getRecoverySteps().map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ul>
      </div>
      
      <div className="error-actions">
        <Button
          variant="primary"
          onClick={() => window.location.reload()}
        >
          Refresh Page
        </Button>
        
        <Button
          variant="outline"
          onClick={() => router.navigate('/')}
        >
          Go to Home
        </Button>
        
        <Button
          variant="ghost"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Hide Details' : 'Show Details'}
        </Button>
      </div>
      
      {showDetails && error && (
        <div className="error-details">
          <h4>Technical Details</h4>
          <pre>{error.toString()}</pre>
          <p className="error-id">
            Error ID: {generateErrorId(error)}
          </p>
          <Button
            variant="link"
            onClick={() => copyToClipboard(generateErrorId(error))}
          >
            Copy Error ID
          </Button>
        </div>
      )}
      
      <div className="support-contact">
        <p>
          Still having issues?{' '}
          <Link to="/support">Contact Support</Link>
        </p>
      </div>
    </div>
  );
};
```

This comprehensive error handling strategy ensures Quick Tym maintains high availability, provides clear user feedback, and enables efficient debugging while protecting sensitive information and maintaining system security.