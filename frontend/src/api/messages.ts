export interface Message {
  id: number
  content: string
  created_at: string
}

async function request(path: string, options: RequestInit = {}): Promise<Response> {
  let response: Response
  try {
    response = await fetch(`/api${path}`, {
      ...options,
      signal: AbortSignal.timeout(10000),
    })
  } catch {
    throw new Error('无法连接留言服务或请求超时，请稍后刷新。')
  }
  if (!response.ok) throw new Error(`请求失败（${response.status}），请稍后重试。`)
  return response
}

export async function listMessages(): Promise<Message[]> {
  const response = await request('/messages')
  return response.json()
}

export async function createMessage(content: string): Promise<Message> {
  const response = await request('/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  })
  return response.json()
}

export async function deleteMessage(id: number): Promise<void> {
  await request(`/messages/${id}`, { method: 'DELETE' })
}
