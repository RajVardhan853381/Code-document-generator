/**
 * Utility Functions - Sample JavaScript File for Testing
 * Demonstrates various JavaScript features for documentation generation.
 */

/**
 * String utility class for common string operations
 */
class StringUtils {
    /**
     * Convert string to title case
     * @param {string} str - Input string
     * @returns {string} String in title case
     * @example
     * StringUtils.toTitleCase('hello world'); // 'Hello World'
     */
    static toTitleCase(str) {
        return str.replace(/\w\S*/g, (txt) => {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    /**
     * Reverse a string
     * @param {string} str - Input string
     * @returns {string} Reversed string
     */
    static reverse(str) {
        return str.split('').reverse().join('');
    }

    /**
     * Check if string is palindrome
     * @param {string} str - Input string
     * @returns {boolean} True if palindrome, false otherwise
     */
    static isPalindrome(str) {
        const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
        return cleaned === cleaned.split('').reverse().join('');
    }
}

/**
 * Array utility class for common array operations
 */
class ArrayUtils {
    /**
     * Get unique values from array
     * @param {Array} arr - Input array
     * @returns {Array} Array with unique values
     */
    static unique(arr) {
        return [...new Set(arr)];
    }

    /**
     * Chunk array into smaller arrays
     * @param {Array} arr - Input array
     * @param {number} size - Size of each chunk
     * @returns {Array<Array>} Array of chunks
     */
    static chunk(arr, size) {
        const chunks = [];
        for (let i = 0; i < arr.length; i += size) {
            chunks.push(arr.slice(i, i + size));
        }
        return chunks;
    }

    /**
     * Flatten nested array
     * @param {Array} arr - Nested array
     * @returns {Array} Flattened array
     */
    static flatten(arr) {
        return arr.reduce((flat, item) => {
            return flat.concat(Array.isArray(item) ? ArrayUtils.flatten(item) : item);
        }, []);
    }
}

/**
 * Mathematical utility functions
 */
const MathUtils = {
    /**
     * Calculate average of numbers
     * @param {number[]} numbers - Array of numbers
     * @returns {number} Average value
     */
    average: (numbers) => {
        if (numbers.length === 0) return 0;
        const sum = numbers.reduce((a, b) => a + b, 0);
        return sum / numbers.length;
    },

    /**
     * Find maximum value
     * @param {number[]} numbers - Array of numbers
     * @returns {number} Maximum value
     */
    max: (numbers) => Math.max(...numbers),

    /**
     * Find minimum value
     * @param {number[]} numbers - Array of numbers
     * @returns {number} Minimum value
     */
    min: (numbers) => Math.min(...numbers)
};

/**
 * Format currency value
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (default: 'USD')
 * @returns {string} Formatted currency string
 */
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Debounce function execution
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Export modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        StringUtils,
        ArrayUtils,
        MathUtils,
        formatCurrency,
        debounce
    };
}
