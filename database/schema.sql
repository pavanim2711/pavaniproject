-- Quick Tym SQLite Database Schema
-- Complete database setup with all 15 tables, constraints, and indexes
-- Version: 1.0
-- Created: 2024

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================================================
-- 1. CATEGORIES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    parent_category_id TEXT REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_category_id);

-- ============================================================================
-- 2. USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('Customer', 'Delivery_Partner', 'Admin')),
    phone TEXT UNIQUE,
    address TEXT,
    location TEXT DEFAULT 'Bengaluru',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    rating DECIMAL(3,2) DEFAULT 5.0 CHECK (rating >= 0 AND rating <= 5),
    total_rentals INTEGER DEFAULT 0,
    total_spent DECIMAL(12,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_rating ON users(rating);
CREATE INDEX IF NOT EXISTS idx_users_location ON users(location);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- ============================================================================
-- 3. PRODUCTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    category_id TEXT REFERENCES categories(id),
    name TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL CHECK (category IN ('Indoor', 'Outdoor')),
    price_per_hour DECIMAL(10,2) NOT NULL CHECK (price_per_hour BETWEEN 50 AND 500),
    min_rental_hours INTEGER DEFAULT 1 CHECK (min_rental_hours >= 1),
    max_rental_hours INTEGER DEFAULT 24 CHECK (max_rental_hours <= 168),
    specifications TEXT,
    image_url TEXT,
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
    security_deposit DECIMAL(10,2) DEFAULT 0.00
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price_per_hour);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_popularity ON products(popularity_score);
CREATE INDEX IF NOT EXISTS idx_products_rental_count ON products(rental_count);
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);

-- ============================================================================
-- 4. INVENTORY TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    location TEXT DEFAULT 'Bengaluru',
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    available_quantity INTEGER NOT NULL DEFAULT 0 CHECK (available_quantity >= 0),
    low_stock_threshold INTEGER DEFAULT 2,
    last_restocked TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, location)
);

CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_inventory_location ON inventory(location);
CREATE INDEX IF NOT EXISTS idx_inventory_availability ON inventory(available_quantity);

-- ============================================================================
-- 5. RENTAL SESSIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS rental_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL REFERENCES products(id),
    status TEXT NOT NULL CHECK (status IN ('pending', 'active', 'completed', 'cancelled', 'overdue', 'paid')),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    total_seconds INTEGER CHECK (total_seconds >= 0),
    billable_seconds INTEGER CHECK (billable_seconds >= 0),
    base_amount DECIMAL(12,2) CHECK (base_amount >= 0),
    tax_amount DECIMAL(12,2) CHECK (tax_amount >= 0),
    delivery_fee DECIMAL(12,2) DEFAULT 0.00 CHECK (delivery_fee >= 0),
    cleaning_fee DECIMAL(12,2) DEFAULT 0.00 CHECK (cleaning_fee >= 0),
    security_deposit DECIMAL(12,2) DEFAULT 0.00 CHECK (security_deposit >= 0),
    deposit_returned BOOLEAN DEFAULT FALSE,
    total_amount DECIMAL(12,2) CHECK (total_amount >= 0),
    location TEXT DEFAULT 'Bengaluru',
    delivery_address TEXT,
    pickup_address TEXT,
    delivery_id TEXT REFERENCES deliveries(id),
    pickup_request_id TEXT REFERENCES pickup_requests(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    cancelled_by TEXT REFERENCES users(id),
    payment_id TEXT REFERENCES payments(id),
    invoice_number TEXT UNIQUE,
    extensions INTEGER DEFAULT 0,
    total_extended_seconds INTEGER DEFAULT 0,
    timer_started_at TIMESTAMP,
    timer_stopped_at TIMESTAMP,
    last_timer_update TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rental_sessions_user_id ON rental_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_product_id ON rental_sessions(product_id);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_status ON rental_sessions(status);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_dates ON rental_sessions(start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_created_at ON rental_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_location ON rental_sessions(location);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_payment_id ON rental_sessions(payment_id);
CREATE INDEX IF NOT EXISTS idx_rental_sessions_invoice_number ON rental_sessions(invoice_number);

-- ============================================================================
-- 6. BOOKINGS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS bookings (
    id TEXT PRIMARY KEY,
    rental_session_id TEXT NOT NULL REFERENCES rental_sessions(id) ON DELETE CASCADE,
    scheduled_start TIMESTAMP NOT NULL,
    scheduled_end TIMESTAMP NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('confirmed', 'pending', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bookings_rental_session_id ON bookings(rental_session_id);
CREATE INDEX IF NOT EXISTS idx_bookings_scheduled_times ON bookings(scheduled_start, scheduled_end);

-- ============================================================================
-- 7. PAYMENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    rental_session_id TEXT NOT NULL REFERENCES rental_sessions(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
    currency TEXT DEFAULT 'INR',
    status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'success', 'failed', 'refunded', 'partially_refunded', 'disputed')),
    payment_method TEXT NOT NULL CHECK (payment_method IN ('credit_card', 'debit_card', 'upi', 'net_banking', 'wallet')),
    payment_gateway TEXT DEFAULT 'mock',
    transaction_id TEXT UNIQUE,
    gateway_transaction_id TEXT,
    gateway_response TEXT,
    card_last4 TEXT,
    card_brand TEXT,
    receipt_url TEXT,
    invoice_url TEXT,
    refund_amount DECIMAL(12,2) DEFAULT 0.00 CHECK (refund_amount >= 0),
    refund_reason TEXT,
    refunded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    failed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0 CHECK (retry_count >= 0)
);

CREATE INDEX IF NOT EXISTS idx_payments_rental_session_id ON payments(rental_session_id);
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);
CREATE INDEX IF NOT EXISTS idx_payments_created_at ON payments(created_at);
CREATE INDEX IF NOT EXISTS idx_payments_payment_method ON payments(payment_method);
CREATE INDEX IF NOT EXISTS idx_payments_transaction_id ON payments(transaction_id);
CREATE INDEX IF NOT EXISTS idx_payments_gateway ON payments(payment_gateway);

-- ============================================================================
-- 8. DELIVERIES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS deliveries (
    id TEXT PRIMARY KEY,
    rental_session_id TEXT NOT NULL REFERENCES rental_sessions(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'assigned', 'in_transit', 'delivered', 'pickup_requested', 'completed')),
    assigned_partner_id TEXT REFERENCES users(id),
    total_distance_km DECIMAL(10,2),
    total_estimated_minutes INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    route_coordinates TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_deliveries_rental_session_id ON deliveries(rental_session_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_assigned_partner_id ON deliveries(assigned_partner_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_status ON deliveries(status);

-- ============================================================================
-- 9. DELIVERY TASKS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS delivery_tasks (
    id TEXT PRIMARY KEY,
    delivery_id TEXT NOT NULL REFERENCES deliveries(id) ON DELETE CASCADE,
    task_type TEXT NOT NULL CHECK (task_type IN ('delivery', 'pickup')),
    status TEXT NOT NULL CHECK (status IN ('pending', 'assigned', 'in_progress', 'completed', 'failed')),
    assigned_to TEXT REFERENCES users(id),
    scheduled_time TIMESTAMP,
    completed_time TIMESTAMP,
    address TEXT NOT NULL,
    notes TEXT,
    distance_km DECIMAL(8,2),
    estimated_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    photo_evidence_url TEXT,
    customer_signature_url TEXT
);

CREATE INDEX IF NOT EXISTS idx_delivery_tasks_delivery_id ON delivery_tasks(delivery_id);
CREATE INDEX IF NOT EXISTS idx_delivery_tasks_assigned_to ON delivery_tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_delivery_tasks_status ON delivery_tasks(status);
CREATE INDEX IF NOT EXISTS idx_delivery_tasks_scheduled_time ON delivery_tasks(scheduled_time);

-- ============================================================================
-- 10. PICKUP REQUESTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS pickup_requests (
    id TEXT PRIMARY KEY,
    rental_session_id TEXT NOT NULL REFERENCES rental_sessions(id) ON DELETE CASCADE,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK (status IN ('pending', 'assigned', 'completed')),
    assigned_partner_id TEXT REFERENCES users(id),
    completed_at TIMESTAMP,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_pickup_requests_rental_session_id ON pickup_requests(rental_session_id);
CREATE INDEX IF NOT EXISTS idx_pickup_requests_status ON pickup_requests(status);

-- ============================================================================
-- 11. REVIEWS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS reviews (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL REFERENCES products(id),
    rental_session_id TEXT REFERENCES rental_sessions(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title TEXT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, rental_session_id)
);

CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);

-- ============================================================================
-- 12. NOTIFICATIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

-- ============================================================================
-- 13. AI RECOMMENDATIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS ai_recommendations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id TEXT NOT NULL REFERENCES products(id),
    recommendation_type TEXT NOT NULL CHECK (recommendation_type IN ('similarity', 'popularity', 'collaborative', 'contextual', 'trending')),
    affinity_score INTEGER NOT NULL CHECK (affinity_score >= 0 AND affinity_score <= 100),
    confidence_score DECIMAL(5,4) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    is_fallback BOOLEAN DEFAULT FALSE,
    fallback_reason TEXT,
    generation_time_ms INTEGER CHECK (generation_time_ms >= 0),
    timeout_occurred BOOLEAN DEFAULT FALSE,
    reason TEXT,
    context TEXT,
    was_shown BOOLEAN DEFAULT FALSE,
    was_clicked BOOLEAN DEFAULT FALSE,
    click_position INTEGER CHECK (click_position >= 1),
    dwell_time_ms INTEGER CHECK (dwell_time_ms >= 0),
    conversion BOOLEAN DEFAULT FALSE,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    shown_at TIMESTAMP,
    clicked_at TIMESTAMP,
    converted_at TIMESTAMP,
    model_version TEXT
);

CREATE INDEX IF NOT EXISTS idx_ai_recommendations_user_id ON ai_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_product_id ON ai_recommendations(product_id);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_affinity_score ON ai_recommendations(affinity_score);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_type ON ai_recommendations(recommendation_type);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_expires_at ON ai_recommendations(expires_at);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_generated_at ON ai_recommendations(generated_at);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_was_clicked ON ai_recommendations(was_clicked);
CREATE INDEX IF NOT EXISTS idx_ai_recommendations_is_fallback ON ai_recommendations(is_fallback);

-- ============================================================================
-- 14. DEMAND PREDICTIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS demand_predictions (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL REFERENCES products(id),
    location TEXT DEFAULT 'Bengaluru',
    prediction_date DATE NOT NULL,
    predicted_demand INTEGER NOT NULL CHECK (predicted_demand >= 0),
    confidence_interval_lower INTEGER CHECK (confidence_interval_lower >= 0),
    confidence_interval_upper INTEGER CHECK (confidence_interval_upper >= 0),
    prediction_std_dev DECIMAL(10,2) CHECK (prediction_std_dev >= 0),
    historical_mean DECIMAL(10,2) CHECK (historical_mean >= 0),
    historical_std_dev DECIMAL(10,2) CHECK (historical_std_dev >= 0),
    weekday_factor DECIMAL(6,4) CHECK (weekday_factor >= 0),
    weekend_factor DECIMAL(6,4) CHECK (weekend_factor >= 0),
    holiday_factor DECIMAL(6,4) CHECK (holiday_factor >= 0),
    model_version TEXT NOT NULL,
    model_type TEXT CHECK (model_type IN ('arima', 'sarima', 'exponential_smoothing', 'prophet', 'lstm', 'rule_based')),
    model_accuracy DECIMAL(5,4) CHECK (model_accuracy >= 0 AND model_accuracy <= 1),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actual_demand INTEGER CHECK (actual_demand >= 0),
    validated BOOLEAN DEFAULT FALSE,
    validated_at TIMESTAMP,
    UNIQUE(product_id, location, prediction_date, model_version)
);

CREATE INDEX IF NOT EXISTS idx_demand_predictions_product_id ON demand_predictions(product_id);
CREATE INDEX IF NOT EXISTS idx_demand_predictions_date ON demand_predictions(prediction_date);
CREATE INDEX IF NOT EXISTS idx_demand_predictions_location ON demand_predictions(location);
CREATE INDEX IF NOT EXISTS idx_demand_predictions_model_version ON demand_predictions(model_version);
CREATE INDEX IF NOT EXISTS idx_demand_predictions_generated_at ON demand_predictions(generated_at);
CREATE INDEX IF NOT EXISTS idx_demand_predictions_validated ON demand_predictions(validated);

-- ============================================================================
-- 15. AUDIT LOG TABLE (Supporting table)
-- ============================================================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values TEXT,
    new_values TEXT,
    changed_by TEXT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_changed_by ON audit_logs(changed_by);

-- ============================================================================
-- INIT MESSAGE
-- ============================================================================
-- Database schema created successfully. All tables, indexes, and constraints in place.
