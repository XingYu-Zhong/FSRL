<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        background-color="#304156"
        text-color="#fff"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>FSRL训练系统</span>
        </el-menu-item>
        <el-menu-item index="/training">
          <el-icon><Monitor /></el-icon>
          <span>模型训练</span>
        </el-menu-item>
        <el-menu-item index="/configs">
          <el-icon><Setting /></el-icon>
          <span>配置管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-title">AI训练系统</div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-dropdown">
              管理员 <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { DataLine, Monitor, Setting, ArrowDown } from '@element-plus/icons-vue'

export default {
  name: 'MainLayout',
  components: {
    DataLine,
    Monitor,
    Setting,
    ArrowDown
  },
  setup() {
    const route = useRoute()
    const activeMenu = computed(() => route.path)

    return {
      activeMenu
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
}

.el-menu-vertical {
  border-right: none;
}

.el-header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}

.header-title {
  font-size: 18px;
  font-weight: bold;
}

.user-dropdown {
  cursor: pointer;
  color: #606266;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 