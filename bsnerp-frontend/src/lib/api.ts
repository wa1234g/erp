const API_BASE_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem('access_token')
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, config)

    if (response.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Network error' }))
      throw new Error(error.detail || 'Request failed')
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint)
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
    })
  }
}

export const api = new ApiClient(`${API_BASE_URL}/api`)

export const authApi = {
  login: (credentials: any) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
  refreshToken: (refreshToken: string) => api.post('/auth/refresh', { refresh_token: refreshToken }),
}

export const clientsApi = {
  getAll: (params?: any) => api.get(`/clients?${new URLSearchParams(params)}`),
  getById: (id: number) => api.get(`/clients/${id}`),
  create: (data: any) => api.post('/clients', data),
  update: (id: number, data: any) => api.put(`/clients/${id}`, data),
  delete: (id: number) => api.delete(`/clients/${id}`),
  bulkDelete: (ids: number[]) => api.post('/clients/bulk-delete', ids),
  getProjects: (id: number) => api.get(`/clients/${id}/projects`),
  getTransactions: (id: number) => api.get(`/clients/${id}/transactions`),
  getStats: () => api.get('/clients/stats/overview'),
}

export const projectsApi = {
  getAll: (params?: any) => api.get(`/projects?${new URLSearchParams(params)}`),
  getById: (id: number) => api.get(`/projects/${id}`),
  create: (data: any) => api.post('/projects', data),
  update: (id: number, data: any) => api.put(`/projects/${id}`, data),
  delete: (id: number) => api.delete(`/projects/${id}`),
  getTasks: (id: number) => api.get(`/projects/${id}/tasks`),
  getTransactions: (id: number) => api.get(`/projects/${id}/transactions`),
  clone: (id: number, newName: string) => api.post(`/projects/${id}/clone`, { new_name: newName }),
  getStats: () => api.get('/projects/stats/overview'),
}

export const tasksApi = {
  getAll: (params?: any) => api.get(`/tasks?${new URLSearchParams(params)}`),
  getById: (id: number) => api.get(`/tasks/${id}`),
  create: (data: any) => api.post('/tasks', data),
  update: (id: number, data: any) => api.put(`/tasks/${id}`, data),
  delete: (id: number) => api.delete(`/tasks/${id}`),
  bulkDelete: (ids: number[]) => api.post('/tasks/bulk-delete', ids),
  getKanban: (projectId?: number) => api.get(`/tasks/kanban${projectId ? `?project_id=${projectId}` : ''}`),
  moveKanban: (data: any) => api.post('/tasks/kanban/move', data),
  addComment: (id: number, content: string) => api.post(`/tasks/${id}/comments`, { content }),
  getStats: () => api.get('/tasks/stats/overview'),
}

export const financeApi = {
  getTransactions: (params?: any) => api.get(`/finance/transactions?${new URLSearchParams(params)}`),
  createTransaction: (data: any) => api.post('/finance/transactions', data),
  updateTransaction: (id: number, data: any) => api.put(`/finance/transactions/${id}`, data),
  approveTransaction: (id: number) => api.post(`/finance/transactions/${id}/approve`),
  getCategories: () => api.get('/finance/categories'),
  createCategory: (data: any) => api.post('/finance/categories', data),
  getProfitLoss: (params?: any) => api.get(`/finance/reports/profit-loss?${new URLSearchParams(params)}`),
  getCashFlow: (months?: number) => api.get(`/finance/reports/cash-flow${months ? `?months=${months}` : ''}`),
  getStats: () => api.get('/finance/stats/overview'),
}

export const serversApi = {
  getAll: (params?: any) => api.get(`/servers?${new URLSearchParams(params)}`),
  getById: (id: number) => api.get(`/servers/${id}`),
  create: (data: any) => api.post('/servers', data),
  update: (id: number, data: any) => api.put(`/servers/${id}`, data),
  delete: (id: number) => api.delete(`/servers/${id}`),
  getMonitoring: (id: number) => api.get(`/servers/${id}/monitoring`),
  createBackup: (id: number, type?: string) => api.post(`/servers/${id}/backup`, { backup_type: type }),
  getBackups: (id: number) => api.get(`/servers/${id}/backups`),
  scheduleMaintenance: (id: number, data: any) => api.post(`/servers/${id}/maintenance`, data),
  getStats: () => api.get('/servers/stats/overview'),
}

export const credentialsApi = {
  getAll: (params?: any) => api.get(`/credentials?${new URLSearchParams(params)}`),
  getById: (id: number, showPassword?: boolean) => api.get(`/credentials/${id}${showPassword ? '?show_password=true' : ''}`),
  create: (data: any) => api.post('/credentials', data),
  update: (id: number, data: any) => api.put(`/credentials/${id}`, data),
  delete: (id: number) => api.delete(`/credentials/${id}`),
  generatePassword: (length?: number) => api.post(`/credentials/generate-password${length ? `?length=${length}` : ''}`),
  checkPasswordStrength: (password: string) => api.post('/credentials/check-password-strength', { password }),
  testConnection: (id: number) => api.post(`/credentials/${id}/test-connection`),
  share: (id: number, userIds: number[]) => api.post(`/credentials/${id}/share`, { user_ids: userIds }),
  getExpiring: (days?: number) => api.get(`/credentials/expiring-soon${days ? `?days=${days}` : ''}`),
  getStats: () => api.get('/credentials/stats/overview'),
}

export const notificationsApi = {
  getAll: (params?: any) => api.get(`/notifications?${new URLSearchParams(params)}`),
  create: (data: any) => api.post('/notifications', data),
  update: (id: number, data: any) => api.put(`/notifications/${id}`, data),
  markRead: (id: number) => api.post(`/notifications/${id}/mark-read`),
  markAllRead: () => api.post('/notifications/mark-all-read'),
  getTemplates: () => api.get('/notifications/templates'),
  createTemplate: (data: any) => api.post('/notifications/templates', data),
  getSubscriptions: () => api.get('/notifications/subscriptions'),
  createSubscription: (data: any) => api.post('/notifications/subscriptions', data),
  sendRenewalReminders: () => api.post('/notifications/send-renewal-reminders'),
  getStats: () => api.get('/notifications/stats/overview'),
}

export const dashboardApi = {
  getStats: () => api.get('/dashboard/stats'),
  getRecentActivity: () => api.get('/dashboard/recent-activity'),
  getRevenueChart: () => api.get('/dashboard/charts/revenue'),
  getProjectsChart: () => api.get('/dashboard/charts/projects'),
  getTasksChart: () => api.get('/dashboard/charts/tasks'),
}

export const settingsApi = {
  getCompany: () => api.get('/settings/company'),
  updateCompany: (data: any) => api.put('/settings/company', data),
  getSecurity: () => api.get('/settings/security'),
  updateSecurity: (data: any) => api.put('/settings/security', data),
  getIntegrations: () => api.get('/settings/integrations'),
  createWebhook: (data: any) => api.post('/settings/integrations/webhook', data),
  getBackup: () => api.get('/settings/backup'),
  createBackup: () => api.post('/settings/backup/create'),
  getAuditLogs: (params?: any) => api.get(`/settings/audit-logs?${new URLSearchParams(params)}`),
  getSystemInfo: () => api.get('/settings/system-info'),
}
