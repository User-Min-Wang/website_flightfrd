/**
 * Validation utilities for the aircraft tracking application
 */

/**
 * Validate ICAO code (6-character hexadecimal)
 */
export const validateICAOCode = (code: string): boolean => {
  if (!code) return false
  return /^[0-9A-Fa-f]{6}$/.test(code.trim())
}

/**
 * Validate aircraft registration
 * Different countries have different formats, but generally:
 * - Start with a letter
 * - Followed by 1-5 alphanumeric characters
 * - May include dashes or spaces in certain formats
 */
export const validateRegistration = (reg: string): boolean => {
  if (!reg) return false
  // Remove spaces and dashes for validation
  const cleanedReg = reg.replace(/[-\s]/g, '')
  return /^[A-Za-z][A-Za-z0-9]{1,5}$/.test(cleanedReg)
}

/**
 * Validate flight number
 * Typically consists of 2-3 letter airline code followed by numbers
 */
export const validateFlightNumber = (flightNum: string): boolean => {
  if (!flightNum) return false
  return /^[A-Za-z]{2,3}\d+$/.test(flightNum.trim())
}

/**
 * Validate airport code (ICAO or IATA)
 * ICAO: 4 letters (e.g., KJFK)
 * IATA: 3 letters (e.g., JFK)
 */
export const validateAirportCode = (code: string): boolean => {
  if (!code) return false
  return /^([A-Za-z]{3}|[A-Za-z]{4})$/.test(code.trim())
}

/**
 * Validate frequency (typically 3 digits with optional decimals)
 * Examples: 118.700, 121.5, 134.450
 */
export const validateFrequency = (freq: string): boolean => {
  if (!freq) return false
  return /^\d{3}(\.\d{1,3})?$/.test(freq.trim())
}

/**
 * Validate squawk code (4-digit octal number)
 * Each digit must be between 0-7
 */
export const validateSquawkCode = (squawk: string): boolean => {
  if (!squawk) return false
  return /^[0-7]{4}$/.test(squawk.trim())
}

/**
 * Validate email address
 */
export const validateEmail = (email: string): boolean => {
  if (!email) return false
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate phone number (basic validation)
 * Accepts various formats with optional country code
 */
export const validatePhone = (phone: string): boolean => {
  if (!phone) return false
  // Remove common separators
  const cleanedPhone = phone.replace(/[-\s().+]/g, '')
  // Basic validation: at least 7 digits, maximum 15
  return /^\d{7,15}$/.test(cleanedPhone)
}

/**
 * Validate coordinate (latitude or longitude)
 */
export const validateCoordinate = (coord: number | null, isLatitude: boolean): boolean => {
  if (coord === null || coord === undefined) return false
  
  if (isLatitude) {
    return coord >= -90 && coord <= 90
  } else {
    return coord >= -180 && coord <= 180
  }
}

/**
 * Validate positive integer
 */
export const validatePositiveInteger = (value: number | string): boolean => {
  const numValue = typeof value === 'string' ? parseInt(value, 10) : value
  return Number.isInteger(numValue) && numValue > 0
}

/**
 * Validate positive number
 */
export const validatePositiveNumber = (value: number | string): boolean => {
  const numValue = typeof value === 'string' ? parseFloat(value) : value
  return typeof numValue === 'number' && !isNaN(numValue) && numValue > 0
}

/**
 * Validate date string in ISO format
 */
export const validateISODate = (dateString: string): boolean => {
  if (!dateString) return false
  const date = new Date(dateString)
  return date instanceof Date && !isNaN(date.getTime())
}

/**
 * Validate URL
 */
export const validateURL = (url: string): boolean => {
  if (!url) return false
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}