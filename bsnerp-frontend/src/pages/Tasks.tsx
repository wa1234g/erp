import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { tasksApi } from '@/lib/api'
import { Plus, Calendar, User, Flag } from 'lucide-react'

export default function Tasks() {
  const [tasks, setTasks] = useState<any[]>([])
  const [kanbanData, setKanbanData] = useState<any>({})
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('kanban')

  useEffect(() => {
    loadTasks()
    loadKanban()
  }, [])

  const loadTasks = async () => {
    try {
      const data = await tasksApi.getAll({ page: 1, limit: 50 })
      setTasks(data.tasks)
    } catch (error) {
      console.error('Error loading tasks:', error)
    }
  }

  const loadKanban = async () => {
    try {
      const data = await tasksApi.getKanban()
      setKanbanData(data)
    } catch (error) {
      console.error('Error loading kanban:', error)
    } finally {
      setLoading(false)
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
      <Badge variant={variants[priority] || 'secondary'} className="text-xs">
        {labels[priority] || priority}
      </Badge>
    )
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      todo: 'bg-gray-100 dark:bg-gray-800',
      in_progress: 'bg-blue-100 dark:bg-blue-900',
      in_review: 'bg-yellow-100 dark:bg-yellow-900',
      done: 'bg-green-100 dark:bg-green-900'
    }
    return colors[status] || 'bg-gray-100'
  }

  const getStatusTitle = (status: string) => {
    const titles: Record<string, string> = {
      todo: 'قائمة المهام',
      in_progress: 'قيد التنفيذ',
      in_review: 'قيد المراجعة',
      done: 'مكتملة'
    }
    return titles[status] || status
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">المهام</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-4">
          {[...Array(4)].map((_, i) => (
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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">المهام</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة مهام الفريق</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          مهمة جديدة
        </Button>
      </div>

      <Tabs value={view} onValueChange={setView}>
        <TabsList>
          <TabsTrigger value="kanban">عرض Kanban</TabsTrigger>
          <TabsTrigger value="list">عرض القائمة</TabsTrigger>
        </TabsList>

        <TabsContent value="kanban" className="space-y-4">
          <div className="grid gap-6 md:grid-cols-4">
            {Object.entries(kanbanData).map(([status, statusTasks]) => (
              <Card key={status} className={getStatusColor(status)}>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">
                    {getStatusTitle(status)}
                  </CardTitle>
                  <CardDescription>
                    {(statusTasks as any[])?.length || 0} مهمة
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {(statusTasks as any[])?.map((task) => (
                    <Card key={task.id} className="bg-white dark:bg-gray-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                      <CardContent className="p-4">
                        <div className="space-y-2">
                          <h4 className="font-medium text-sm">{task.title}</h4>
                          
                          <div className="flex items-center justify-between">
                            {getPriorityBadge(task.priority)}
                            <div className="flex items-center gap-1 text-xs text-gray-500">
                              <Flag className="h-3 w-3" />
                              {task.type}
                            </div>
                          </div>

                          {task.assigned_user_name && (
                            <div className="flex items-center gap-2 text-xs text-gray-600">
                              <User className="h-3 w-3" />
                              {task.assigned_user_name}
                            </div>
                          )}

                          {task.due_date && (
                            <div className="flex items-center gap-2 text-xs text-gray-600">
                              <Calendar className="h-3 w-3" />
                              {new Date(task.due_date).toLocaleDateString('ar-EG')}
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                  
                  {(!statusTasks || (statusTasks as any[]).length === 0) && (
                    <div className="text-center py-4 text-gray-500 text-sm">
                      لا توجد مهام
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="list" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>قائمة المهام</CardTitle>
              <CardDescription>جميع المهام في الشركة</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {tasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800">
                    <div className="flex items-center space-x-4 space-x-reverse">
                      <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-blue-600 font-semibold text-sm">
                          {task.title.charAt(0)}
                        </span>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">
                          {task.title}
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {task.project_name} • {task.assigned_user_name}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          {getPriorityBadge(task.priority)}
                          <Badge variant="outline">{task.type}</Badge>
                        </div>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-medium">{task.status}</p>
                      {task.due_date && (
                        <p className="text-sm text-gray-500">
                          {new Date(task.due_date).toLocaleDateString('ar-EG')}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              
              {tasks.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-500 dark:text-gray-400">لا توجد مهام</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
