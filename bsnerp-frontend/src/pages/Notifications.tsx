import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { notificationsApi } from '@/lib/api'
import { Bell, Check, CheckCheck, Plus, Settings } from 'lucide-react'

export default function Notifications() {
  const [notifications, setNotifications] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadNotifications()
  }, [])

  const loadNotifications = async () => {
    try {
      const data = await notificationsApi.getAll({ page: 1, limit: 50 })
      setNotifications(data.notifications)
    } catch (error) {
      console.error('Error loading notifications:', error)
    } finally {
      setLoading(false)
    }
  }

  const markAsRead = async (notificationId: number) => {
    try {
      await notificationsApi.markRead(notificationId)
      setNotifications(prev => prev.map(n => 
        n.id === notificationId ? { ...n, status: 'read', read_at: new Date() } : n
      ))
    } catch (error) {
      console.error('Error marking notification as read:', error)
    }
  }

  const markAllAsRead = async () => {
    try {
      await notificationsApi.markAllRead()
      setNotifications(prev => prev.map(n => ({ ...n, status: 'read', read_at: new Date() })))
    } catch (error) {
      console.error('Error marking all notifications as read:', error)
    }
  }

  const getPriorityBadge = (priority: string) => {
    const variants: Record<string, any> = {
      low: 'secondary',
      medium: 'outline',
      high: 'default',
      urgent: 'destructive'
    }
    
    const labels: Record<string, string> = {
      low: 'منخفضة',
      medium: 'متوسطة',
      high: 'عالية',
      urgent: 'عاجلة'
    }

    return (
      <Badge variant={variants[priority] || 'secondary'}>
        {labels[priority] || priority}
      </Badge>
    )
  }

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      renewal_reminder: 'تذكير تجديد',
      project_update: 'تحديث مشروع',
      task_assignment: 'تعيين مهمة',
      payment_due: 'استحقاق دفع',
      server_alert: 'تنبيه سيرفر',
      backup_status: 'حالة النسخ الاحتياطي',
      security_alert: 'تنبيه أمني',
      custom: 'مخصص'
    }
    return labels[type] || type
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">التنبيهات</h1>
        </div>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  const unreadCount = notifications.filter(n => n.status !== 'read').length

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">التنبيهات</h1>
          <p className="text-gray-600 dark:text-gray-400">
            {unreadCount > 0 ? `${unreadCount} تنبيه غير مقروء` : 'جميع التنبيهات مقروءة'}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Settings className="h-4 w-4 ml-2" />
            إعدادات التنبيهات
          </Button>
          <Button>
            <Plus className="h-4 w-4 ml-2" />
            تنبيه جديد
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>جميع التنبيهات</CardTitle>
              <CardDescription>آخر التنبيهات والإشعارات</CardDescription>
            </div>
            {unreadCount > 0 && (
              <Button variant="outline" onClick={markAllAsRead}>
                <CheckCheck className="h-4 w-4 ml-2" />
                تحديد الكل كمقروء
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`p-4 border rounded-lg transition-colors ${
                  notification.status === 'read' 
                    ? 'bg-gray-50 dark:bg-gray-800 opacity-75' 
                    : 'bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 space-x-reverse">
                    <div className={`h-10 w-10 rounded-full flex items-center justify-center ${
                      notification.priority === 'urgent' ? 'bg-red-100' :
                      notification.priority === 'high' ? 'bg-yellow-100' :
                      'bg-blue-100'
                    }`}>
                      <Bell className={`h-5 w-5 ${
                        notification.priority === 'urgent' ? 'text-red-600' :
                        notification.priority === 'high' ? 'text-yellow-600' :
                        'text-blue-600'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-semibold text-gray-900 dark:text-white">
                          {notification.title}
                        </h3>
                        {notification.status !== 'read' && (
                          <div className="h-2 w-2 bg-blue-600 rounded-full"></div>
                        )}
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">
                        {notification.message}
                      </p>
                      <div className="flex items-center gap-2">
                        <Badge variant="outline">{getTypeLabel(notification.type)}</Badge>
                        {getPriorityBadge(notification.priority)}
                        <span className="text-xs text-gray-500">
                          {new Date(notification.created_at).toLocaleDateString('ar-EG')} • 
                          {new Date(notification.created_at).toLocaleTimeString('ar-EG')}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    {notification.status !== 'read' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => markAsRead(notification.id)}
                      >
                        <Check className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {notifications.length === 0 && (
            <div className="text-center py-8">
              <Bell className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">لا توجد تنبيهات</p>
              <p className="text-sm text-gray-400 mt-1">ستظهر التنبيهات الجديدة هنا</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
