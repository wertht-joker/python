<template>
  <div class="layout">
    <!-- 左：输入区 -->
    <div class="panel input-panel">
      <h2>① 输入简历</h2>
      <el-upload
        drag
        :show-file-list="false"
        :http-request="doUpload"
        accept=".pdf,.docx,.txt,.md"
        class="uploader"
      >
        <div class="upload-hint">📤 拖拽上传简历（PDF / Word）</div>
        <div class="upload-sub">或点击选择文件</div>
      </el-upload>

      <div class="divider">或直接粘贴</div>
      <el-input
        v-model="resumeText"
        type="textarea"
        :rows="12"
        placeholder="把简历文字粘贴到这里…"
      />

      <h2 style="margin-top: 20px">② 选择目标岗位</h2>
      <el-select v-model="job" placeholder="选择岗位" style="width: 100%">
        <el-option v-for="j in jobs" :key="j.name" :label="`${j.name}（${j.category}）`" :value="j.name" />
      </el-select>

      <el-button type="primary" size="large" style="width: 100%; margin-top: 20px" :loading="loading" @click="doGrade">
        🎯 开始打分
      </el-button>
    </div>

    <!-- 右：结果区 -->
    <div class="panel result-panel">
      <template v-if="result">
        <div class="score-head">
          <div class="score-total">{{ result.total }}<span class="unit">分</span></div>
          <div class="score-job">目标岗位：{{ result.job }}</div>
        </div>

        <div class="columns">
          <div ref="chartEl" class="chart"></div>
          <div class="dims">
            <div v-for="(d, k) in result.dimensions" :key="k" class="dim-row">
              <span class="dim-name">{{ d.name }}</span>
              <el-progress :percentage="d.score" :stroke-width="10" :color="barColor(d.score)" />
              <span class="dim-weight">权重 {{ Math.round(d.weight * 100) }}%</span>
            </div>
          </div>
        </div>

        <div class="skills">
          <div class="skill-block">
            <h3>✅ 已掌握（{{ result.matched_skills.length }}）</h3>
            <el-tag v-for="s in result.matched_skills" :key="s" class="tag" type="success">{{ s }}</el-tag>
            <span v-if="!result.matched_skills.length" class="empty">未识别到技能</span>
          </div>
          <div class="skill-block">
            <h3>❌ 缺失（{{ result.missing_skills.length }}）</h3>
            <el-tag v-for="s in result.missing_skills" :key="s" class="tag" :type="result.core_missing.includes(s) ? 'danger' : 'warning'">
              {{ s }}{{ result.core_missing.includes(s) ? ' · 核心' : '' }}
            </el-tag>
            <span v-if="!result.missing_skills.length" class="empty">岗位要求的技能全部命中 🎉</span>
          </div>
        </div>

        <div class="advice">
          <h3>💡 改进建议</h3>
          <p v-if="result.advice" class="advice-text">{{ result.advice }}</p>
          <p v-else class="empty">未配置 DeepSeek API Key，暂无 AI 建议（各维度得分与技能匹配仍可用）</p>
        </div>
      </template>

      <template v-else>
        <div class="placeholder">
          <div class="ph-icon">📊</div>
          <p>上传或粘贴简历，选择岗位后点「开始打分」</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import request from '../api'

const resumeText = ref('')
const job = ref('')
const jobs = ref([])
const loading = ref(false)
const result = ref(null)
const chartEl = ref(null)
let chart = null

async function loadJobs() {
  try {
    jobs.value = await request.get('/jobs')
  } catch (e) {
    ElMessage.error('加载岗位失败：' + e.message)
  }
}

async function doUpload({ file }) {
  const fd = new FormData()
  fd.append('file', file)
  try {
    const data = await request.post('/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    resumeText.value = data.text
    ElMessage.success(`解析成功，识别到 ${data.entities.skills.length} 项技能`)
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function doGrade() {
  if (!resumeText.value.trim()) return ElMessage.warning('请先输入简历内容')
  if (!job.value) return ElMessage.warning('请选择目标岗位')
  loading.value = true
  try {
    result.value = await request.post('/grade', { resume_text: resumeText.value, job: job.value })
    await nextTick()
    renderChart()
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    loading.value = false
  }
}

function renderChart() {
  if (!result.value || !chartEl.value) return
  if (!chart) chart = echarts.init(chartEl.value)
  const dims = result.value.dimensions
  const indicator = Object.values(dims).map((d) => ({ name: d.name, max: 100 }))
  const values = Object.values(dims).map((d) => d.score)
  chart.setOption({
    radar: {
      indicator,
      radius: '65%',
      axisName: { color: '#666', fontSize: 12 },
    },
    series: [{
      type: 'radar',
      data: [{ value: values, name: '得分', areaStyle: { opacity: 0.3 } }],
    }],
  })
}

function barColor(score) {
  if (score >= 80) return '#67c23a'
  if (score >= 60) return '#e6a23c'
  return '#f56c6c'
}

onMounted(loadJobs)
</script>

<style scoped>
.layout { display: flex; gap: 20px; padding: 24px 32px; align-items: flex-start; }
.panel { background: #fff; border-radius: 10px; padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.panel h2 { font-size: 15px; color: #303133; margin-bottom: 14px; }
.input-panel { width: 380px; flex-shrink: 0; }
.result-panel { flex: 1; min-height: 560px; }
.uploader { margin-bottom: 8px; }
.upload-hint { color: #409eff; font-size: 14px; }
.upload-sub { color: #999; font-size: 12px; margin-top: 4px; }
.divider { text-align: center; color: #bbb; font-size: 12px; margin: 14px 0; }
.score-head { display: flex; align-items: baseline; gap: 16px; margin-bottom: 16px; }
.score-total { font-size: 46px; font-weight: bold; color: #409eff; }
.unit { font-size: 16px; color: #999; margin-left: 4px; }
.score-job { font-size: 14px; color: #666; }
.columns { display: flex; gap: 24px; align-items: center; margin-bottom: 20px; }
.chart { width: 320px; height: 320px; flex-shrink: 0; }
.dims { flex: 1; display: flex; flex-direction: column; gap: 16px; }
.dim-row { display: flex; align-items: center; gap: 12px; }
.dim-name { width: 70px; font-size: 13px; color: #333; flex-shrink: 0; }
.dim-weight { font-size: 11px; color: #999; width: 60px; flex-shrink: 0; }
.skills { display: flex; gap: 20px; margin-bottom: 20px; }
.skill-block { flex: 1; }
.skill-block h3 { font-size: 13px; color: #333; margin-bottom: 10px; }
.tag { margin: 0 6px 6px 0; }
.advice { border-top: 1px solid #eee; padding-top: 16px; }
.advice h3 { font-size: 14px; color: #333; margin-bottom: 10px; }
.advice-text { font-size: 13px; color: #555; line-height: 1.8; white-space: pre-wrap; }
.empty { color: #bbb; font-size: 13px; }
.placeholder { text-align: center; color: #bbb; padding-top: 140px; }
.ph-icon { font-size: 60px; margin-bottom: 16px; }
</style>
