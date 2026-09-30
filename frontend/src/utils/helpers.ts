/**
 * General helper utilities
 */

/**
 * Get query parameter from URL
 * @example getQueryParam("id") → "123"
 */
export const getQueryParam = (paramName: string): string | null => {
  const params = new URLSearchParams(window.location.search);
  return params.get(paramName);
};

/**
 * Set query parameter in URL
 * @example setQueryParam("id", "123")
 */
export const setQueryParam = (paramName: string, value: string): void => {
  const params = new URLSearchParams(window.location.search);
  params.set(paramName, value);
  window.history.replaceState({}, '', `?${params.toString()}`);
};

/**
 * Get all query parameters as object
 * @example getAllQueryParams() → {id: "123", page: "1"}
 */
export const getAllQueryParams = (): Record<string, string> => {
  const params = new URLSearchParams(window.location.search);
  const result: Record<string, string> = {};
  params.forEach((value, key) => {
    result[key] = value;
  });
  return result;
};

/**
 * Deep clone an object
 * @example deepClone({a: {b: 1}}) → {a: {b: 1}}
 */
export const deepClone = <T>(obj: T): T => {
  return JSON.parse(JSON.stringify(obj));
};

/**
 * Debounce a function
 * @example const debouncedSearch = debounce(search, 300)
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Throttle a function
 * @example const throttledScroll = throttle(onScroll, 1000)
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

/**
 * Retry async operation with exponential backoff
 * @example retry(() => fetch(url), 3, 1000)
 */
export const retry = async <T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  delayMs: number = 1000
): Promise<T> => {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      await new Promise(resolve => setTimeout(resolve, delayMs * attempt));
    }
  }
  throw new Error('Max retries exceeded');
};

/**
 * Sleep for specified milliseconds
 * @example await sleep(1000) // Wait 1 second
 */
export const sleep = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Generate random ID
 * @example generateId() → "abc123xyz"
 */
export const generateId = (): string => {
  return Math.random().toString(36).substring(2, 11);
};

/**
 * Check if object is empty
 * @example isEmpty({}) → true
 */
export const isEmptyObject = (obj: Record<string, any>): boolean => {
  return Object.keys(obj).length === 0;
};

/**
 * Merge two objects deeply
 * @example mergeObjects({a: 1}, {b: 2}) → {a: 1, b: 2}
 */
export const mergeObjects = <T extends Record<string, any>>(
  target: T,
  source: Partial<T>
): T => {
  return { ...target, ...source };
};

/**
 * Get difference between two arrays
 * @example arrayDifference([1,2,3], [2,3,4]) → [1]
 */
export const arrayDifference = <T>(arr1: T[], arr2: T[]): T[] => {
  return arr1.filter(item => !arr2.includes(item));
};

/**
 * Get intersection of two arrays
 * @example arrayIntersection([1,2,3], [2,3,4]) → [2,3]
 */
export const arrayIntersection = <T>(arr1: T[], arr2: T[]): T[] => {
  return arr1.filter(item => arr2.includes(item));
};

/**
 * Get unique values from array
 * @example arrayUnique([1,2,2,3]) → [1,2,3]
 */
export const arrayUnique = <T>(arr: T[]): T[] => {
  return Array.from(new Set(arr));
};

/**
 * Group array by key
 * @example groupBy([{type: 'a', val: 1}, {type: 'a', val: 2}], 'type')
 */
export const groupBy = <T>(arr: T[], key: keyof T): Record<string, T[]> => {
  return arr.reduce((result, item) => {
    const group = String(item[key]);
    if (!result[group]) result[group] = [];
    result[group].push(item);
    return result;
  }, {} as Record<string, T[]>);
};

/**
 * Sort array of objects by property
 * @example sortBy([{name: 'b'}, {name: 'a'}], 'name')
 */
export const sortBy = <T>(arr: T[], key: keyof T, ascending: boolean = true): T[] => {
  return [...arr].sort((a, b) => {
    if (a[key] < b[key]) return ascending ? -1 : 1;
    if (a[key] > b[key]) return ascending ? 1 : -1;
    return 0;
  });
};
