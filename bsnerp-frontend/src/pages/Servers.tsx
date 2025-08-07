import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { serversApi } from '@/lib/api'
import { Plus, Server, Activity, HardDrive, Cpu, MemoryStick } from 'lucide-react'

export default function Servers() {
  const [servers, setServers] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadServers()
  }, [])

  const loadServers = async () => {
    try {
      const data = await serversApi.getAll({ page: 1, limit: 20 })
      setServers(data.servers)
    } catch (error) {
      console.error('Error loading servers:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, any> = {
      online: 'default',
      offline: 'destructive',
      maintenance: 'outline',
      error: 'destructive'
    }
    
    const labels: Record<string, string> = {
      online: 'متصل',
      offline: 'غير متصل',
      maintenance: 'صيانة',
      error: 'خطأ'
    }

    return (
      <Badge variant={variants[status] || 'secondary'}>
        {labels[status] || status}
      </Badge>
    )
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      online: 'text-green-600',
      offline: 'text-red-600',
      maintenance: 'text-yellow-600',
      error: 'text-red-600'
    }
    return colors[status] || 'text-gray-600'
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">السيرفرات</h1>
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
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">السيرفرات</h1>
          <p className="text-gray-600 dark:text-gray-400">مراقبة وإدارة سيرفرات الشركة</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          سيرفر جديد
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {servers.map((server) => (
          <Card key={server.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="flex items-center gap-3">
                  <div className={`h-10 w-10 rounded-full flex items-center justify-center ${
                    server.status === 'online' ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    <Server className={`h-5 w-5 ${getStatusColor(server.status)}`} />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{server.name}</CardTitle>
                    <CardDescription>{server.hostname}</CardDescription>
                  </div>
                </div>
                {getStatusBadge(server.status)}
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">النوع:</span>
                    <p className="font-medium">{server.type}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">الموقع:</span>
                    <p className="font-medium">{server.location}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">المزود:</span>
                    <p className="font-medium">{server.provider}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">التكلفة:</span>
                    <p className="font-medium">{server.monthly_cost} ج.م/شهر</p>
                  </div>
                </div>

                {server.status === 'online' && (
                  <div className="space-y-3">
                    <div>
                      <div className="flex items-center justify-between text-sm mb-1">
                        <div className="flex items-center gap-1">
                          <Cpu className="h-4 w-4" />
                          <span>المعالج</span>
                        </div>
                        <span>{server.cpu_usage}%</span>
                      </div>
                      <Progress value={server.cpu_usage} className="h-2" />
                    </div>

                    <div>
                      <div className="flex items-center justify-between text-sm mb-1">
                        <div className="flex items-center gap-1">
                          <MemoryStick className="h-4 w-4" />
                          <span>الذاكرة</span>
                        </div>
                        <span>{server.memory_usage}%</span>
                      </div>
                      <Progress value={server.memory_usage} className="h-2" />
                    </div>

                    <div>
                      <div className="flex items-center justify-between text-sm mb-1">
                        <div className="flex items-center gap-1">
                          <HardDrive className="h-4 w-4" />
                          <span>التخزين</span>
                        </div>
                        <span>{server.disk_usage}%</span>
                      </div>
                      <Progress value={server.disk_usage} className="h-2" />
                    </div>

                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-1">
                        <Activity className="h-4 w-4" />
                        <span>وقت التشغيل</span>
                      </div>
                      <span className="font-medium">{server.uptime_percentage}%</span>
                    </div>
                  </div>
                )}

                <div className="flex justify-between items-center pt-2">
                  <Badge variant="outline">{server.projects?.length || 0} مشروع</Badge>
                  <Button variant="ghost" size="sm">
                    عرض التفاصيل
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {servers.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-gray-500 dark:text-gray-400">لا توجد سيرفرات</p>
            <Button className="mt-4">
              <Plus className="h-4 w-4 ml-2" />
              إضافة أول سيرفر
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
