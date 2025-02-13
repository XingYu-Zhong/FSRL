<template>
  <div class="config-list">
    <el-table :data="configs" style="width: 100%">
      <el-table-column prop="name" label="配置名称" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="$emit('edit', row)">
            编辑
          </el-button>
          <el-button type="danger" size="small" @click="$emit('delete', row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'ConfigList',
  props: {
    configs: {
      type: Array,
      required: true
    }
  },
  emits: ['edit', 'delete']
}
</script> 