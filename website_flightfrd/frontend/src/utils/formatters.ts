/**
 * Utility functions for formatting data in the aircraft tracking application
 */

/**
 * Format a date string to a more readable format
 */
export const formatDate = (dateString: string, includeTime: boolean = true): string => {
  const date = new Date(dateString)
  
  if (includeTime) {
    return date.toLocaleString()
  }
  
  return date.toLocaleDateString()
}

/**
 * Format time difference between two dates
 */
export const formatTimeDifference = (startDate: string, endDate: string): string => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffMs = end.getTime() - start.getTime()
  
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
  
  if (diffDays > 0) {
    return `${diffDays}d ${diffHours}h ${diffMinutes}m`
  }
  
  if (diffHours > 0) {
    return `${diffHours}h ${diffMinutes}m`
  }
  
  return `${diffMinutes}m`
}

/**
 * Format altitude in feet to a more readable format
 */
export const formatAltitude = (altitudeFeet: number | null, unit: 'feet' | 'meters' = 'feet'): string => {
  if (altitudeFeet === null) return 'N/A'
  
  if (unit === 'meters') {
    const meters = Math.round(altitudeFeet * 0.3048)
    return `${meters.toLocaleString()} m`
  }
  
  return `${Math.round(altitudeFeet).toLocaleString()} ft`
}

/**
 * Format speed in knots to various units
 */
export const formatSpeed = (speedKnots: number | null, unit: 'knots' | 'kmh' | 'mph' = 'knots'): string => {
  if (speedKnots === null) return 'N/A'
  
  switch (unit) {
    case 'kmh':
      return `${Math.round(speedKnots * 1.852).toLocaleString()} km/h`
    case 'mph':
      return `${Math.round(speedKnots * 1.15078).toLocaleString()} mph`
    case 'knots':
    default:
      return `${Math.round(speedKnots).toLocaleString()} kts`
  }
}

/**
 * Format distance in kilometers to various units
 */
export const formatDistance = (distanceKm: number | null, unit: 'km' | 'nm' | 'mi' = 'km'): string => {
  if (distanceKm === null) return 'N/A'
  
  switch (unit) {
    case 'nm':
      return `${Math.round(distanceKm * 0.539957).toLocaleString()} nm`
    case 'mi':
      return `${Math.round(distanceKm * 0.621371).toLocaleString()} mi`
    case 'km':
    default:
      return `${Math.round(distanceKm).toLocaleString()} km`
  }
}

/**
 * Format coordinates to degrees, minutes, seconds
 */
export const formatCoordinates = (degrees: number, isLatitude: boolean): string => {
  if (degrees === null || degrees === undefined) return 'N/A'
  
  const absDegrees = Math.abs(degrees)
  const deg = Math.floor(absDegrees)
  const min = Math.floor((absDegrees - deg) * 60)
  const sec = ((absDegrees - deg - min / 60) * 3600).toFixed(2)
  
  const direction = isLatitude 
    ? (degrees >= 0 ? 'N' : 'S') 
    : (degrees >= 0 ? 'E' : 'W')
  
  return `${deg}°${min}'${sec}" ${direction}`
}

/**
 * Format heading in degrees to compass direction
 */
export const formatHeading = (heading: number | null): string => {
  if (heading === null) return 'N/A'
  
  const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
  const index = Math.round(heading / 22.5) % 16
  
  return directions[index]
}

/**
 * Format ICAO code with proper casing
 */
export const formatICAO = (icao: string): string => {
  return icao.toUpperCase()
}

/**
 * Format aircraft registration
 */
export const formatRegistration = (reg: string): string => {
  if (!reg) return 'N/A'
  
  // Add space or hyphen formatting if needed
  return reg.toUpperCase()
}

/**
 * Format flight number
 */
export const formatFlightNumber = (flightNum: string): string => {
  if (!flightNum) return 'N/A'
  
  return flightNum.toUpperCase()
}

/**
 * Format squawk code
 */
export const formatSquawk = (squawk: string): string => {
  if (!squawk) return 'N/A'
  
  return squawk.padStart(4, '0')
}

/**
 * Format frequency in MHz
 */
export const formatFrequency = (freq: string): string => {
  // Ensure frequency is formatted with 3 decimal places
  const numFreq = parseFloat(freq)
  if (isNaN(numFreq)) return 'N/A'
  
  return numFreq.toFixed(3)
}

/**
 * Truncate text to specified length with ellipsis
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (!text) return ''
  
  if (text.length <= maxLength) {
    return text
  }
  
  return `${text.substring(0, maxLength)}...`
}