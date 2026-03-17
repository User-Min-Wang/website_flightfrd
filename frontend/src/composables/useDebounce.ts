import { ref, watch } from 'vue'

/**
 * Composable for debouncing function calls
 */
export const useDebounce = <T>(fn: (arg: T) => void, delay: number) => {
  let timeoutId: NodeJS.Timeout | null = null

  const debounce = (arg: T) => {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }

    timeoutId = setTimeout(() => {
      fn(arg)
    }, delay)
  }

  const cancel = () => {
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
  }

  return {
    debounce,
    cancel
  }
}

/**
 * Composable for debouncing a reactive value
 */
export const useDebouncedRef = <T>(initialValue: T, delay: number) => {
  const source = ref(initialValue)
  const debounced = ref(initialValue)

  let timeoutId: NodeJS.Timeout | null = null

  watch(source, (newValue) => {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }

    timeoutId = setTimeout(() => {
      debounced.value = newValue
    }, delay)
  })

  return {
    source,
    debounced
  }
}