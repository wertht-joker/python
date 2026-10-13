<template>
  <div class="page">
    <header class="topbar">
      <h1>📄 简历打分助手</h1>
      <span class="subtitle">基于知识图谱 · 分维度打分 · AI 改进建议</span>
    </header>
    <GraderView />
  </div>
</template>

<script setup>
import GraderView from './views/GraderView.vue'
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, "Microsoft YaHei", sans-serif; background: #f5f6fa; }
.page { min-height: 100vh; }
.topbar { background: #fff; padding: 18px 32px; border-bottom: 1px solid #eee; display: flex; align-items: baseline; gap: 16px; }
.topbar h1 { font-size: 20px; color: #303133; }
.subtitle { font-size: 13px; color: #909399; }
</style>
