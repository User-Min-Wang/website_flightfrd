<template>
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-lg leading-6 font-medium text-gray-900 mb-4">实时航班信息</h2>
      
      <div class="space-y-4">
        <div v-for="aircraft in aircraftList" :key="aircraft.hex" class="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="font-semibold text-gray-900">
                {{ aircraft.flight || '未知航班' }}
                <span class="text-sm text-gray-500 ml-2">({{ aircraft.hex }})</span>
              </h3>
              <p class="text-sm text-gray-500 mt-1">
                {{ aircraft.latitude && aircraft.longitude ? `${aircraft.latitude.toFixed(4)}, ${aircraft.longitude.toFixed(4)}` : '位置未知' }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-500">高度</p>
              <p class="text-lg font-semibold">
                {{ aircraft.altitude ? formatAltitude(aircraft.altitude) : 'N/A' }}
              </p>
            </div>
          </div>
          
          <div class="mt-3 grid grid-cols-2 gap-2 text-sm">
            <div>
              <span class="text-gray-500">速度:</span>
              <span class="ml-1">{{ aircraft.speed ? formatSpeed(aircraft.speed) : 'N/A' }}</span>
            </div>
            <div>
              <span class="text-gray-500">航向:</span>
              <span class="ml-1">{{ aircraft.track ? formatTrack(aircraft.track) : 'N/A' }}</span>
            </div>
            <div>
              <span class="text-gray-500">垂直速度:</span>
              <span class="ml-1">{{ aircraft.vert_rate ? formatVerticalRate(aircraft.vert_rate) : 'N/A' }}</span>
            </div>
            <div>
              <span class="text-gray-500">来源:</span>
              <span class="ml-1">{{ aircraft.type }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="aircraftList.length === 0" class="text-center py-8 text-gray-500">
          暂无航班信息
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Aircraft } from '@/types/aircraft';
import { formatAltitude, formatSpeed, formatTrack, formatVerticalRate } from '@/utils/formatters';

interface Props {
  aircraftList: Aircraft[];
}

defineProps<Props>();
</script>