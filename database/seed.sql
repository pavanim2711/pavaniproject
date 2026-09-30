-- Quick Tym Sample Data - Bengaluru Rental Market
-- Realistic data for testing and demo purposes
-- Version: 1.0

PRAGMA foreign_keys = OFF;

-- ============================================================================
-- INSERT CATEGORIES FIRST
-- ============================================================================
INSERT OR IGNORE INTO categories (id, name, description) VALUES
('cat-1', 'Outdoor', 'Outdoor equipment and camping gear'),
('cat-2', 'Indoor', 'Indoor equipment and furniture'),
('cat-3', 'Sports', 'Sports and recreational equipment'),
('cat-4', 'Tools', 'Construction and DIY tools'),
('cat-5', 'Party', 'Party and event supplies'),
('cat-6', 'Travel', 'Travel and photography equipment');

-- ============================================================================
-- INSERT USERS (No FK dependencies)
-- ============================================================================
INSERT OR IGNORE INTO users (id, email, password_hash, name, role, phone, location, is_active, is_verified, rating, total_rentals, total_spent, created_at) VALUES
('user-1', 'priya.sharma@example.com', '$2b$12$abcdefghijklmnopqrstuvwxyz1234567890', 'Priya Sharma', 'Customer', '9876543210', 'Bengaluru', 1, 1, 4.5, 12, 5400.00, datetime('now', '-30 days')),
('user-2', 'rajesh.kumar@example.com', '$2b$12$hijklmnopqrstuvwxyzabcdef1234567890', 'Rajesh Kumar', 'Delivery_Partner', '9876543211', 'Bengaluru', 1, 1, 4.8, 180, 0.00, datetime('now', '-60 days')),
('user-3', 'admin@quicktym.com', '$2b$12$klmnopqrstuvwxyzabcdefghij1234567890', 'Admin Bengaluru', 'Admin', '9876543212', 'Bengaluru', 1, 1, 5.0, 0, 0.00, datetime('now', '-90 days')),
('user-4', 'arun.singh@example.com', '$2b$12$mnopqrstuvwxyzabcdefghijk1234567890', 'Arun Singh', 'Customer', '9876543213', 'Bengaluru', 1, 1, 4.2, 5, 2100.00, datetime('now', '-15 days'));

-- ============================================================================
-- INSERT PRODUCTS (Depends on categories)
-- ============================================================================
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-1', 'cat-1', 'Camping Tent (4-person)', 'Waterproof 4-person camping tent with easy setup. Perfect for trekking and camping adventures in Western Ghats.', 'Outdoor', 150.00, 1, 24, '4 capacity, 3.2kg weight', '/images/tent.jfif', 0.92, 28, 4.6, 15, 1, 1, 100.00, 50.00, 2000.00, datetime('now', '-45 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-2', 'cat-5', 'Portable Bluetooth Speaker', 'High-quality portable speaker with 360-degree sound. Great for parties, picnics, and outdoor events.', 'Indoor', 80.00, 2, 12, '20W power, 10 hours battery', '/images/bluetooth-speaker.jpg', 0.88, 42, 4.4, 22, 1, 1, 80.00, 40.00, 1500.00, datetime('now', '-50 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-3', 'cat-4', 'Power Drill Set (20-piece)', 'Complete power drill set with bits and accessories. Ideal for construction, DIY projects, and home renovation.', 'Outdoor', 100.00, 1, 24, '20V voltage, 20 pieces', '/images/electric-drill.webp', 0.85, 18, 4.3, 9, 1, 1, 120.00, 60.00, 3000.00, datetime('now', '-40 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-4', 'cat-1', 'Trekking Backpack 60L', 'Professional 60-liter backpack for multi-day trekking. Comfortable suspension system and weather-resistant.', 'Outdoor', 120.00, 1, 72, '60L capacity, 1.8kg weight', '/images/backpack.jpg', 0.90, 35, 4.7, 18, 1, 1, 90.00, 45.00, 2500.00, datetime('now', '-48 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-5', 'cat-5', 'Folding Table (6-seater)', 'Lightweight folding table perfect for outdoor events, parties, and gatherings. Easy to carry and setup.', 'Indoor', 90.00, 2, 24, '6 seats, 1.8m x 0.6m dimensions', '/images/folding-table.webp', 0.83, 22, 4.2, 11, 1, 1, 100.00, 50.00, 1800.00, datetime('now', '-35 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-6', 'cat-4', 'Ladder 8ft Aluminium', 'Heavy-duty 8-foot aluminum ladder. Perfect for household repairs, painting, and maintenance work.', 'Outdoor', 70.00, 1, 24, '8ft height, 5.5kg weight', '/images/ladder.jpg', 0.81, 16, 4.1, 8, 1, 1, 70.00, 35.00, 1200.00, datetime('now', '-30 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-7', 'cat-6', 'Action Camera + Mounts', '4K action camera with multiple mounting accessories. Perfect for adventure sports and travel documentation.', 'Outdoor', 200.00, 2, 24, '4K resolution, 12MP sensor', '/images/action-camera.jpg', 0.94, 31, 4.8, 19, 1, 1, 150.00, 75.00, 4000.00, datetime('now', '-42 days'));
INSERT INTO products (id, category_id, name, description, category, price_per_hour, min_rental_hours, max_rental_hours, specifications, image_url, popularity_score, rental_count, average_rating, review_count, is_active, requires_delivery, delivery_fee, cleaning_fee, security_deposit, created_at) VALUES
('prod-8', 'cat-3', 'Badminton Set (full)', 'Complete badminton set with net, rackets, and shuttles. Great for indoor and outdoor play.', 'Indoor', 60.00, 2, 8, '2 rackets, 12 shuttles included', '/images/badminton-set.jpg', 0.79, 24, 4.0, 12, 1, 1, 60.00, 30.00, 800.00, datetime('now', '-32 days'));

-- ============================================================================
-- INSERT INVENTORY (Depends on products)
-- ============================================================================
INSERT OR IGNORE INTO inventory (id, product_id, location, quantity, available_quantity, low_stock_threshold, last_restocked, created_at, updated_at) VALUES
('inv-1', 'prod-1', 'Bengaluru', 8, 6, 2, datetime('now', '-7 days'), datetime('now', '-10 days'), datetime('now', '-5 days')),
('inv-2', 'prod-2', 'Bengaluru', 12, 10, 3, datetime('now', '-5 days'), datetime('now', '-8 days'), datetime('now', '-3 days')),
('inv-3', 'prod-3', 'Bengaluru', 6, 4, 2, datetime('now', '-10 days'), datetime('now', '-12 days'), datetime('now', '-8 days')),
('inv-4', 'prod-4', 'Bengaluru', 10, 8, 2, datetime('now', '-6 days'), datetime('now', '-9 days'), datetime('now', '-4 days')),
('inv-5', 'prod-5', 'Bengaluru', 7, 5, 2, datetime('now', '-8 days'), datetime('now', '-11 days'), datetime('now', '-6 days')),
('inv-6', 'prod-6', 'Bengaluru', 9, 7, 2, datetime('now', '-9 days'), datetime('now', '-12 days'), datetime('now', '-7 days')),
('inv-7', 'prod-7', 'Bengaluru', 5, 3, 1, datetime('now', '-4 days'), datetime('now', '-7 days'), datetime('now', '-2 days')),
('inv-8', 'prod-8', 'Bengaluru', 15, 13, 3, datetime('now', '-3 days'), datetime('now', '-6 days'), datetime('now', '-1 days'));

-- ============================================================================
-- INSERT PAYMENTS (No FK from users/products, but needs to exist before rental_sessions)
-- ============================================================================
INSERT OR IGNORE INTO payments (id, rental_session_id, user_id, amount, currency, status, payment_method, payment_gateway, transaction_id, gateway_transaction_id, gateway_response, card_last4, receipt_url, invoice_url, created_at, updated_at, processed_at) VALUES
('pay-1', 'rental-1', 'user-1', 6110.00, 'INR', 'success', 'upi', 'mock', 'TXN20240115001', 'MOCK_TXN_001', '{"status": "success", "message": "Payment processed"}', NULL, '/receipts/pay-1.pdf', '/invoices/inv-2024-001.pdf', datetime('now', '-4 days'), datetime('now', '-4 days'), datetime('now', '-4 days')),
('pay-2', 'rental-2', 'user-4', 1796.00, 'INR', 'pending', 'credit_card', 'mock', NULL, NULL, NULL, NULL, NULL, NULL, datetime('now', '-2 days'), datetime('now', '-2 days'), NULL);

-- ============================================================================
-- INSERT DELIVERIES (Can be created before rental_sessions reference them)
-- ============================================================================
INSERT OR IGNORE INTO deliveries (id, rental_session_id, status, assigned_partner_id, total_distance_km, total_estimated_minutes, started_at, completed_at, created_at, updated_at) VALUES
('deliv-1', 'rental-1', 'completed', 'user-2', 12.5, 28, datetime('now', '-5 days', '+07:00'), datetime('now', '-5 days', '+09:30'), datetime('now', '-5 days'), datetime('now', '-3 days')),
('deliv-2', 'rental-2', 'in_transit', 'user-2', 18.3, 35, datetime('now', '-2 days', '+09:00'), NULL, datetime('now', '-2 days'), datetime('now', '-1 days'));

-- ============================================================================
-- INSERT PICKUP REQUESTS (Can be created before rental_sessions reference them)
-- ============================================================================
INSERT OR IGNORE INTO pickup_requests (id, rental_session_id, requested_at, status, assigned_partner_id, completed_at, notes) VALUES
('pickup-1', 'rental-1', datetime('now', '-3 days'), 'completed', 'user-2', datetime('now', '-3 days', '+19:45'), 'Tenant condition verified as per contract'),
('pickup-2', 'rental-2', datetime('now', '-1 days'), 'pending', NULL, NULL, 'Awaiting pickup completion');

-- ============================================================================
-- INSERT RENTAL SESSIONS (Now depends on users, products, payments, deliveries, pickups)
-- ============================================================================
INSERT OR IGNORE INTO rental_sessions (id, user_id, product_id, status, start_time, end_time, total_seconds, billable_seconds, base_amount, tax_amount, delivery_fee, cleaning_fee, security_deposit, deposit_returned, total_amount, location, delivery_address, pickup_address, delivery_id, pickup_request_id, created_at, updated_at, timer_started_at, timer_stopped_at, invoice_number, payment_id) VALUES
('rental-1', 'user-1', 'prod-1', 'completed', datetime('now', '-5 days', '+08:00'), datetime('now', '-5 days', '+32:00'), 86400, 86400, 3600.00, 360.00, 100.00, 50.00, 2000.00, 1, 6110.00, 'Bengaluru', '{"area": "Koramangala", "street": "Tech Park Road", "building": "Tower A"}', '{"area": "Indiranagar", "street": "100 Feet Road", "building": "Apt 305"}', 'deliv-1', 'pickup-1', datetime('now', '-5 days'), datetime('now', '-3 days'), datetime('now', '-5 days', '+08:00'), datetime('now', '-5 days', '+32:00'), 'INV-2024-001', 'pay-1'),
('rental-2', 'user-4', 'prod-2', 'active', datetime('now', '-2 days', '+10:00'), NULL, NULL, NULL, 160.00, 16.00, 80.00, 40.00, 1500.00, 0, 1796.00, 'Bengaluru', '{"area": "Whitefield", "street": "International Tech Park", "building": "Building 2"}', '{"area": "Marathahalli", "street": "Main Road", "building": "House 45"}', 'deliv-2', 'pickup-2', datetime('now', '-2 days'), datetime('now', '-1 days'), datetime('now', '-2 days', '+10:00'), NULL, 'INV-2024-002', 'pay-2');

-- ============================================================================
-- INSERT BOOKINGS (Depends on rental_sessions)
-- ============================================================================
INSERT OR IGNORE INTO bookings (id, rental_session_id, scheduled_start, scheduled_end, status, notes, created_at) VALUES
('book-1', 'rental-1', datetime('now', '-5 days', '+08:00'), datetime('now', '-5 days', '+32:00'), 'confirmed', 'Camping trip to Nandi Hills', datetime('now', '-7 days')),
('book-2', 'rental-2', datetime('now', '-2 days', '+10:00'), datetime('now', '-1 days', '+10:00'), 'confirmed', 'Party at community center', datetime('now', '-3 days'));

-- ============================================================================
-- INSERT DELIVERY TASKS (Depends on deliveries)
-- ============================================================================
INSERT OR IGNORE INTO delivery_tasks (id, delivery_id, task_type, status, assigned_to, scheduled_time, completed_time, address, notes, distance_km, estimated_duration_minutes, actual_duration_minutes) VALUES
('task-1', 'deliv-1', 'delivery', 'completed', 'user-2', datetime('now', '-5 days', '+08:00'), datetime('now', '-5 days', '+09:30'), '{"area": "Koramangala", "street": "Tech Park Road", "building": "Tower A"}', 'Tent delivered safely', 12.5, 25, 22),
('task-2', 'deliv-1', 'pickup', 'completed', 'user-2', datetime('now', '-3 days', '+18:00'), datetime('now', '-3 days', '+19:45'), '{"area": "Indiranagar", "street": "100 Feet Road", "building": "Apt 305"}', 'Tent picked up, condition verified', 12.5, 25, 27),
('task-3', 'deliv-2', 'delivery', 'in_progress', 'user-2', datetime('now', '-2 days', '+10:00'), NULL, '{"area": "Whitefield", "street": "International Tech Park", "building": "Building 2"}', 'On the way', 18.3, 32, NULL);

-- ============================================================================
-- INSERT REVIEWS (Depends on users, products, rental_sessions)
-- ============================================================================
INSERT OR IGNORE INTO reviews (id, user_id, product_id, rental_session_id, rating, title, comment, created_at) VALUES
('review-1', 'user-1', 'prod-1', 'rental-1', 5, 'Excellent tent, great experience', 'The tent arrived on time, was in perfect condition. Great quality and waterproof. Would definitely rent again!', datetime('now', '-2 days')),
('review-2', 'user-1', 'prod-1', 'rental-1', 5, 'Delivery was smooth', 'Rajesh was professional and careful with the tent delivery. Highly recommend this service!', datetime('now', '-2 days'));

-- ============================================================================
-- INSERT NOTIFICATIONS (Depends on users)
-- ============================================================================
INSERT OR IGNORE INTO notifications (id, user_id, type, title, message, is_read, created_at) VALUES
('notif-1', 'user-1', 'rental_confirmed', 'Rental Confirmed', 'Your camping tent rental has been confirmed. Delivery scheduled for today at 8-9 AM.', 1, datetime('now', '-5 days')),
('notif-2', 'user-1', 'rental_completed', 'Rental Completed', 'Your tent rental has been completed successfully. Payment of ₹6,110 processed.', 1, datetime('now', '-3 days')),
('notif-3', 'user-1', 'pickup_scheduled', 'Pickup Scheduled', 'Your tent pickup has been scheduled for tomorrow at 6 PM.', 1, datetime('now', '-4 days')),
('notif-4', 'user-4', 'rental_active', 'Rental Active', 'Your Bluetooth speaker rental is now active. Timer started. Hourly rate: ₹80/hour.', 0, datetime('now', '-2 days')),
('notif-5', 'user-2', 'delivery_assigned', 'Delivery Assigned', 'New delivery assigned: Tent to Koramangala. Delivery fee: ₹100.', 1, datetime('now', '-5 days'));

-- ============================================================================
-- INSERT AI RECOMMENDATIONS (Depends on users, products)
-- ============================================================================
INSERT OR IGNORE INTO ai_recommendations (id, user_id, product_id, recommendation_type, affinity_score, confidence_score, is_fallback, generation_time_ms, reason, was_shown, was_clicked, conversion, generated_at) VALUES
('rec-1', 'user-1', 'prod-4', 'similarity', 85, 0.87, 0, 145, 'Based on tent rental history', 1, 1, 1, datetime('now', '-20 days')),
('rec-2', 'user-1', 'prod-7', 'contextual', 78, 0.82, 0, 128, 'Travel-related product', 1, 0, 0, datetime('now', '-15 days')),
('rec-3', 'user-4', 'prod-5', 'popularity', 92, 0.95, 0, 85, 'Popular party gear', 1, 1, 1, datetime('now', '-3 days')),
('rec-4', 'user-4', 'prod-8', 'trending', 88, 0.91, 0, 120, 'Trending this week', 0, 0, 0, datetime('now', '-1 days'));

-- ============================================================================
-- INSERT DEMAND PREDICTIONS (Depends on products)
-- ============================================================================
INSERT OR IGNORE INTO demand_predictions (id, product_id, location, prediction_date, predicted_demand, confidence_interval_lower, confidence_interval_upper, model_version, model_type, generated_at) VALUES
('pred-1', 'prod-1', 'Bengaluru', DATE('now'), 3, 2, 5, 'v1.0', 'rule_based', datetime('now')),
('pred-2', 'prod-2', 'Bengaluru', DATE('now'), 5, 3, 7, 'v1.0', 'rule_based', datetime('now')),
('pred-3', 'prod-3', 'Bengaluru', DATE('now'), 2, 1, 4, 'v1.0', 'rule_based', datetime('now')),
('pred-4', 'prod-4', 'Bengaluru', DATE('now'), 4, 2, 6, 'v1.0', 'rule_based', datetime('now')),
('pred-5', 'prod-5', 'Bengaluru', DATE('now'), 3, 2, 5, 'v1.0', 'rule_based', datetime('now')),
('pred-6', 'prod-6', 'Bengaluru', DATE('now'), 2, 1, 3, 'v1.0', 'rule_based', datetime('now')),
('pred-7', 'prod-7', 'Bengaluru', DATE('now'), 2, 1, 4, 'v1.0', 'rule_based', datetime('now')),
('pred-8', 'prod-8', 'Bengaluru', DATE('now'), 4, 2, 6, 'v1.0', 'rule_based', datetime('now'));

-- Re-enable foreign keys
PRAGMA foreign_keys = ON;
