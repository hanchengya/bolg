<template>
  <div class="admin-movies">
    <!-- 搜索和添加 -->
    <div class="flex justify-between items-center mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索电影..."
        class="px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
        @input="searchMovies"
      />
      <button
        @click="showAddModal = true"
        class="bg-accent-primary hover:bg-red-700 text-white px-6 py-2 rounded-lg transition"
      >
        ➕ 添加电影
      </button>
    </div>

    <!-- 电影列表 -->
    <div v-if="loading" class="text-center py-12">
      <div class="text-gray-400">加载中...</div>
    </div>
    <div v-else class="grid grid-cols-1 gap-4">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="bg-bg-tertiary rounded-lg p-4 flex gap-4 hover:bg-gray-700 transition"
      >
        <img
          :src="movie.poster"
          :alt="movie.title"
          class="w-20 h-28 object-cover rounded"
        />
        <div class="flex-1">
          <h3 class="text-xl font-bold mb-2">{{ movie.title }}</h3>
          <div class="text-gray-400 text-sm space-y-1">
            <p><span class="text-gray-500">排名:</span> {{ movie.rank }}</p>
            <p><span class="text-gray-500">评分:</span> {{ movie.douban_rating }}</p>
            <p><span class="text-gray-500">年份:</span> {{ movie.year }}</p>
            <p><span class="text-gray-500">导演:</span> {{ movie.director }}</p>
          </div>
        </div>
        <div class="flex flex-col justify-center gap-2">
          <button
            @click="editMovie(movie)"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition"
          >
            编辑
          </button>
          <button
            @click="confirmDelete(movie)"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition"
          >
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑电影弹窗 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 overflow-y-auto" @click.self="closeModal">
      <div class="bg-bg-secondary rounded-lg p-8 max-w-2xl w-full mx-4 my-8">
        <h2 class="text-2xl font-bold mb-6">{{ showEditModal ? '编辑电影' : '添加电影' }}</h2>
        
        <form @submit.prevent="saveMovie" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-gray-400 mb-2">电影名称*</label>
              <input
                v-model="formData.title"
                type="text"
                required
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              />
            </div>
            
            <div>
              <label class="block text-gray-400 mb-2">原始标题</label>
              <input
                v-model="formData.original_title"
                type="text"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              />
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-gray-400 mb-2">排名</label>
              <input
                v-model.number="formData.rank"
                type="number"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              />
            </div>
            
            <div>
              <label class="block text-gray-400 mb-2">年份</label>
              <input
                v-model.number="formData.year"
                type="number"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              />
            </div>
            
            <div>
              <label class="block text-gray-400 mb-2">评分</label>
              <input
                v-model.number="formData.douban_rating"
                type="number"
                step="0.1"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              />
            </div>
          </div>

          <div>
            <label class="block text-gray-400 mb-2">导演</label>
            <input
              v-model="formData.director"
              type="text"
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
            />
          </div>

          <div>
            <label class="block text-gray-400 mb-2">主演 (用 / 分隔)</label>
            <input
              v-model="formData.cast"
              type="text"
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              placeholder="演员1 / 演员2 / 演员3"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-gray-400 mb-2">类型 (用 / 分隔)</label>
              <input
                v-model="formData.genres"
                type="text"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
                placeholder="剧情 / 动作"
              />
            </div>
            
            <div>
              <label class="block text-gray-400 mb-2">国家/地区</label>
              <input
                v-model="formData.country"
                type="text"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
              />
            </div>
          </div>

          <div>
            <label class="block text-gray-400 mb-2">剧情简介</label>
            <textarea
              v-model="formData.summary"
              rows="4"
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
            ></textarea>
          </div>

          <div>
            <label class="block text-gray-400 mb-2">海报图片*</label>
            <div class="space-y-3">
              <!-- 当前海报预览 -->
              <div v-if="formData.poster && !posterFile" class="flex items-center gap-4">
                <img :src="formData.poster" alt="当前海报" class="w-24 h-32 object-cover rounded" />
                <span class="text-gray-400 text-sm">当前海报</span>
              </div>
              
              <!-- 新上传的图片预览 -->
              <div v-if="posterPreview" class="flex items-center gap-4">
                <img :src="posterPreview" alt="新海报预览" class="w-24 h-32 object-cover rounded" />
                <span class="text-green-400 text-sm">新上传的图片</span>
              </div>
              
              <!-- 文件上传 -->
              <input
                type="file"
                accept="image/*"
                @change="handlePosterUpload"
                class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:bg-accent-primary file:text-white hover:file:bg-red-700 file:cursor-pointer"
              />
              <p class="text-gray-500 text-sm">支持 JPG、PNG、WebP 格式，建议尺寸：400x600</p>
            </div>
          </div>

          <div>
            <label class="block text-gray-400 mb-2">豆瓣链接</label>
            <input
              v-model="formData.douban_url"
              type="text"
              class="w-full px-4 py-2 bg-bg-tertiary border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent-primary"
            />
          </div>
          
          <div class="flex gap-4 pt-4">
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

const movies = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const showAddModal = ref(false);
const showEditModal = ref(false);
const posterFile = ref(null);
const posterPreview = ref('');
const formData = ref({
  title: '',
  original_title: '',
  rank: null,
  year: null,
  country: '',
  director: '',
  cast: '',
  genres: '',
  runtime: null,
  summary: '',
  poster: '',
  douban_url: '',
  douban_rating: null
});
const editingMovieId = ref(null);

const loadMovies = async () => {
  console.log('🔍 [AdminMovies] 开始加载电影列表...');
  loading.value = true;
  try {
    console.log('📡 [AdminMovies] 调用 adminService.getMovies()');
    const result = await adminService.getMovies();
    console.log('✅ [AdminMovies] 获取到电影数据:', result, '类型:', typeof result, '是数组?', Array.isArray(result));
    
    // 确保result是数组
    if (Array.isArray(result)) {
      movies.value = result;
    } else if (result && Array.isArray(result.data)) {
      movies.value = result.data;
    } else {
      console.warn('⚠️ [AdminMovies] 返回的数据不是数组，设置为空数组');
      movies.value = [];
    }
  } catch (error) {
    console.error('❌ [AdminMovies] 获取电影列表失败:', error);
    console.error('错误详情:', error.response?.data || error.message);
    movies.value = []; // 确保出错时也是数组
    alert('获取电影列表失败: ' + (error.message || '未知错误'));
  } finally {
    loading.value = false;
    console.log('🏁 [AdminMovies] 加载完成，电影数量:', movies.value?.length || 0);
  }
};

const searchMovies = async () => {
  if (searchQuery.value.trim()) {
    loading.value = true;
    try {
      movies.value = await adminService.searchMovies(searchQuery.value);
    } catch (error) {
      console.error('搜索电影失败:', error);
    } finally {
      loading.value = false;
    }
  } else {
    loadMovies();
  }
};

const handlePosterUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      alert('请选择图片文件');
      return;
    }
    
    // 验证文件大小（限制5MB）
    if (file.size > 5 * 1024 * 1024) {
      alert('图片大小不能超过5MB');
      return;
    }
    
    posterFile.value = file;
    
    // 创建预览
    const reader = new FileReader();
    reader.onload = (e) => {
      posterPreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
    
    console.log('📷 选择了图片:', file.name, '大小:', (file.size / 1024).toFixed(2), 'KB');
  }
};

const editMovie = (movie) => {
  editingMovieId.value = movie.id;
  formData.value = { ...movie };
  posterFile.value = null;
  posterPreview.value = '';
  showEditModal.value = true;
};

const saveMovie = async () => {
  console.log('💾 [saveMovie] 开始保存电影...');
  console.log('💾 [saveMovie] 模式:', showEditModal.value ? '编辑' : '新建');
  console.log('💾 [saveMovie] formData:', formData.value);
  console.log('💾 [saveMovie] posterFile:', posterFile.value);
  
  try {
    // 构建FormData
    const data = new FormData();
    
    // 添加所有字段
    Object.keys(formData.value).forEach(key => {
      if (formData.value[key] !== null && formData.value[key] !== '' && key !== 'poster') {
        data.append(key, formData.value[key]);
        console.log(`  - 添加字段 ${key}:`, formData.value[key]);
      }
    });
    
    // 如果有新上传的图片，添加到FormData
    if (posterFile.value) {
      data.append('poster', posterFile.value);
      console.log('📤 添加图片文件:', posterFile.value.name, posterFile.value.type, posterFile.value.size, 'bytes');
    } else if (showEditModal.value && formData.value.poster) {
      // 编辑模式且没有新图片，保留原图片URL
      console.log('  - 编辑模式，保留原图片');
    } else if (!showEditModal.value) {
      // 新建模式必须有图片
      alert('请上传海报图片');
      return;
    }
    
    // 打印FormData内容
    console.log('📦 FormData内容:');
    for (let [key, value] of data.entries()) {
      console.log(`  ${key}:`, value);
    }
    
    if (showEditModal.value) {
      console.log('📡 调用 updateMovie, ID:', editingMovieId.value);
      await adminService.updateMovie(editingMovieId.value, data);
      alert('电影更新成功');
    } else {
      console.log('📡 调用 createMovie');
      await adminService.createMovie(data);
      alert('电影创建成功');
    }
    closeModal();
    loadMovies();
    emit('stats-updated');
  } catch (error) {
    console.error('❌ 保存电影失败:', error);
    console.error('错误详情:', error.response?.data || error.message);
    alert('保存失败：' + (error.response?.data?.message || error.message));
  }
};

const confirmDelete = async (movie) => {
  if (confirm(`确定要删除电影 "${movie.title}" 吗？`)) {
    try {
      await adminService.deleteMovie(movie.id);
      alert('电影删除成功');
      loadMovies();
      emit('stats-updated');
    } catch (error) {
      console.error('删除电影失败:', error);
      alert('删除失败');
    }
  }
};

const closeModal = () => {
  showAddModal.value = false;
  showEditModal.value = false;
  posterFile.value = null;
  posterPreview.value = '';
  formData.value = {
    title: '',
    original_title: '',
    rank: null,
    year: null,
    country: '',
    director: '',
    cast: '',
    genres: '',
    runtime: null,
    summary: '',
    poster: '',
    douban_url: '',
    douban_rating: null
  };
  editingMovieId.value = null;
};

onMounted(() => {
  loadMovies();
});
</script>
