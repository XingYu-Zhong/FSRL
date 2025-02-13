<template>
  <div class="json-editor-container" :style="{ height }">
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      加载编辑器中...
    </div>
    <div v-show="!loading" ref="editorContainer" class="editor"></div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import loader from '@monaco-editor/loader'
import { Loading } from '@element-plus/icons-vue'

export default {
  name: 'JsonEditor',
  components: {
    Loading
  },
  props: {
    modelValue: {
      type: [Object, String],
      required: true
    },
    height: {
      type: String,
      default: '400px'
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'change'],
  setup(props, { emit }) {
    const editorContainer = ref(null)
    const loading = ref(true)
    let editor = null

    const initEditor = async () => {
      try {
        // 等待下一个 tick，确保 DOM 已更新
        await nextTick()
        
        const monaco = await loader.init()
        
        // 再次确保容器存在
        if (!editorContainer.value) {
          console.error('Editor container not found')
          return
        }

        const value = typeof props.modelValue === 'string' 
          ? props.modelValue 
          : JSON.stringify(props.modelValue, null, 2)

        editor = monaco.editor.create(editorContainer.value, {
          value,
          language: 'json',
          theme: 'vs',
          automaticLayout: true,
          minimap: { enabled: false },
          readOnly: props.readonly,
          scrollBeyondLastLine: false,
          fontSize: 14,
          tabSize: 2,
          formatOnPaste: true,
          formatOnType: true
        })

        editor.onDidChangeModelContent(() => {
          try {
            const value = editor.getValue()
            const json = JSON.parse(value)
            emit('update:modelValue', json)
            emit('change', json)
          } catch (e) {
            // JSON 解析错误时不更新值
            console.warn('Invalid JSON:', e)
          }
        })

        loading.value = false
      } catch (error) {
        console.error('Failed to load editor:', error)
        loading.value = false
      }
    }

    onMounted(async () => {
      await initEditor()
    })

    onBeforeUnmount(() => {
      if (editor) {
        editor.dispose()
      }
    })

    watch(() => props.modelValue, (newValue) => {
      if (editor && typeof newValue !== 'undefined') {
        const editorValue = editor.getValue()
        const newValueStr = typeof newValue === 'string' 
          ? newValue 
          : JSON.stringify(newValue, null, 2)
        
        if (editorValue !== newValueStr) {
          editor.setValue(newValueStr)
        }
      }
    }, { deep: true })

    return {
      editorContainer,
      loading
    }
  }
}
</script>

<style scoped>
.json-editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  position: relative;
}

.editor {
  width: 100%;
  height: 100%;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
}
</style> 