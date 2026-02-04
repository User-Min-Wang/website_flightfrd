import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  autoRefresh: boolean;
  refreshInterval: number; // in seconds
  showLabels: boolean;
  showTrails: boolean;
  mapLayer: 'osm' | 'satellite' | 'terrain';
  language: string;
  notificationsEnabled: boolean;
  notificationTypes: {
    aircraftAlerts: boolean;
    atcMessages: boolean;
    systemUpdates: boolean;
  };
  units: {
    distance: 'km' | 'nm' | 'mi'; // kilometers, nautical miles, miles
    altitude: 'feet' | 'meters';
    speed: 'knots' | 'kmh' | 'mph';
  };
}

export const useSettingsStore = defineStore('settings', () => {
  // State
  const preferences = ref<UserPreferences>({
    theme: 'auto',
    autoRefresh: true,
    refreshInterval: 30, // 30 seconds
    showLabels: true,
    showTrails: false,
    mapLayer: 'osm',
    language: 'en',
    notificationsEnabled: true,
    notificationTypes: {
      aircraftAlerts: true,
      atcMessages: true,
      systemUpdates: true
    },
    units: {
      distance: 'km',
      altitude: 'feet',
      speed: 'knots'
    }
  })

  const loading = ref<boolean>(false)
  const error = ref<string | null>(null)

  // Getters
  const getCurrentTheme = computed(() => preferences.value.theme)
  
  const isAutoRefreshEnabled = computed(() => preferences.value.autoRefresh)
  
  const getRefreshInterval = computed(() => preferences.value.refreshInterval)
  
  const getUnits = computed(() => preferences.value.units)

  // Actions
  const setPreferences = (prefs: Partial<UserPreferences>) => {
    preferences.value = { ...preferences.value, ...prefs }
    // Persist to localStorage
    localStorage.setItem('userPreferences', JSON.stringify(preferences.value))
  }

  const setTheme = (theme: 'light' | 'dark' | 'auto') => {
    preferences.value.theme = theme
    localStorage.setItem('userPreferences', JSON.stringify(preferences.value))
  }

  const setAutoRefresh = (enabled: boolean) => {
    preferences.value.autoRefresh = enabled
  }

  const setRefreshInterval = (interval: number) => {
    preferences.value.refreshInterval = interval
  }

  const setShowLabels = (show: boolean) => {
    preferences.value.showLabels = show
  }

  const setShowTrails = (show: boolean) => {
    preferences.value.showTrails = show
  }

  const setMapLayer = (layer: 'osm' | 'satellite' | 'terrain') => {
    preferences.value.mapLayer = layer
  }

  const setLanguage = (lang: string) => {
    preferences.value.language = lang
  }

  const setNotificationsEnabled = (enabled: boolean) => {
    preferences.value.notificationsEnabled = enabled
  }

  const setNotificationType = (type: keyof UserPreferences['notificationTypes'], enabled: boolean) => {
    preferences.value.notificationTypes[type] = enabled
  }

  const setUnitSystem = (category: keyof UserPreferences['units'], unit: any) => {
    (preferences.value.units[category] as any) = unit
  }

  const setLoading = (status: boolean) => {
    loading.value = status
  }

  const setError = (message: string | null) => {
    error.value = message
  }

  const clearError = () => {
    error.value = null
  }

  // Initialize from localStorage if available
  const initializeFromStorage = () => {
    const savedPrefs = localStorage.getItem('userPreferences')
    if (savedPrefs) {
      try {
        const parsedPrefs = JSON.parse(savedPrefs) as UserPreferences
        // Merge with default values to ensure all properties exist
        preferences.value = { ...preferences.value, ...parsedPrefs }
      } catch (e) {
        console.error('Failed to parse user preferences from localStorage:', e)
        // Use defaults if parsing fails
      }
    }
  }

  // Apply theme to document
  const applyTheme = () => {
    const theme = preferences.value.theme
    const html = document.documentElement
    
    // Remove existing theme classes
    html.classList.remove('theme-light', 'theme-dark')
    
    // Apply theme based on preference
    if (theme === 'auto') {
      // Check system preference
      const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches
      html.classList.add(isDarkMode ? 'theme-dark' : 'theme-light')
    } else {
      html.classList.add(`theme-${theme}`)
    }
  }

  return {
    // State
    preferences,
    loading,
    error,

    // Getters
    getCurrentTheme,
    isAutoRefreshEnabled,
    getRefreshInterval,
    getUnits,

    // Actions
    setPreferences,
    setTheme,
    setAutoRefresh,
    setRefreshInterval,
    setShowLabels,
    setShowTrails,
    setMapLayer,
    setLanguage,
    setNotificationsEnabled,
    setNotificationType,
    setUnitSystem,
    setLoading,
    setError,
    clearError,
    initializeFromStorage,
    applyTheme
  }
})