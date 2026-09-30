/**
 * Formatter utilities for common data transformations
 */

/**
 * Format price in Indian Rupees
 * @example formatPrice(150) → "₹150"
 */
export const formatPrice = (price: number): string => {
  return `₹${Math.round(price)}`;
};

/**
 * Format price with decimal places
 * @example formatPriceWithDecimal(150.5) → "₹150.50"
 */
export const formatPriceWithDecimal = (price: number): string => {
  return `₹${price.toFixed(2)}`;
};

/**
 * Format date to readable format
 * @example formatDate(new Date()) → "14 Aug 2026"
 */
export const formatDate = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return dateObj.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Format time to readable format
 * @example formatTime(new Date()) → "2:30 PM"
 */
export const formatTime = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return dateObj.toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
};

/**
 * Format date and time together
 * @example formatDateTime(new Date()) → "14 Aug 2026, 2:30 PM"
 */
export const formatDateTime = (date: Date | string): string => {
  return `${formatDate(date)}, ${formatTime(date)}`;
};

/**
 * Format duration in hours to readable format
 * @example formatDuration(2.5) → "2h 30m"
 */
export const formatDuration = (hours: number): string => {
  const h = Math.floor(hours);
  const m = Math.round((hours - h) * 60);
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
};

/**
 * Truncate text with ellipsis
 * @example truncateText("Hello World", 8) → "Hello..."
 */
export const truncateText = (text: string, length: number): string => {
  return text.length > length ? text.substring(0, length) + '...' : text;
};

/**
 * Capitalize first letter
 * @example capitalize("hello") → "Hello"
 */
export const capitalize = (text: string): string => {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
};

/**
 * Format category name with proper casing
 * @example formatCategoryName("outdoor") → "Outdoor"
 */
export const formatCategoryName = (category: string): string => {
  return category
    .split('_')
    .map(word => capitalize(word))
    .join(' ');
};

/**
 * Format rental hours to readable format
 * @example formatRentalHours(2) → "2 hours"
 */
export const formatRentalHours = (hours: number): string => {
  return hours === 1 ? '1 hour' : `${hours} hours`;
};

/**
 * Format number as currency
 * @example formatCurrency(1000) → "1,000"
 */
export const formatCurrency = (amount: number): string => {
  return amount.toLocaleString('en-IN');
};

/**
 * Format product name for display
 * @example formatProductName("camping_tent_4_person") → "Camping Tent 4 Person"
 */
export const formatProductName = (name: string): string => {
  return name
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => capitalize(word))
    .join(' ');
};
