<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadFile } from 'element-plus'

// ---- 分类树 ----
interface CategoryNode {
  id: number
  label: string
  children?: CategoryNode[]
}

const categories = ref<CategoryNode[]>([
  {
    id: 1,
    label: '产品资料',
    children: [
      { id: 11, label: '产品白皮书' },
      { id: 12, label: '功能说明书' },
      { id: 13, label: '版本发布说明' },
    ],
  },
  { id: 2, label: '技术方案' },
  {
    id: 3,
    label: '客户案例',
    children: [
      { id: 31, label: '政府/国企' },
      { id: 32, label: '制造业' },
      { id: 33, label: 'IT/互联网' },
      { id: 34, label: '金融' },
    ],
  },
  { id: 4, label: '销售话术' },
  { id: 5, label: '培训资料' },
  { id: 6, label: '合同模板' },
])

const activeCategory = ref<number>(0)

// ---- 文档列表 ----
interface DocumentItem {
  id: number
  title: string
  category: string
  categoryColor: string
  author: string
  authorAvatar: string
  updateTime: string
  views: number
  content: string
}

const documents = ref<DocumentItem[]>([
  {
    id: 1,
    title: 'AI运维平台v3.2产品白皮书',
    category: '产品资料',
    categoryColor: '#409EFF',
    author: '王总监',
    authorAvatar: '',
    updateTime: '2026-06-12 14:30',
    views: 1283,
    content: `# AI运维平台v3.2产品白皮书

## 1. 产品概述

AI运维平台v3.2是面向企业级IT运维场景的智能化管理平台，融合AI技术实现智能告警、自动工单和故障预测三大核心能力。

## 2. 核心功能

### 2.1 智能告警
基于机器学习算法，对海量运维数据进行实时分析，自动识别异常模式，减少误报率达95%。

### 2.2 自动工单
智能路由和自动分配工单，结合历史数据推荐最佳处理方案，工单处理效率提升60%。

### 2.3 故障预测
利用时序分析模型，提前识别潜在故障风险，实现从被动响应到主动预防的转变。

## 3. 技术架构

采用微服务架构，支持私有化部署和SaaS两种模式，兼容主流云平台。`,
  },
  {
    id: 2,
    title: '中科曙光IT运维升级项目方案',
    category: '技术方案',
    categoryColor: '#67C23A',
    author: '李经理',
    authorAvatar: '',
    updateTime: '2026-06-11 09:15',
    views: 856,
    content: `# 中科曙光IT运维升级项目技术方案

## 项目背景
中科曙光现有IT运维平台已运行5年，面临性能瓶颈和功能滞后问题。
本次升级旨在引入智能化运维能力，提升整体运维效率。

## 方案架构
- 采用AI运维平台v3.2作为核心底座
- 迁移现有数据至新平台，确保历史数据完整
- 分阶段实施：POC验证 -> 试点部署 -> 全面推广

## 实施计划
- 第一阶段（2周）：POC验证
- 第二阶段（4周）：核心模块上线
- 第三阶段（6周）：全面推广及培训`,
  },
  {
    id: 3,
    title: '华为云竞争应对策略分析',
    category: '销售话术',
    categoryColor: '#E6A23C',
    author: '张销售',
    authorAvatar: '',
    updateTime: '2026-06-10 16:45',
    views: 642,
    content: `# 华为云竞争应对策略

## 竞争分析
华为云在基础设施层面具有品牌优势，但在行业定制化和AI能力方面较弱。

## 应对策略
1. 强调AI运维的差异化能力
2. 突出行业Know-how积累
3. 提供更灵活的本地化服务

## 话术要点
"我们的AI运维平台已经在XX行业积累了丰富经验，能够针对您的业务场景提供定制化解决方案..."`,
  },
  {
    id: 4,
    title: '政府客户商务谈判要点',
    category: '销售话术',
    categoryColor: '#E6A23C',
    author: '赵总',
    authorAvatar: '',
    updateTime: '2026-06-09 11:20',
    views: 521,
    content: '# 政府客户商务谈判要点\n\n## 注意事项\n1. 严格遵守政府采购流程\n2. 提前准备资质文件\n3. 关注预算执行节点\n\n## 关键话术\n- 强调合规性和安全性\n- 突出国产化适配能力\n- 提供政务云部署方案',
  },
  {
    id: 5,
    title: 'IT运维平台标准合同模板',
    category: '合同模板',
    categoryColor: '#F56C6C',
    author: '法务部',
    authorAvatar: '',
    updateTime: '2026-06-08 08:30',
    views: 945,
    content: '# IT运维平台标准合同模板\n\n## 核心条款\n1. 服务范围及交付标准\n2. 付款方式及节点\n3. 知识产权归属\n4. 保密条款\n5. 违约责任\n\n> 注意：使用前请根据具体项目调整个性化条款',
  },
  {
    id: 6,
    title: '新员工产品培训手册（2026版）',
    category: '培训资料',
    categoryColor: '#909399',
    author: 'HR部门',
    authorAvatar: '',
    updateTime: '2026-06-05 15:00',
    views: 2310,
    content: '# 新员工产品培训手册\n\n## 培训目标\n- 了解公司产品体系\n- 掌握核心产品功能\n- 能够独立进行产品演示\n\n## 培训计划（5天）\n1. Day 1: 公司及产品线介绍\n2. Day 2-3: 核心产品深入学习\n3. Day 4: 销售技巧培训\n4. Day 5: 考核及认证',
  },
])

// ---- 搜索 ----
const searchKeyword = ref('')

const filteredDocuments = computed(() => {
  let list = documents.value

  // 按分类筛选
  if (activeCategory.value > 0) {
    const categoryLabel = getCategoryLabel(activeCategory.value)
    if (categoryLabel) {
      list = list.filter((d) => d.category === categoryLabel)
    }
  }

  // 按关键词搜索
  if (searchKeyword.value.trim()) {
    const kw = searchKeyword.value.trim().toLowerCase()
    list = list.filter(
      (d) =>
        d.title.toLowerCase().includes(kw) ||
        d.content.toLowerCase().includes(kw) ||
        d.author.toLowerCase().includes(kw),
    )
  }

  return list
})

function getCategoryLabel(id: number): string | null {
  for (const cat of categories.value) {
    if (cat.id === id) return cat.label
    if (cat.children) {
      const child = cat.children.find((c) => c.id === id)
      if (child) return cat.label
    }
  }
  return null
}

function handleCategoryClick(id: number) {
  activeCategory.value = activeCategory.value === id ? 0 : id
}

// ---- 文档预览弹窗 ----
const previewVisible = ref(false)
const previewDoc = ref<DocumentItem | null>(null)

function handlePreview(doc: DocumentItem) {
  previewDoc.value = doc
  previewVisible.value = true
}

// ---- 上传 ----
const uploadVisible = ref(false)
const uploadFileList = ref<UploadFile[]>([])

function handleUploadSuccess() {
  ElMessage.success('文档上传成功')
  uploadVisible.value = false
  uploadFileList.value = []
}

function handleBeforeUpload(file: File) {
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/markdown', 'text/plain']
  const isAllowed = allowedTypes.includes(file.type)
  if (!isAllowed) {
    ElMessage.error('仅支持 PDF、Word、Markdown、TXT 格式')
  }
  return isAllowed
}

// ---- 新建文档 ----
function handleCreateDoc() {
  uploadVisible.value = true
}

// ---- 格式化 ----
function formatViews(views: number): string {
  if (views >= 10000) return `${(views / 10000).toFixed(1)}万`
  if (views >= 1000) return `${(views / 1000).toFixed(1)}k`
  return String(views)
}

// ---- 简单 Markdown 样式渲染 ----
function renderMarkdownPreview(content: string): string {
  const safe = content.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  return safe
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br/>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
}
</script>

<template>
  <div class="knowledge-page">
    <!-- 顶部操作栏 -->
    <div class="knowledge-header">
      <div class="search-area">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索文档标题、内容、作者..."
          :prefix-icon="'Search'"
          clearable
          size="default"
          style="width: 420px"
        />
      </div>
      <el-button type="primary" @click="handleCreateDoc">
        <el-icon><Plus /></el-icon>新建文档
      </el-button>
    </div>

    <div class="knowledge-body">
      <!-- 左侧分类树 -->
      <div class="sidebar">
        <el-card shadow="hover" class="category-card">
          <template #header>
            <span class="card-title">文档分类</span>
          </template>
          <el-menu
            :default-active="String(activeCategory)"
            class="category-menu"
            @select="(id: string) => handleCategoryClick(Number(id))"
          >
            <template v-for="cat in categories" :key="cat.id">
              <el-sub-menu v-if="cat.children" :index="String(cat.id)">
                <template #title>
                  <el-icon><Folder /></el-icon>
                  <span>{{ cat.label }}</span>
                </template>
                <el-menu-item
                  v-for="child in cat.children"
                  :key="child.id"
                  :index="String(child.id)"
                >
                  {{ child.label }}
                </el-menu-item>
              </el-sub-menu>
              <el-menu-item v-else :index="String(cat.id)">
                <el-icon><Document /></el-icon>
                <span>{{ cat.label }}</span>
              </el-menu-item>
            </template>
          </el-menu>
        </el-card>
      </div>

      <!-- 右侧文档列表 -->
      <div class="main-content">
        <el-card shadow="hover" class="doc-list-card">
          <template #header>
            <div class="list-header">
              <span class="card-title">文档列表</span>
              <span class="doc-count">共 {{ filteredDocuments.length }} 篇</span>
            </div>
          </template>

          <el-table
            :data="filteredDocuments"
            style="width: 100%"
            stripe
            @row-click="handlePreview"
            row-class-name="doc-row"
          >
            <el-table-column prop="title" label="文档标题" min-width="240">
              <template #default="{ row }">
                <div class="doc-title-cell">
                  <el-icon color="#409EFF"><Document /></el-icon>
                  <span>{{ row.title }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120" align="center">
              <template #default="{ row }">
                <el-tag size="small" :color="row.categoryColor" effect="dark">
                  {{ row.category }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="author" label="作者" width="100" align="center" />
            <el-table-column prop="updateTime" label="更新时间" width="160" align="center" />
            <el-table-column prop="views" label="浏览" width="90" align="center">
              <template #default="{ row }">
                <div class="views-cell">
                  <el-icon><View /></el-icon>
                  <span>{{ formatViews(row.views) }}</span>
                </div>
              </template>
            </el-table-column>
          </el-table>

          <el-empty
            v-if="filteredDocuments.length === 0"
            description="未找到匹配的文档"
            :image-size="100"
            style="padding: 40px 0"
          />
        </el-card>
      </div>
    </div>

    <!-- 文档预览弹窗 -->
    <el-dialog
      v-model="previewVisible"
      :title="previewDoc?.title ?? '文档预览'"
      width="760px"
      top="5vh"
      destroy-on-close
    >
      <div class="preview-body" v-if="previewDoc">
        <div class="preview-meta">
          <el-tag size="small" :color="previewDoc.categoryColor" effect="dark">
            {{ previewDoc.category }}
          </el-tag>
          <span class="meta-item">作者：{{ previewDoc.author }}</span>
          <span class="meta-item">更新：{{ previewDoc.updateTime }}</span>
          <span class="meta-item">
            <el-icon><View /></el-icon>
            {{ formatViews(previewDoc.views) }} 次浏览
          </span>
        </div>
        <div class="preview-content markdown-body" v-html="renderMarkdownPreview(previewDoc.content)" />
      </div>
    </el-dialog>

    <!-- 上传文档弹窗 -->
    <el-dialog v-model="uploadVisible" title="新建文档" width="560px" destroy-on-close>
      <el-form label-width="80px">
        <el-form-item label="文档标题">
          <el-input placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select placeholder="请选择分类" style="width: 100%">
            <template v-for="cat in categories" :key="cat.id">
              <el-option-group v-if="cat.children" :label="cat.label">
                <el-option
                  v-for="child in cat.children"
                  :key="child.id"
                  :label="child.label"
                  :value="child.id"
                />
              </el-option-group>
              <el-option v-else :label="cat.label" :value="cat.id" />
            </template>
          </el-select>
        </el-form-item>
        <el-form-item label="文件上传">
          <el-upload
            v-model:file-list="uploadFileList"
            drag
            :before-upload="handleBeforeUpload"
            :on-success="handleUploadSuccess"
            :auto-upload="false"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 PDF、Word、Markdown、TXT 格式，单文件不超过 20MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="uploadVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUploadSuccess">确认上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.knowledge-page {
  max-width: 1400px;
  margin: 0 auto;
}

.knowledge-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.knowledge-body {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.sidebar {
  width: 240px;
  flex-shrink: 0;

  .category-card {
    .category-menu {
      border-right: none;

      :deep(.el-sub-menu__title) {
        height: 40px;
        line-height: 40px;
      }

      :deep(.el-menu-item) {
        height: 36px;
        line-height: 36px;
      }
    }
  }
}

.main-content {
  flex: 1;
  min-width: 0;

  .list-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .doc-count {
      font-size: 13px;
      color: #909399;
    }
  }
}

.card-title {
  font-size: 15px;
  font-weight: 600;
}

.doc-title-cell {
  display: flex;
  align-items: center;
  gap: 8px;

  span {
    color: #303133;
    font-weight: 500;
  }
}

.views-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: #909399;
  font-size: 13px;
}

:deep(.doc-row) {
  cursor: pointer;

  &:hover {
    background-color: #f5f7fa;
  }
}

// ---- 预览弹窗 ----
.preview-body {
  .preview-meta {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
    padding-bottom: 16px;
    border-bottom: 1px solid #ebeef5;
    margin-bottom: 16px;

    .meta-item {
      font-size: 13px;
      color: #909399;
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }

  .preview-content {
    max-height: 480px;
    overflow-y: auto;
    line-height: 1.8;
    font-size: 14px;
    color: #303133;

    :deep(h2) {
      font-size: 20px;
      margin: 20px 0 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #ebeef5;
    }

    :deep(h3) {
      font-size: 17px;
      margin: 16px 0 10px;
    }

    :deep(h4) {
      font-size: 15px;
      margin: 12px 0 8px;
    }

    :deep(blockquote) {
      margin: 10px 0;
      padding: 8px 16px;
      background: #f5f7fa;
      border-left: 4px solid #409eff;
      color: #606266;
    }

    :deep(strong) {
      color: #303133;
    }
  }
}
</style>
