import { App } from 'vue'
import type { Map, TileLayer, Marker, Popup, Polyline, LayerGroup } from 'leaflet'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $map: {
      initMap: (containerId: string, options?: any) => Map
      addTileLayer: (map: Map, url: string, options?: any) => TileLayer
      addMarker: (map: Map, latlng: [number, number], options?: any) => Marker
      addPopup: (marker: Marker, content: string) => Popup
      addPolyline: (map: Map, latlngs: [number, number][], options?: any) => Polyline
      createLayerGroup: (layers?: any[]) => LayerGroup
      fitBounds: (map: Map, bounds: [[number, number], [number, number]]) => void
    }
  }
}

// This plugin provides a wrapper around Leaflet functionality
// It could also be implemented using a composable instead of a plugin
const mapPlugin = {
  install(app: App) {
    // We're not adding anything directly to the app instance
    // Instead, we'll provide the map utilities separately
    // This plugin mainly serves as a type declaration
  }
}

export default mapPlugin