/**
 * Validation utilities for common input validation
 */

/**
 * Validate email format
 * @example isValidEmail("user@example.com") → true
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 * Min 6 chars, at least one uppercase, one lowercase, one number
 * @example isValidPassword("Pass123") → true
 */
export const isValidPassword = (password: string): boolean => {
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/;
  return passwordRegex.test(password);
};

/**
 * Validate phone number (Indian format)
 * @example isValidPhoneNumber("9876543210") → true
 */
export const isValidPhoneNumber = (phone: string): boolean => {
  const phoneRegex = /^[6-9]\d{9}$/;
  return phoneRegex.test(phone);
};

/**
 * Validate if string is empty or whitespace only
 * @example isEmpty("  ") → true
 */
export const isEmpty = (text: string): boolean => {
  return !text || text.trim().length === 0;
};

/**
 * Validate if number is positive
 * @example isPositive(10) → true
 */
export const isPositive = (num: number): boolean => {
  return num > 0;
};

/**
 * Validate if price is in valid range (₹50 - ₹500)
 * @example isValidPrice(150) → true
 */
export const isValidPrice = (price: number): boolean => {
  return price >= 50 && price <= 500;
};

/**
 * Validate if date is in the future
 * @example isFutureDate(new Date(Date.now() + 86400000)) → true
 */
export const isFutureDate = (date: Date): boolean => {
  return date > new Date();
};

/**
 * Validate if date is in the past
 * @example isPastDate(new Date(Date.now() - 86400000)) → true
 */
export const isPastDate = (date: Date): boolean => {
  return date < new Date();
};

/**
 * Validate rental hours are within acceptable range (1-24 hours)
 * @example isValidRentalHours(5) → true
 */
export const isValidRentalHours = (hours: number): boolean => {
  return hours >= 1 && hours <= 24;
};

/**
 * Validate if URL is valid
 * @example isValidUrl("https://example.com") → true
 */
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

/**
 * Validate if string contains only letters
 * @example isAlphabetic("Hello") → true
 */
export const isAlphabetic = (text: string): boolean => {
  return /^[a-zA-Z\s]+$/.test(text);
};

/**
 * Validate if string contains only alphanumeric characters
 * @example isAlphanumeric("Hello123") → true
 */
export const isAlphanumeric = (text: string): boolean => {
  return /^[a-zA-Z0-9]+$/.test(text);
};

/**
 * Validate form data object
 * @example validateForm({email: "user@example.com", password: "Pass123"}) → {valid: true}
 */
export const validateForm = (data: Record<string, any>): { valid: boolean; errors: Record<string, string> } => {
  const errors: Record<string, string> = {};

  if (data.email && !isValidEmail(data.email)) {
    errors.email = 'Invalid email format';
  }

  if (data.password && !isValidPassword(data.password)) {
    errors.password = 'Password must be at least 6 characters with uppercase, lowercase, and numbers';
  }

  if (data.phone && !isValidPhoneNumber(data.phone)) {
    errors.phone = 'Invalid phone number';
  }

  if (data.price && !isValidPrice(data.price)) {
    errors.price = 'Price must be between ₹50 and ₹500';
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors,
  };
};
