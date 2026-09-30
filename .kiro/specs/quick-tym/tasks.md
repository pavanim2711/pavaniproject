# Implementation Plan: Quick Tym Rental MVP

## Overview

Implement a full-stack AI-powered rental web application with time-based billing, three user roles (Customer, Delivery Partner, Admin), and intelligent features. The MVP will enable the demo scenario: Customer Pavani in Bengaluru renting a picnic mat for a picnic with 5 friends. The system uses React + TypeScript frontend, FastAPI Python backend, SQLite database, and rule-based AI services.

## Tasks

### P0: Project Foundation and Setup

- [ ] 1. Initialize project structure and development environment
  - [ ] 1.1 Set up project directories with frontend/, backend/, api/, database/ separation
    - Create root README.md with setup instructions
    - Initialize Git repository with .gitignore for Python/Node projects
    - Set up environment configuration (.env.example files)
    - _Requirements: 14.1, 14.2, 14.3, 14.4_
  
  - [ ] 1.2 Configure frontend development environment
    - Initialize React + Vite + TypeScript project in frontend/
    - Install required dependencies: react-router, axios, styled-components, react-query
    - Configure TypeScript with strict mode and path aliases
    - Set up Vite development server on localhost:5173
    - _Requirements: 14.1, 11.1, 11.2_

  - [ ] 1.3 Configure backend development environment
    - Initialize FastAPI Python project in backend/ with virtual environment
    - Install dependencies: fastapi, sqlalchemy, pydantic, python-jose, bcrypt
    - Configure FastAPI with automatic OpenAPI documentation at /docs and /redoc
    - Set up SQLite database connection and Alembic for migrations
    - _Requirements: 14.2, 13.1, 13.2_

  - [x] 1.4 Set up testing frameworks
    - Configure pytest for backend testing with coverage reporting
    - Set up Vitest for frontend testing with React Testing Library
    - Create basic test configuration and example tests
    - _Requirements: 14.5_

- [ ] 2. Checkpoint - Development environment verification
  - Ensure frontend and backend start successfully, ask the user if questions arise.

### P0: Database Schema and Core Models

- [ ] 3. Implement database schema and models
  - [ ] 3.1 Create SQLAlchemy ORM models for all 15 tables
    - Implement User, Product, Category, Inventory models
    - Implement RentalSession, Booking, Payment models
    - Implement Delivery, DeliveryTask, PickupRequest models
    - Implement Review, Notification, AIRecommendation, DemandPrediction models
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 3.2 Define database relationships and constraints
    - Set up foreign key relationships with appropriate cascade rules
    - Implement business logic constraints in models (price ranges, status transitions)
    - Add database indexes for performance optimization
    - _Requirements: 13.2, 13.4, 13.5_

  - [x] 3.3 Write property tests for data models
    - **Property 1: User role validation** - Only Customer, Delivery_Partner, or Admin roles allowed
    - **Property 2: Product price bounds** - Price must be between ₹50 and ₹500 per hour
    - **Validates: Requirements 1.3, 2.1**

  - [ ] 3.3 Create Alembic migration scripts
    - Generate initial migration for all 15 tables
    - Create seed data script for Bengaluru launch (10 products, sample users)
    - Add migration rollback capability
    - _Requirements: 13.1, 13.3_

### P0: Authentication and Authorization System

- [ ] 4. Implement user authentication and role-based access control
  - [ ] 4.1 Create User registration and login endpoints
    - Implement /api/v1/auth/register endpoint with validation
    - Implement /api/v1/auth/login endpoint with JWT token generation
    - Set up password hashing with bcrypt and secure password validation
    - _Requirements: 1.1, 1.2, 1.4_

  - [ ] 4.2 Implement JWT authentication middleware
    - Create JWT token validation with 24-hour expiration
    - Implement role extraction and permission checking
    - Set up token refresh mechanism
    - _Requirements: 1.3, 1.5_

  - [x] 4.3 Write property tests for authentication
    - **Property 3: JWT token integrity** - Tokens cannot be tampered with without detection
    - **Property 4: Role-based access control** - Users can only access endpoints allowed for their role
    - **Validates: Requirements 1.3, 1.5**

  - [ ] 4.4 Create frontend authentication context and services
    - Implement React AuthContext with login/logout functionality
    - Create axios interceptors for adding JWT tokens to requests
    - Implement protected route components for different user roles
    - _Requirements: 1.3, 11.2_

### P1: Product Catalog and Discovery

- [ ] 5. Implement product browsing and search functionality
  - [ ] 5.1 Create product API endpoints
    - Implement GET /api/v1/products with filtering (category, price range, availability)
    - Implement GET /api/v1/products/{id} for detailed product view
    - Add product search endpoint with relevance scoring
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ] 5.2 Build frontend product discovery interface
    - Create ProductGrid component with responsive product cards
    - Implement search bar with auto-suggest functionality
    - Build filter sidebar for category, price, and availability filtering
    - Add pagination for large product catalogs
    - _Requirements: 2.2, 2.3, 11.1, 11.2_

  - [x] 5.3 Write integration tests for product discovery
    - Test search relevance scoring with various query types
    - Test filtering combinations and edge cases
    - Test pagination performance with large datasets
    - _Requirements: 2.3_

- [ ] 6. Checkpoint - Product catalog functionality
  - Ensure products can be discovered, searched, and filtered, ask the user if questions arise.

### P1: Time-Based Rental System Core

- [ ] 7. Implement rental session management
  - [ ] 7.1 Create rental booking endpoints
    - Implement POST /api/v1/rentals to create new rental sessions
    - Add rental validation (product availability, user eligibility)
    - Generate booking confirmation with reference numbers
    - _Requirements: 4.1, 4.5_

  - [ ] 7.2 Implement real-time rental timer service
    - Create Timer service with 1-second precision tracking
    - Implement timer start on delivery confirmation
    - Implement timer stop on pickup request (immediate stop)
    - Add WebSocket broadcasting for real-time timer updates
    - _Requirements: 4.2, 4.3, 6.1_

  - [x] 7.3 Write property tests for rental timing
    - **Property 5: Timer stop precision** - Timer must stop within 1 second of pickup request
    - **Property 6: Billing accuracy** - Charges must equal elapsed_time × hourly_rate with 1-second precision
    - **Validates: Requirements 4.3, 6.5**

  - [ ] 7.4 Create rental billing calculation service
    - Implement billing calculation with minimum 1-hour charge
    - Add rounding rules (round up to nearest whole minute/hour)
    - Create itemized invoice generation
    - _Requirements: 4.4, 4.6, 6.2, 6.3, 6.4, 6.6_

### P1: Delivery and Pickup Workflow

- [ ] 8. Implement delivery assignment and tracking
  - [ ] 8.1 Create delivery assignment service
    - Implement AI_Assignment_Optimizer with rule-based logic
    - Consider partner rating (>4.0), current load (<3 deliveries), proximity (<5km)
    - Add delivery batching for efficiency (k-means clustering)
    - _Requirements: 5.1, 5.2, 5.5_

  - [ ] 8.2 Build delivery tracking endpoints
    - Implement delivery status updates (pending → assigned → in_transit → delivered)
    - Add delivery confirmation with photo evidence and signature
    - Create pickup request handling with immediate timer stop
    - _Requirements: 5.3, 5.4_

  - [x] 8.3 Write property tests for delivery optimization
    - **Property 7: Partner assignment fairness** - Higher-rated partners get priority when equally qualified
    - **Property 8: Proximity optimization** - Nearest available partner within 5km gets assignment
    - **Validates: Requirements 5.1, 5.2**

  - [ ] 8.4 Create delivery partner frontend interface
    - Build delivery dashboard with assigned tasks
    - Implement task status updates with photo upload
    - Add map integration for route visualization
    - _Requirements: 5.3, 5.4_

### P1: Payment Processing System

- [ ] 9. Implement secure payment processing
  - [ ] 9.1 Create mock payment processor
    - Implement payment validation (card number Luhn check, expiry date)
    - Add simulated authorization (90% success, 5% insufficient funds, 5% network error)
    - Implement retry logic with exponential backoff
    - _Requirements: 7.1, 7.2, 7.3_

  - [ ] 9.2 Build payment endpoints and invoice generation
    - Implement POST /api/v1/payments for payment processing
    - Create invoice generation with mandatory fields
    - Add OTP verification for payments over ₹5000
    - _Requirements: 7.4, 7.5, 7.6_

  - [x] 9.3 Write property tests for payment security
    - **Property 9: Payment idempotency** - Same payment request processed twice results in same outcome
    - **Property 10: Transaction integrity** - Payment amount cannot be altered during processing
    - **Validates: Requirements 7.2, 7.4**

  - [ ] 9.4 Create frontend payment interface
    - Build secure payment form with validation
    - Implement OTP verification flow
    - Add payment status tracking and receipt display
    - _Requirements: 7.1, 7.5_

- [ ] 10. Checkpoint - Core rental workflow
  - Ensure complete rental flow works (discover → book → deliver → use → pickup → bill), ask the user if questions arise.

### P2: AI-Powered Features Implementation

- [ ] 11. Implement AI recommendation engine
  - [ ] 11.1 Create rule-based recommendation service
    - Analyze rental history, browsing behavior, and ratings
    - Generate affinity scores (0-100) for product categories
    - Implement fallback to popular products for new users
    - _Requirements: 3.1, 3.2, 3.3, 3.5_

  - [ ] 11.2 Build recommendation API endpoints
    - Implement GET /api/v1/ai/recommendations with personalized suggestions
    - Add relevance scoring (confidence: 70-100%) and categorization
    - Ensure response within 500ms with timeout fallback
    - _Requirements: 3.2, 3.4_

  - [x] 11.3 Write property tests for recommendations
    - **Property 11: Recommendation relevance** - Recommended products match user's historical preferences
    - **Property 12: Fallback mechanism** - New users receive popular products as recommendations
    - **Validates: Requirements 3.1, 3.5**

  - [ ] 11.4 Create frontend recommendation display
    - Build "Recommended for You" section on homepage
    - Implement recommendation carousel with reasoning display
    - Add click tracking for CTR measurement
    - _Requirements: 3.2, 3.6_

- [ ] 12. Implement demand prediction system
  - [ ] 12.1 Create time-series forecasting service
    - Analyze 30+ days of historical rental data
    - Implement ARIMA or Prophet model for 7-day forecasts
    - Consider seasonal patterns and local events
    - _Requirements: 8.1, 8.3_

  - [ ] 12.2 Build demand prediction endpoints and alerts
    - Implement daily prediction updates at 2:00 AM
    - Add confidence intervals (80% confidence band)
    - Create alert system for predicted demand >50% above inventory
    - _Requirements: 8.2, 8.4, 8.6_

  - [x] 12.3 Write property tests for predictions
    - **Property 13: Prediction consistency** - Same input data produces same predictions
    - **Property 14: Alert accuracy** - Alerts trigger when predicted_demand > 1.5 × current_inventory
    - **Validates: Requirements 8.5, 8.6**

### P2: Rental Assistant and User Support

- [ ] 13. Implement AI rental assistant
  - [ ] 13.1 Create rule-based assistant service
    - Implement question answering about product suitability, duration, pricing
    - Maintain conversation context for 30 minutes
    - Add confidence scoring with human escalation (score < 60%)
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

  - [ ] 13.2 Build assistant API and frontend interface
    - Implement WebSocket endpoint for real-time assistant conversations
    - Create chat interface with message history
    - Add product availability lookups during conversations
    - _Requirements: 9.1, 9.5_

  - [x] 13.3 Write property tests for assistant accuracy
    - **Property 15: Response relevance** - Assistant answers must relate to product rental queries
    - **Property 16: Escalation correctness** - Low confidence questions (<60%) trigger human escalation
    - **Validates: Requirements 9.4, 9.6**

### P2: Admin Dashboard and Management

- [ ] 14. Implement comprehensive admin interface
  - [ ] 14.1 Create admin dashboard with metrics
    - Implement real-time metrics (rentals, revenue, user activity)
    - Add 5-minute refresh intervals for live updates
    - Create data visualizations with charts and graphs
    - _Requirements: 10.1_

  - [ ] 14.2 Build user and product management tools
    - Implement user account suspension/removal with audit logging
    - Create product CRUD with validation (price: ₹50-₹500, stock: 0-100)
    - Add bulk import/export capability (CSV format)
    - _Requirements: 10.2, 10.3, 10.4_

  - [x] 14.3 Write integration tests for admin functionality
    - Test two-person rule enforcement for critical operations
    - Test audit logging completeness for all admin actions
    - Test bulk operations performance and validation
    - _Requirements: 10.5_

### P2: Brand Identity and Responsive UI

- [ ] 15. Implement branded user interface
  - [ ] 15.1 Apply Quick Tym visual theme
    - Implement brand colors (#0F172A, #A3E635, #2563EB) with accessibility compliance
    - Create design system components (buttons, forms, cards, navigation)
    - Apply "Urban Tech + Rental" theme consistently across all screens
    - _Requirements: 15.1, 15.2, 15.3_

  - [ ] 15.2 Build responsive layouts and components
    - Implement mobile-first responsive design (320px to 1920px)
    - Create touch-optimized controls for mobile (44×44px minimum)
    - Add progressive loading and offline capability for poor network conditions
    - _Requirements: 11.1, 11.2, 11.3, 11.5_

  - [x] 15.3 Write UI component tests
    - Test component responsiveness across breakpoints
    - Test accessibility compliance (contrast ratios, ARIA labels)
    - Test browser compatibility (Chrome, Firefox, Safari, Edge)
    - _Requirements: 11.4_

### P0: Configuration and Error Handling

- [ ] 16. Implement system configuration and error resilience
  - [ ] 16.1 Create configuration management system
    - Implement YAML configuration parsing with schema validation
    - Add environment-specific configurations (development, staging, production)
    - Create pretty printer for configuration round-trip validation
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

  - [ ] 16.2 Build comprehensive error handling
    - Implement structured JSON logging with context (user_id, request_id, stack trace)
    - Add circuit breakers for external dependencies with fallback mechanisms
    - Create user-friendly error messages with recovery suggestions
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

  - [x] 16.3 Write property tests for configuration validation
    - **Property 17: Configuration round-trip** - parse(print(config)) equals original config
    - **Property 18: Environment isolation** - Configurations don't leak between environments
    - **Validates: Requirements 12.4, 12.5**

### P0: Security and Performance Optimization

- [ ] 17. Implement security and performance features
  - [ ] 17.1 Add security measures
    - Implement data encryption (bcrypt for passwords, AES-256 for sensitive data)
    - Add multi-factor authentication for sensitive operations
    - Implement brute force protection (account lockout after 5 failed attempts)
    - _Requirements: 18.1, 18.2, 18.3, 18.5_

  - [ ] 17.2 Optimize system performance
    - Implement response time targets (dashboard <2s, search <1s, API <500ms)
    - Add query optimization and database indexing
    - Implement caching strategy (Redis for sessions, API response caching)
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

  - [x] 17.3 Write performance and security tests
    - Test response time SLAs under load (100 concurrent users)
    - Test security controls effectiveness (authentication, authorization, data protection)
    - Test graceful degradation under failure conditions
    - _Requirements: 17.3, 18.6_

- [ ] 18. Final checkpoint - Complete system validation
  - Ensure all tests pass, verify demo scenario works (Pavani rents picnic mat), ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- P0 tasks are critical path for MVP functionality
- P1 tasks are important for core rental workflow
- P2 tasks are enhancements that improve user experience and system intelligence
- Each task references specific requirements for traceability (e.g., Requirements 4.3 refers to timer stop precision)
- Property tests validate universal correctness properties defined in requirements
- Checkpoints ensure incremental validation at major milestones
- The demo scenario (Pavani rents picnic mat) should be testable after completing P0 and P1 tasks

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3"] },
    { "id": 1, "tasks": ["3.1", "4.1", "16.1"] },
    { "id": 2, "tasks": ["3.2", "3.4", "4.2", "4.4", "5.1", "7.1", "16.2"] },
    { "id": 3, "tasks": ["1.4", "3.3", "4.3", "5.2", "7.2", "7.4", "8.1", "9.1", "9.2", "15.1"] },
    { "id": 4, "tasks": ["5.3", "7.3", "8.2", "8.4", "9.4", "11.1", "12.1", "13.1", "14.1", "15.2"] },
    { "id": 5, "tasks": ["8.3", "9.3", "11.2", "11.4", "12.2", "13.2", "14.2", "16.3", "17.1"] },
    { "id": 6, "tasks": ["11.3", "12.3", "13.3", "14.3", "15.3", "17.2"] },
    { "id": 7, "tasks": ["17.3"] }
  ]
}
```