<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>训练任务统计</span>
            </div>
          </template>
          <div class="item">
            <span>运行中的任务：{{ runningTasks }}</span>
          </div>
          <div class="item">
            <span>已完成的任务：{{ completedTasks }}</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
            </div>
          </template>
          <div class="item">
            <span>CPU使用率：{{ cpuUsage }}%</span>
          </div>
          <div class="item">
            <span>内存使用率：{{ memoryUsage }}%</span>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>配置统计</span>
            </div>
          </template>
          <div class="item">
            <span>MainLab配置数：{{ mainlabConfigs }}</span>
          </div>
          <div class="item">
            <span>LLMLab配置数：{{ llmlabConfigs }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const runningTasks = ref(0)
    const completedTasks = ref(0)
    const cpuUsage = ref(0)
    const memoryUsage = ref(0)
    const mainlabConfigs = ref(0)
    const llmlabConfigs = ref(0)

    return {
      runningTasks,
      completedTasks,
      cpuUsage,
      memoryUsage,
      mainlabConfigs,
      llmlabConfigs
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item {
  margin-bottom: 18px;
}
</style> 