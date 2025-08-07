import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { projectsApi } from '@/lib/api'
import { Plus, Calendar, Users, DollarSign } from 'lucide-react'

export default function Projects() {
  const [projects, setProjects] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      const data = await projectsApi.getAll({ page: 1, limit: 20 })
      setProjects(data.projects)
    } catch (error) {
      console.error('Error loading projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, any> = {
      planning: 'secondary',
      in_progress: 'default',
      on_hold: 'outline',
      completed: 'default',
      cancelled: 'destructive'
    }
    
    const labels: Record<string, string> = {
      planning: 'تخطيط',
      in_progress: 'قيد التنفيذ',
      on_hold: 'متوقف',
      completed: 'مكتمل',
      cancelled: 'ملغي'
    }

    return (
      <Badge variant={variants[status] || 'secondary'}>
        {labels[status] || status}
      </Badge>
    )
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

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">المشاريع</h1>
        </div>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
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
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">المشاريع</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة مشاريع الشركة</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          مشروع جديد
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <Card key={project.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{project.name}</CardTitle>
                  <CardDescription>{project.client_name}</CardDescription>
                </div>
                <div className="flex flex-col gap-1">
                  {getStatusBadge(project.status)}
                  {getPriorityBadge(project.priority)}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>التقدم</span>
                    <span>{project.progress}%</span>
                  </div>
                  <Progress value={project.progress} className="h-2" />
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-600 dark:text-gray-400">
                      {project.start_date ? new Date(project.start_date).toLocaleDateString('ar-EG') : 'غير محدد'}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-600 dark:text-gray-400">
                      {project.team_members?.length || 0} عضو
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-600 dark:text-gray-400">
                      {project.budget?.toLocaleString() || 0} ج.م
                    </span>
                  </div>
                </div>

                {project.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                    {project.description}
                  </p>
                )}

                <div className="flex justify-between items-center pt-2">
                  <Badge variant="outline">{project.type}</Badge>
                  <Button variant="ghost" size="sm">
                    عرض التفاصيل
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {projects.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-gray-500 dark:text-gray-400">لا توجد مشاريع</p>
            <Button className="mt-4">
              <Plus className="h-4 w-4 ml-2" />
              إنشاء أول مشروع
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
