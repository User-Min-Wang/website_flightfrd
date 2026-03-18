/**
 * Constants for the aircraft tracking application
 */

// API endpoints
export const API_ENDPOINTS = {
  AIRCRAFT: '/aircraft',
  FLIGHTS: '/flights',
  ATC: '/atc',
  CALENDAR: '/calendar',
  IMAGES: '/images'
} as const

// Default map settings
export const DEFAULT_MAP_SETTINGS = {
  CENTER: [39.8283, -98.5795] as [number, number], // Center of US
  ZOOM: 4,
  MIN_ZOOM: 2,
  MAX_ZOOM: 18,
  TILE_LAYER: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  TILE_LAYER_ATTRIBUTION: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
} as const

// Units of measurement
export const UNITS = {
  DISTANCE: {
    KM: 'km',
    NM: 'nm',  // nautical miles
    MI: 'mi'   // miles
  },
  ALTITUDE: {
    FEET: 'feet',
    METERS: 'meters'
  },
  SPEED: {
    KNOTS: 'knots',
    KMH: 'kmh',  // kilometers per hour
    MPH: 'mph'   // miles per hour
  }
} as const

// Aircraft status values
export const AIRCRAFT_STATUS = {
  ACTIVE: 'active',
  RETIRED: 'retired',
  STORED: 'stored'
} as const

// Flight status values
export const FLIGHT_STATUS = {
  SCHEDULED: 'scheduled',
  ACTIVE: 'active',
  LANDED: 'landed',
  CANCELLED: 'cancelled',
  DELAYED: 'delayed'
} as const

// ATC message types
export const ATC_MESSAGE_TYPES = {
  CLEARANCE: 'clearance',
  CONTACT: 'contact',
  TAXI: 'taxi',
  TAKEOFF: 'takeoff',
  LANDING: 'landing',
  POSITION: 'position',
  WEATHER: 'weather',
  EMERGENCY: 'emergency'
} as const

// ATC sender types
export const ATC_SENDER_TYPES = {
  PILOT: 'pilot',
  CONTROLLER: 'controller',
  STATION: 'station'
} as const

// Notification types
export const NOTIFICATION_TYPES = {
  AIRCRAFT_ALERTS: 'aircraftAlerts',
  ATC_MESSAGES: 'atcMessages',
  SYSTEM_UPDATES: 'systemUpdates'
} as const

// Default refresh intervals (in milliseconds)
export const REFRESH_INTERVALS = {
  AIRCRAFT_DATA: 30000,    // 30 seconds
  FLIGHT_POSITIONS: 10000, // 10 seconds
  ATC_MESSAGES: 5000,      // 5 seconds
  WEATHER_DATA: 600000     // 10 minutes
} as const

// Storage keys for local storage
export const STORAGE_KEYS = {
  USER_PREFERENCES: 'userPreferences',
  AUTH_TOKEN: 'authToken',
  REFRESH_TOKEN: 'refreshToken',
  LAST_VISITED_ROUTE: 'lastVisitedRoute'
} as const

// Error messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  SERVER_ERROR: 'Server error occurred. Please try again later.',
  UNAUTHORIZED: 'Unauthorized access. Please log in.',
  NOT_FOUND: 'Requested resource not found.',
  VALIDATION_ERROR: 'Validation error occurred. Please check your input.'
} as const

// Success messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Login successful!',
  LOGOUT_SUCCESS: 'Logout successful!',
  DATA_SAVED: 'Data saved successfully!',
  BOOKING_CREATED: 'Booking created successfully!'
} as const

// Application themes
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto'
} as const

// Map layers
export const MAP_LAYERS = {
  OSM: 'osm',
  SATELLITE: 'satellite',
  TERRAIN: 'terrain'
} as const

// Aircraft icon colors by altitude
export const ALTITUDE_COLOR_RANGES = [
  { max: 10000, color: '#FF0000' },   // Red: Low altitude
  { max: 20000, color: '#FF8000' },   // Orange: Medium-low altitude
  { max: 30000, color: '#FFFF00' },   // Yellow: Medium altitude
  { max: 40000, color: '#00FF00' },   // Green: Medium-high altitude
  { max: Infinity, color: '#0000FF' }  // Blue: High altitude
]