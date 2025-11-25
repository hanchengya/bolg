<template>
  <div class="admin-users">
    <!-- 搜索和添加 -->
    <div class="flex justify-between items-center mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索用户..."
        class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
        @input="searchUsers"
      />
      <button
        @click="showAddModal = true"
        class="bg-accent-primary hover:bg-red-700 text-white px-6 py-2 rounded-lg transition"
      >
        ➕ 添加用户
      </button>
    </div>

    <!-- 用户列表 -->
    <div v-if="loading" class="text-center py-12">
      <div class="text-gray-400">加载中...</div>
    </div>
    <div v-else class="bg-bg-tertiary rounded-lg overflow-hidden">
      <table class="w-full">
        <thead class="bg-bg-secondary">
          <tr>
            <th class="px-6 py-3 text-left">ID</th>
            <th class="px-6 py-3 text-left">用户名</th>
            <th class="px-6 py-3 text-left">邮箱</th>
            <th class="px-6 py-3 text-left">管理员</th>
            <th class="px-6 py-3 text-left">注册时间</th>
            <th class="px-6 py-3 text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-t border-gray-700 hover:bg-bg-secondary">
            <td class="px-6 py-4">{{ user.id }}</td>
            <td class="px-6 py-4 font-semibold">{{ user.username }}</td>
            <td class="px-6 py-4 text-gray-400">{{ user.email }}</td>
            <td class="px-6 py-4">
              <span v-if="user.is_staff" class="text-accent-primary">✓</span>
              <span v-else class="text-gray-600">-</span>
            </td>
            <td class="px-6 py-4 text-gray-400">{{ formatDate(user.date_joined) }}</td>
            <td class="px-6 py-4 text-right">
              <button
                @click="editUser(user)"
                class="text-blue-400 hover:text-blue-300 mr-4"
              >
                编辑
              </button>
              <button
                @click="confirmDelete(user)"
                class="text-red-400 hover:text-red-300"
                :disabled="user.is_superuser"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑用户弹窗 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click.self="closeModal">
      <div class="bg-bg-secondary rounded-lg p-8 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-6">{{ showEditModal ? '编辑用户' : '添加用户' }}</h2>
        
        <form @submit.prevent="saveUser">
          <div class="mb-4">
            <label class="block text-gray-400 mb-2">用户名</label>
            <input
              v-model="formData.username"
              type="text"
              required
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-gray-400 mb-2">邮箱</label>
            <input
              v-model="formData.email"
              type="email"
              required
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
            />
          </div>
          
          <div v-if="!showEditModal" class="mb-4">
            <label class="block text-gray-400 mb-2">密码</label>
            <input
              v-model="formData.password"
              type="password"
              required
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
            />
          </div>
          
          <div class="mb-6">
            <label class="flex items-center">
              <input
                v-model="formData.is_staff"
                type="checkbox"
                class="mr-2"
              />
              <span class="text-gray-400">管理员权限</span>
            </label>
          </div>
          
          <div class="flex gap-4">
            <button
              type="submit"
              class="flex-1 bg-accent-primary hover:bg-red-700 text-white py-2 rounded-lg transition"
            >
              保存
            </button>
            <button
              type="button"
              @click="closeModal"
              class="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 rounded-lg transition"
            >
              取消
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { adminService } from '../services/admin';

const emit = defineEmits(['stats-updated']);

const users = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const showAddModal = ref(false);
const showEditModal = ref(false);
const formData = ref({
  username: '',
  email: '',
  password: '',
  is_staff: false
});
const editingUserId = ref(null);

const loadUsers = async () => {
  console.log('🔍 [AdminUsers] 开始加载用户列表...');
  loading.value = true;
  try {
    console.log('📡 [AdminUsers] 调用 adminService.getUsers()');
    const result = await adminService.getUsers();
    console.log('✅ [AdminUsers] 获取到用户数据:', result, '类型:', typeof result, '是数组?', Array.isArray(result));
    
    // 确保result是数组
    if (Array.isArray(result)) {
      users.value = result;
    } else if (result && Array.isArray(result.data)) {
      users.value = result.data;
    } else {
      console.warn('⚠️ [AdminUsers] 返回的数据不是数组，设置为空数组');
      users.value = [];
    }
  } catch (error) {
    console.error('❌ [AdminUsers] 获取用户列表失败:', error);
    console.error('错误详情:', error.response?.data || error.message);
    users.value = []; // 确保出错时也是数组
    alert('获取用户列表失败: ' + (error.message || '未知错误'));
  } finally {
    loading.value = false;
    console.log('🏁 [AdminUsers] 加载完成，用户数量:', users.value?.length || 0);
  }
};

const searchUsers = async () => {
  if (searchQuery.value.trim()) {
    loading.value = true;
    try {
      users.value = await adminService.searchUsers(searchQuery.value);
    } catch (error) {
      console.error('搜索用户失败:', error);
    } finally {
      loading.value = false;
    }
  } else {
    loadUsers();
  }
};

const editUser = (user) => {
  editingUserId.value = user.id;
  formData.value = {
    username: user.username,
    email: user.email,
    is_staff: user.is_staff,
    password: ''
  };
  showEditModal.value = true;
};

const saveUser = async () => {
  try {
    if (showEditModal.value) {
      await adminService.updateUser(editingUserId.value, formData.value);
      alert('用户更新成功');
    } else {
      await adminService.createUser(formData.value);
      alert('用户创建成功');
    }
    closeModal();
    loadUsers();
    emit('stats-updated');
  } catch (error) {
    console.error('保存用户失败:', error);
    alert('保存失败：' + (error.response?.data?.message || error.message));
  }
};

const confirmDelete = async (user) => {
  if (confirm(`确定要删除用户 "${user.username}" 吗？`)) {
    try {
      await adminService.deleteUser(user.id);
      alert('用户删除成功');
      loadUsers();
      emit('stats-updated');
    } catch (error) {
      console.error('删除用户失败:', error);
      alert('删除失败');
    }
  }
};

const closeModal = () => {
  showAddModal.value = false;
  showEditModal.value = false;
  formData.value = {
    username: '',
    email: '',
    password: '',
    is_staff: false
  };
  editingUserId.value = null;
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN');
};

onMounted(() => {
  loadUsers();
});
</script>
