<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { listMessages, createMessage, deleteMessage, type Message } from './api/messages'

const messages = ref<Message[]>([])
const content = ref('')
const busy = ref(false)
const error = ref('')
const loaded = ref(false)

async function run(action: () => Promise<void>) {
  if (busy.value) return
  busy.value = true
  error.value = ''
  try { await action() }
  catch (cause) { error.value = cause instanceof Error ? cause.message : '操作失败，请重试。' }
  finally { busy.value = false }
}

function refresh() {
  return run(async () => {
    messages.value = await listMessages()
    loaded.value = true
  })
}

function submit() {
  const text = content.value.trim()
  if (!text) return
  return run(async () => {
    const message = await createMessage(text)
    messages.value.unshift(message)
    content.value = ''
  })
}

function remove(id: number) {
  if (busy.value || !window.confirm('确定删除这条留言吗？')) return
  return run(async () => {
    await deleteMessage(id)
    messages.value = messages.value.filter(message => message.id !== id)
  })
}

onMounted(refresh)
</script>

<template>
  <main>
    <header>
      <h1>留言板</h1>
      <p class="muted">记录想法，也看看大家分享了什么。</p>
    </header>
    <form class="card" @submit.prevent="submit">
      <label for="content">你的留言</label>
      <textarea id="content" v-model="content" rows="4" maxlength="1000"
        placeholder="有什么想分享的？" required :disabled="busy" />
      <div class="row">
        <span class="muted">{{ content.length }} / 1000</span>
        <button :disabled="busy || !content.trim()">发布留言</button>
      </div>
    </form>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <p v-if="busy" role="status" class="muted">正在处理，请稍候…</p>
    <section aria-labelledby="messages-title" :aria-busy="busy">
      <div class="row section-heading">
        <h2 id="messages-title">最新留言</h2>
        <button class="secondary" :disabled="busy" @click="refresh">刷新</button>
      </div>
      <p v-if="loaded && !messages.length" class="card muted">还没有留言，写下第一条吧。</p>
      <ul class="messages">
        <li v-for="message in messages" :key="message.id" class="card">
          <p class="message-content">{{ message.content }}</p>
          <div class="row">
            <time :datetime="message.created_at" class="muted">{{ new Date(message.created_at).toLocaleString('zh-CN') }}</time>
            <button class="secondary danger" :disabled="busy" @click="remove(message.id)">删除</button>
          </div>
        </li>
      </ul>
    </section>
  </main>
</template>
