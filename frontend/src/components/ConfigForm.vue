<template>
  <div class="config-form">
    <div v-if="!isEdit" class="name-input">
      <el-input
        v-model="configName"
        placeholder="请输入配置名称"
        :rules="[{ required: true, message: '请输入配置名称' }]"
      >
        <template #prepend>配置名称</template>
      </el-input>
    </div>
    
    <json-editor
      v-model="jsonConfig"
      height="600px"
      @change="validateJson"
    />

    <div class="form-actions">
      <el-button type="primary" @click="handleSubmit" :disabled="!isValid">保存</el-button>
      <el-button @click="$emit('cancel')">取消</el-button>
    </div>

    <div class="template-actions" v-if="!isEdit">
      <el-button type="info" @click="loadTemplate('mainlab')">加载 MainLab 模板</el-button>
      <el-button type="info" @click="loadTemplate('llmlab')">加载 LLMLab 模板</el-button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import JsonEditor from './JsonEditor.vue'

// 配置模板
const templates = {
  mainlab: {
    rlEnvInit: {
      envName: "MainLabEnv",
      envParameters: {
        param1: "value1",
        param2: "value2"
      }
    },
    algorithm: {
      system: "stable-baselines3",
      algorithmModel: "PPO",
      algorithmParameters: {
        learning_rate: "0.0003",
        n_steps: "2048"
      }
    }
  },
  llmlab: {
    llmEnvInit: {
      envName: "LLMLabEnv",
      envParameters: {
        param1: "value1",
        param2: "value2"
      }
    },
    algorithm: {
      system: "openai",
      algorithmModel: "gpt-3.5-turbo",
      algorithmParameters: {
        temperature: "0.7",
        max_tokens: "150"
      }
    }
  }
}

export default {
  name: 'ConfigForm',
  components: {
    JsonEditor
  },
  props: {
    config: {
      type: Object,
      default: () => ({})
    },
    configType: {
      type: String,
      required: true,
      validator: (value) => ['mainlab', 'llmlab'].includes(value)
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const configName = ref('')
    const jsonConfig = ref({})
    const isValid = ref(false)

    const isEdit = computed(() => Boolean(props.config.name))

    // 初始化编辑器内容
    if (isEdit.value) {
      jsonConfig.value = { ...props.config }
    } else {
      jsonConfig.value = { ...templates[props.configType] }
    }

    const validateJson = (value) => {
      try {
        // 验证必要的字段
        const hasRequiredFields = value && 
          ((props.configType === 'mainlab' && value.rlEnvInit) || 
           (props.configType === 'llmlab' && value.llmEnvInit)) && 
          value.algorithm

        isValid.value = hasRequiredFields
      } catch (e) {
        isValid.value = false
      }
    }

    const loadTemplate = (type) => {
      jsonConfig.value = { ...templates[type] }
    }

    const handleSubmit = () => {
      if (!isEdit.value && !configName.value) {
        ElMessage.error('请输入配置名称')
        return
      }

      const finalConfig = {
        ...jsonConfig.value
      }

      if (!isEdit.value) {
        finalConfig.name = configName.value
      }

      emit('submit', finalConfig)
    }

    return {
      configName,
      jsonConfig,
      isValid,
      isEdit,
      validateJson,
      loadTemplate,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.config-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.name-input {
  max-width: 400px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.template-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
</style> 