<template>
  <div class="relative h-full w-full">
    <div id="map" class="h-full w-full"></div>
    <div class="absolute top-4 right-4 z-[1000]">
      <slot name="controls" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons in webpack environment
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface Props {
  center?: [number, number];
  zoom?: number;
}

const props = withDefaults(defineProps<Props>(), {
  center: () => [39.9042, 116.4074], // Beijing coordinates as default
  zoom: 10,
});

const mapInstance = ref<L.Map | null>(null);

onMounted(() => {
  // Initialize the map
  mapInstance.value = L.map('map').setView(props.center, props.zoom);

  // Add tile layer (OpenStreetMap)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
  }).addTo(mapInstance.value);

  // Make map instance available to parent component
  emit('map-ready', mapInstance.value);
});

onUnmounted(() => {
  if (mapInstance.value) {
    mapInstance.value.remove();
  }
});

const emit = defineEmits<{
  (e: 'map-ready', map: L.Map): void;
}>();

defineExpose({
  map: mapInstance
});
</script>