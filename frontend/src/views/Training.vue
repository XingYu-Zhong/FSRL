<template>
  <div class="training-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>模型训练</span>
        </div>
      </template>
      
      <!-- 选择配置部分 -->
      <div v-if="!currentConfig" class="config-selection">
        <el-table :data="configList" style="width: 100%">
          <el-table-column prop="name" label="配置名称" />
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="selectConfig(row)">
                选择训练
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 训练参数设置部分 -->
      <div v-else class="training-form">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
          <el-form-item label="配置名称">
            <span>{{ currentConfig.name }}</span>
          </el-form-item>

          <el-form-item label="训练类型" prop="env_type">
            <el-select v-model="form.env_type" placeholder="请选择训练类型">
              <el-option label="训练" value="train" />
              <el-option label="加载" value="load" />
              <el-option label="测试" value="test" />
              <el-option 
                label="LLM" 
                value="llm" 
                :disabled="currentConfig.type !== 'llmlab'"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="开始时间" prop="start_time">
            <el-date-picker
              v-model="form.start_time"
              type="datetime"
              placeholder="选择开始时间"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>

          <el-form-item label="结束时间" prop="end_time">
            <el-date-picker
              v-model="form.end_time"
              type="datetime"
              placeholder="选择结束时间"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>

          <el-form-item 
            v-if="form.env_type === 'load'" 
            label="加载时间步数" 
            prop="load_time_steps"
          >
            <el-input-number 
              v-model="form.load_time_steps" 
              :min="1"
              :step="1"
            />
          </el-form-item>

          <el-form-item label="代理设置" prop="proxy">
            <el-input 
              v-model="form.proxy" 
              placeholder="可选，例如：7890"
            >
              <template #prepend>http://127.0.0.1:</template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleStartTraining">开始训练</el-button>
            <el-button @click="currentConfig = null">返回</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { getConfigs, startTraining } from '../api'
import { ElMessage } from 'element-plus'

export default {
  name: 'Training',
  setup() {
    const configs = ref({
      mainlab: {},
      llmlab: {}
    })
    const currentConfig = ref(null)
    const formRef = ref(null)

    const form = ref({
      env_type: 'train',
      start_time: '',
      end_time: '',
      load_time_steps: '',
      proxy: ''
    })

    const rules = {
      env_type: [{ required: true, message: '请选择训练类型', trigger: 'change' }],
      start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
      end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
      load_time_steps: [{ required: true, message: '请输入加载时间步数', trigger: 'blur' }],
      proxy: [{ pattern: /^\d*$/, message: '请输入正确的端口号', trigger: 'blur' }]
    }

    const configList = computed(() => {
      return [
        ...Object.entries(configs.value.mainlab).map(([name, config]) => ({
          name,
          ...config,
          type: 'mainlab'
        })),
        ...Object.entries(configs.value.llmlab).map(([name, config]) => ({
          name,
          ...config,
          type: 'llmlab'
        }))
      ]
    })

    const loadConfigs = async () => {
      try {
        configs.value = await getConfigs()
      } catch (error) {
        console.error('Failed to load configs:', error)
        ElMessage.error('加载配置失败')
      }
    }

    const selectConfig = (config) => {
      currentConfig.value = config
      // 根据配置类型设置默认训练类型
      form.value.env_type = config.type === 'llmlab' ? 'llm' : 'train'
    }

    const handleStartTraining = async () => {
      if (!formRef.value) return

      try {
        await formRef.value.validate()
        
        const trainingConfig = {
          task_name: currentConfig.value.name,
          ...form.value
        }

        await startTraining(trainingConfig)
        ElMessage.success('训练任务已启动')
        currentConfig.value = null
        
        // 重置表单
        form.value = {
          env_type: 'train',
          start_time: '',
          end_time: '',
          load_time_steps: '',
          proxy: ''
        }
      } catch (error) {
        console.error('Failed to start training:', error)
        ElMessage.error('启动训练失败：' + (error.message || '未知错误'))
      }
    }

    // 初始加载
    loadConfigs()

    return {
      configs,
      configList,
      currentConfig,
      form,
      formRef,
      rules,
      selectConfig,
      handleStartTraining
    }
  }
}
</script>

<style scoped>
.training-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.training-form {
  max-width: 600px;
  margin: 0 auto;
}
</style> 