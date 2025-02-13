<template>
  <div class="configs-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配置管理</span>
          <el-button type="primary" @click="handleAddConfig">新建配置</el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="MainLab" name="mainlab">
          <config-list
            :configs="mainlabConfigs"
            @edit="handleEditConfig"
            @delete="handleDeleteConfig"
          />
        </el-tab-pane>
        <el-tab-pane label="LLMLab" name="llmlab">
          <config-list
            :configs="llmlabConfigs"
            @edit="handleEditConfig"
            @delete="handleDeleteConfig"
          />
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑配置' : '新建配置'"
      width="80%"
    >
      <config-form
        v-if="dialogVisible"
        :config="currentConfig"
        :config-type="activeTab"
        @submit="handleSubmit"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ConfigList from '../components/ConfigList.vue'
import ConfigForm from '../components/ConfigForm.vue'
import { getConfigs, addConfig, updateConfig, deleteConfig } from '../api'

export default {
  name: 'Configs',
  components: {
    ConfigList,
    ConfigForm
  },
  setup() {
    const configs = ref({
      mainlab: {},
      llmlab: {}
    })
    const activeTab = ref('mainlab')
    const dialogVisible = ref(false)
    const currentConfig = ref(null)
    const isEdit = computed(() => Boolean(currentConfig.value?.name))

    const mainlabConfigs = computed(() => {
      return Object.entries(configs.value.mainlab).map(([name, config]) => ({
        name,
        ...config
      }))
    })

    const llmlabConfigs = computed(() => {
      return Object.entries(configs.value.llmlab).map(([name, config]) => ({
        name,
        ...config
      }))
    })

    const loadConfigs = async () => {
      try {
        configs.value = await getConfigs()
      } catch (error) {
        console.error('Failed to load configs:', error)
        ElMessage.error('加载配置失败')
      }
    }

    const handleAddConfig = () => {
      currentConfig.value = {}
      dialogVisible.value = true
    }

    const handleEditConfig = (config) => {
      currentConfig.value = { ...config }
      dialogVisible.value = true
    }

    const handleDeleteConfig = async (config) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除配置 "${config.name}" 吗？`,
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await deleteConfig(activeTab.value, config.name)
        ElMessage.success('删除成功')
        loadConfigs()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Failed to delete config:', error)
          ElMessage.error('删除失败')
        }
      }
    }

    const handleSubmit = async (configData) => {
      try {
        if (isEdit.value) {
          await updateConfig(activeTab.value, configData.name, configData)
          ElMessage.success('更新成功')
        } else {
          await addConfig(activeTab.value, configData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadConfigs()
      } catch (error) {
        console.error('Failed to save config:', error)
        ElMessage.error('保存失败')
      }
    }

    // 初始加载
    loadConfigs()

    return {
      configs,
      activeTab,
      dialogVisible,
      currentConfig,
      isEdit,
      mainlabConfigs,
      llmlabConfigs,
      handleAddConfig,
      handleEditConfig,
      handleDeleteConfig,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.configs-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 