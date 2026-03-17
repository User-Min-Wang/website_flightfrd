<template>
  <div class="flight-list-container">
    <!-- 顶部操作栏 -->
    <div class="header-section">
      <div class="title-area">
        <h2 class="page-title">
          <el-icon><Airplane /></el-icon>
          今日航班列表
        </h2>
        <span class="date-display">{{ currentDate }}</span>
      </div>
      
      <div class="action-buttons">
        <el-button 
          type="primary" 
          :icon="Refresh" 
          @click="refreshFlights"
          :loading="loading"
        >
          刷新数据
        </el-button>
        <el-button 
          type="success" 
          :icon="Download"
          @click="exportToCSV"
        >
          导出 CSV
        </el-button>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-card shadow="hover">
        <div class="filter-content">
          <!-- 特殊班次筛选 -->
          <div class="filter-group">
            <span class="filter-label">特殊班次：</span>
            <el-checkbox-group v-model="specialFilters">
              <el-checkbox label="painted" border>
                <el-icon><Brush /></el-icon> 彩绘飞机
              </el-checkbox>
              <el-checkbox label="special_aircraft" border>
                <el-icon><Star /></el-icon> 特殊机型
              </el-checkbox>
              <el-checkbox label="rare_airline" border>
                <el-icon><Flag /></el-icon> 罕见航司
              </el-checkbox>
            </el-checkbox-group>
          </div>

          <!-- 快速筛选按钮 -->
          <div class="quick-filters">
            <el-button 
              :type="showSpecialOnly ? 'primary' : 'default'"
              @click="toggleSpecialOnly"
            >
              {{ showSpecialOnly ? '显示全部' : '只看特殊班次' }}
              <el-badge 
                v-if="!showSpecialOnly && specialCount > 0"
                :value="specialCount"
                class="badge-count"
              />
            </el-button>
          </div>

          <!-- 搜索和状态筛选 -->
          <div class="search-area">
            <el-input
              v-model="searchQuery"
              placeholder="搜索航班号/目的地/航空公司..."
              prefix-icon="Search"
              clearable
              class="search-input"
            />
            
            <el-select 
              v-model="statusFilter" 
              placeholder="航班状态" 
              clearable
              class="status-select"
            >
              <el-option label="计划" value="scheduled" />
              <el-option label="延误" value="delayed" />
              <el-option label="取消" value="cancelled" />
              <el-option label="起飞" value="departed" />
              <el-option label="到达" value="arrived" />
            </el-select>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 统计信息 -->
    <div class="stats-row" v-if="flights.length > 0">
      <el-card shadow="hover" class="stat-card">
        <div class="stat-item">
          <span class="stat-value">{{ flights.length }}</span>
          <span class="stat-label">总航班数</span>
        </div>
      </el-card>
      <el-card shadow="hover" class="stat-card special-card">
        <div class="stat-item">
          <span class="stat-value special-text">{{ specialCount }}</span>
          <span class="stat-label">特殊班次</span>
        </div>
      </el-card>
      <el-card shadow="hover" class="stat-card">
        <div class="stat-item">
          <span class="stat-value delayed-text">{{ delayedCount }}</span>
          <span class="stat-label">延误航班</span>
        </div>
      </el-card>
      <el-card shadow="hover" class="stat-card">
        <div class="stat-item">
          <span class="stat-value cancelled-text">{{ cancelledCount }}</span>
          <span class="stat-label">取消航班</span>
        </div>
      </el-card>
    </div>

    <!-- 航班列表 -->
    <div class="table-section">
      <el-table
        :data="filteredFlights"
        style="width: 100%"
        v-loading="loading"
        element-loading-text="加载中..."
        stripe
        border
        :default-sort="{prop: 'scheduledTime', order: 'ascending'}"
      >
        <el-table-column prop="flightNumber" label="航班号" width="120" sortable>
          <template #default="{ row }">
            <span class="flight-number" :class="{ 'special-flight': row.isSpecial }">
              {{ row.flightNumber }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="airline" label="航空公司" width="150" sortable />
        
        <el-table-column prop="origin" label="出发地" width="100" sortable />
        
        <el-table-column prop="destination" label="目的地" width="100" sortable />
        
        <el-table-column prop="scheduledTime" label="计划时间" width="120" sortable>
          <template #default="{ row }">
            {{ formatTime(row.scheduledTime) }}
          </template>
        </el-table-column>

        <el-table-column prop="estimatedTime" label="预计时间" width="120">
          <template #default="{ row }">
            <span :class="{ 'time-changed': row.scheduledTime !== row.estimatedTime }">
              {{ formatTime(row.estimatedTime) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="aircraft" label="机型" width="120" sortable>
          <template #default="{ row }">
            <span :class="{ 'special-aircraft': row.isSpecialAircraft }">
              {{ row.aircraft }}
              <el-tag v-if="row.isSpecialAircraft" size="small" type="warning">特殊</el-tag>
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="100" sortable>
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="gate" label="登机口" width="80" sortable />

        <el-table-column label="特殊标记" min-width="200">
          <template #default="{ row }">
            <div class="tags-container">
              <el-tag 
                v-if="row.isPainted" 
                type="danger" 
                size="small"
                effect="dark"
              >
                <el-icon><Brush /></el-icon> 彩绘
              </el-tag>
              <el-tag 
                v-if="row.isSpecialAircraft" 
                type="warning" 
                size="small"
              >
                <el-icon><Star /></el-icon> 特殊机型
              </el-tag>
              <el-tag 
                v-if="row.isRareAirline" 
                type="success" 
                size="small"
              >
                <el-icon><Flag /></el-icon> 罕见航司
              </el-tag>
              <el-tag 
                v-if="row.customTags && row.customTags.length" 
                type="info" 
                size="small"
              >
                {{ row.customTags.join(', ') }}
              </el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              link 
              @click="viewDetails(row)"
            >
              详情
            </el-button>
            <el-button 
              type="warning" 
              link 
              @click="markSpecial(row)"
              v-if="!row.isSpecial"
            >
              标记
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination-section" v-if="totalPages > 1">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[20, 50, 100, 200]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredFlights.length"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="航班详情"
      width="600px"
    >
      <div v-if="selectedFlight" class="flight-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="航班号">
            {{ selectedFlight.flightNumber }}
          </el-descriptions-item>
          <el-descriptions-item label="航空公司">
            {{ selectedFlight.airline }}
          </el-descriptions-item>
          <el-descriptions-item label="航线">
            {{ selectedFlight.origin }} → {{ selectedFlight.destination }}
          </el-descriptions-item>
          <el-descriptions-item label="机型">
            {{ selectedFlight.aircraft }}
          </el-descriptions-item>
          <el-descriptions-item label="计划时间">
            {{ formatTime(selectedFlight.scheduledTime) }}
          </el-descriptions-item>
          <el-descriptions-item label="预计时间">
            {{ formatTime(selectedFlight.estimatedTime) }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(selectedFlight.status)">
              {{ getStatusText(selectedFlight.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="登机口">
            {{ selectedFlight.gate || '未分配' }}
          </el-descriptions-item>
          <el-descriptions-item label="特殊标记" :span="2">
            <div class="detail-tags">
              <el-tag v-if="selectedFlight.isPainted" type="danger">彩绘飞机</el-tag>
              <el-tag v-if="selectedFlight.isSpecialAircraft" type="warning">特殊机型</el-tag>
              <el-tag v-if="selectedFlight.isRareAirline" type="success">罕见航司</el-tag>
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">
            {{ selectedFlight.remarks || '无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { 
  Airplane, Refresh, Download, Search, Brush, Star, Flag 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 数据类型定义
interface Flight {
  id: number
  flightNumber: string
  airline: string
  origin: string
  destination: string
  scheduledTime: string
  estimatedTime: string
  aircraft: string
  status: string
  gate: string
  isPainted: boolean
  isSpecialAircraft: boolean
  isRareAirline: boolean
  isSpecial: boolean
  customTags?: string[]
  remarks?: string
}

// 响应式数据
const loading = ref(false)
const flights = ref<Flight[]>([])
const searchQuery = ref('')
const statusFilter = ref('')
const specialFilters = ref<string[]>([])
const showSpecialOnly = ref(false)
const currentPage = ref(1)
const pageSize = ref(50)
const detailVisible = ref(false)
const selectedFlight = ref<Flight | null>(null)

// 计算属性
const currentDate = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

const filteredFlights = computed(() => {
  let result = [...flights.value]

  // 特殊班次筛选
  if (showSpecialOnly.value || specialFilters.value.length > 0) {
    result = result.filter(flight => {
      if (showSpecialOnly.value) {
        return flight.isSpecial
      }
      
      return specialFilters.value.some(filter => {
        if (filter === 'painted') return flight.isPainted
        if (filter === 'special_aircraft') return flight.isSpecialAircraft
        if (filter === 'rare_airline') return flight.isRareAirline
        return false
      })
    })
  }

  // 搜索筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(flight =>
      flight.flightNumber.toLowerCase().includes(query) ||
      flight.airline.toLowerCase().includes(query) ||
      flight.origin.toLowerCase().includes(query) ||
      flight.destination.toLowerCase().includes(query)
    )
  }

  // 状态筛选
  if (statusFilter.value) {
    result = result.filter(flight => flight.status === statusFilter.value)
  }

  return result
})

const specialCount = computed(() => {
  return flights.value.filter(f => f.isSpecial).length
})

const delayedCount = computed(() => {
  return flights.value.filter(f => f.status === 'delayed').length
})

const cancelledCount = computed(() => {
  return flights.value.filter(f => f.status === 'cancelled').length
})

const totalPages = computed(() => {
  return Math.ceil(filteredFlights.value.length / pageSize.value)
})

// 方法
const refreshFlights = async () => {
  loading.value = true
  try {
    // 模拟 API 调用 - 实际项目中替换为真实 API
    await simulateApiCall()
    ElMessage.success('航班数据已更新')
  } catch (error) {
    ElMessage.error('获取航班数据失败')
  } finally {
    loading.value = false
  }
}

const simulateApiCall = async () => {
  // 模拟延迟
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // 生成模拟数据
  flights.value = generateMockFlights()
}

const generateMockFlights = (): Flight[] => {
  const airlines = ['中国国航', '东方航空', '南方航空', '海南航空', '四川航空', '厦门航空', '吉祥航空', '春秋航空']
  const rareAirlines = ['长龙航空', '奥凯航空', '成都航空', '天津航空', '首都航空']
  const cities = ['北京', '上海', '广州', '深圳', '成都', '杭州', '西安', '重庆', '昆明', '武汉']
  const aircrafts = ['A320', 'B737', 'A330', 'B787', 'A350', 'B777', 'ARJ21', 'C919']
  const specialAircrafts = ['A380', 'B747', 'A220', 'E190']
  const statuses = ['scheduled', 'delayed', 'departed', 'arrived', 'cancelled']
  
  const mockFlights: Flight[] = []
  
  for (let i = 1; i <= 150; i++) {
    const isRare = Math.random() < 0.1
    const isSpecialAircraft = Math.random() < 0.08
    const isPainted = Math.random() < 0.05
    
    const airline = isRare 
      ? rareAirlines[Math.floor(Math.random() * rareAirlines.length)]
      : airlines[Math.floor(Math.random() * airlines.length)]
    
    const aircraft = isSpecialAircraft
      ? specialAircrafts[Math.floor(Math.random() * specialAircrafts.length)]
      : aircrafts[Math.floor(Math.random() * aircrafts.length)]
    
    const status = statuses[Math.floor(Math.random() * statuses.length)]
    
    mockFlights.push({
      id: i,
      flightNumber: `${airline.substring(0, 2).toUpperCase()}${Math.floor(1000 + Math.random() * 9000)}`,
      airline,
      origin: cities[Math.floor(Math.random() * cities.length)],
      destination: cities[Math.floor(Math.random() * cities.length)],
      scheduledTime: new Date(Date.now() + Math.random() * 86400000).toISOString(),
      estimatedTime: new Date(Date.now() + Math.random() * 86400000).toISOString(),
      aircraft,
      status,
      gate: `${String.fromCharCode(65 + Math.floor(Math.random() * 6))}${Math.floor(1 + Math.random() * 50)}`,
      isPainted,
      isSpecialAircraft,
      isRareAirline: isRare,
      isSpecial: isPainted || isSpecialAircraft || isRare,
      customTags: isPainted ? ['熊猫涂装', '迪士尼涂装'] : [],
      remarks: isSpecialAircraft ? '稀有机型执飞' : ''
    })
  }
  
  return mockFlights
}

const toggleSpecialOnly = () => {
  showSpecialOnly.value = !showSpecialOnly.value
  if (showSpecialOnly.value) {
    specialFilters.value = []
  }
}

const viewDetails = (flight: Flight) => {
  selectedFlight.value = flight
  detailVisible.value = true
}

const markSpecial = async (flight: Flight) => {
  try {
    await ElMessageBox.prompt('请输入特殊标记原因', '标记为特殊班次', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /.+/,
      inputErrorMessage: '请输入内容'
    })
    
    flight.isSpecial = true
    flight.customTags = [...(flight.customTags || []), '手动标记']
    ElMessage.success('标记成功')
  } catch {
    // 用户取消
  }
}

const exportToCSV = () => {
  const headers = ['航班号', '航空公司', '出发地', '目的地', '计划时间', '预计时间', '机型', '状态', '登机口', '特殊标记']
  const rows = filteredFlights.value.map(f => [
    f.flightNumber,
    f.airline,
    f.origin,
    f.destination,
    f.scheduledTime,
    f.estimatedTime,
    f.aircraft,
    f.status,
    f.gate,
    [f.isPainted ? '彩绘' : '', f.isSpecialAircraft ? '特殊机型' : '', f.isRareAirline ? '罕见航司' : ''].filter(Boolean).join(';')
  ])
  
  const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
  const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `航班列表_${new Date().toLocaleDateString()}.csv`
  link.click()
  
  ElMessage.success('导出成功')
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    scheduled: '',
    delayed: 'warning',
    cancelled: 'danger',
    departed: 'success',
    arrived: 'success'
  }
  return types[status] || ''
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    scheduled: '计划',
    delayed: '延误',
    cancelled: '取消',
    departed: '已起飞',
    arrived: '已到达'
  }
  return texts[status] || status
}

// 生命周期
onMounted(() => {
  refreshFlights()
  
  // 设置定时刷新（每5分钟）
  const interval = setInterval(() => {
    refreshFlights()
  }, 300000)
  
  // 组件卸载时清除定时器
  return () => clearInterval(interval)
})
</script>

<style scoped>
.flight-list-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.title-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-display {
  color: #909399;
  font-size: 14px;
  margin-left: 10px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-label {
  font-weight: bold;
  color: #606266;
}

.quick-filters {
  display: flex;
  gap: 10px;
}

.badge-count {
  margin-left: 5px;
}

.search-area {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 250px;
}

.status-select {
  width: 150px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

.special-text {
  color: #E6A23C;
}

.delayed-text {
  color: #F56C6C;
}

.cancelled-text {
  color: #909399;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.table-section {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.flight-number {
  font-weight: bold;
  color: #303133;
}

.special-flight {
  color: #E6A23C;
  font-weight: bold;
}

.special-aircraft {
  color: #F56C6C;
}

.tags-container {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.flight-detail {
  padding: 10px;
}

.detail-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.time-changed {
  color: #F56C6C;
  font-weight: bold;
}

:deep(.el-checkbox__label) {
  display: flex;
  align-items: center;
  gap: 5px;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
  color: #606266;
  font-weight: 600;
}

:deep(.el-table__row:hover) {
  background-color: #ecf5ff;
}
</style>
