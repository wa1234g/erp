import React, { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { dashboardApi } from '@/lib/api'
import {
  Users,
  FolderOpen,
  CheckSquare,
  DollarSign,
  Server,
  TrendingUp,
  TrendingDown,
  Activity,
  AlertCircle
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [recentActivity, setRecentActivity] = useState<any[]>([])
  const [revenueChart, setRevenueChart] = useState<any[]>([])
  const [projectsChart, setProjectsChart] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [statsData, activityData, revenueData, projectsData] = await Promise.all([
        dashboardApi.getStats(),
        dashboardApi.getRecentActivity(),
        dashboardApi.getRevenueChart(),
        dashboardApi.getProjectsChart()
      ])
      
      setStats(statsData)
      setRecentActivity((activityData as any).activities)
      setRevenueChart((revenueData as any).data)
      setProjectsChart((projectsData as any).data)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">لوحة القيادة</h1>
        <p className="text-gray-600 dark:text-gray-400">نظرة عامة على أداء الشركة</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">العملاء</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.clients?.total || 0}
                </p>
                <div className="flex items-center text-sm">
                  <TrendingUp className="h-4 w-4 text-green-500 ml-1" />
                  <span className="text-green-600">+{stats?.clients?.growth || 0}%</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <FolderOpen className="h-8 w-8 text-purple-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">المشاريع</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.projects?.active || 0}
                </p>
                <div className="flex items-center text-sm">
                  <span className="text-gray-600">من {stats?.projects?.total || 0}</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckSquare className="h-8 w-8 text-green-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">المهام</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.tasks?.completed || 0}
                </p>
                <div className="flex items-center text-sm">
                  <span className="text-gray-600">مكتملة</span>
                  {stats?.tasks?.overdue > 0 && (
                    <Badge variant="destructive" className="mr-2">
                      {stats.tasks.overdue} متأخرة
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DollarSign className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">الأرباح</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.finance?.profit?.toLocaleString() || 0} ج.م
                </p>
                <div className="flex items-center text-sm">
                  {stats?.finance?.profit >= 0 ? (
                    <TrendingUp className="h-4 w-4 text-green-500 ml-1" />
                  ) : (
                    <TrendingDown className="h-4 w-4 text-red-500 ml-1" />
                  )}
                  <span className={stats?.finance?.profit >= 0 ? 'text-green-600' : 'text-red-600'}>
                    {stats?.finance?.profit_margin?.toFixed(1) || 0}%
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>الإيرادات والمصروفات</CardTitle>
            <CardDescription>آخر 12 شهر</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueChart}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="revenue" stroke="#8884d8" name="الإيرادات" />
                <Line type="monotone" dataKey="expenses" stroke="#82ca9d" name="المصروفات" />
                <Line type="monotone" dataKey="profit" stroke="#ffc658" name="الأرباح" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>حالة المشاريع</CardTitle>
            <CardDescription>توزيع المشاريع حسب الحالة</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={projectsChart}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {projectsChart.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity and Server Status */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="h-5 w-5 ml-2" />
              النشاط الأخير
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.slice(0, 5).map((activity, index) => (
                <div key={index} className="flex items-start space-x-3 space-x-reverse">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <Activity className="h-4 w-4 text-blue-600" />
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {activity.title}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {activity.description}
                    </p>
                    <p className="text-xs text-gray-400">
                      {new Date(activity.timestamp).toLocaleDateString('ar-EG')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Server className="h-5 w-5 ml-2" />
              حالة السيرفرات
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">السيرفرات المتصلة</span>
                <Badge variant="secondary">
                  {stats?.servers?.online || 0} / {stats?.servers?.total || 0}
                </Badge>
              </div>
              <Progress value={stats?.servers?.uptime || 0} className="w-full" />
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">وقت التشغيل</span>
                <span className="font-medium">{stats?.servers?.uptime?.toFixed(1) || 0}%</span>
              </div>
              
              {stats?.servers?.offline > 0 && (
                <div className="flex items-center p-3 bg-red-50 rounded-lg">
                  <AlertCircle className="h-5 w-5 text-red-500 ml-2" />
                  <span className="text-sm text-red-700">
                    {stats.servers.offline} سيرفر غير متصل
                  </span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>إجراءات سريعة</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <Button variant="outline" className="h-20 flex-col">
              <Users className="h-6 w-6 mb-2" />
              عميل جديد
            </Button>
            <Button variant="outline" className="h-20 flex-col">
              <FolderOpen className="h-6 w-6 mb-2" />
              مشروع جديد
            </Button>
            <Button variant="outline" className="h-20 flex-col">
              <CheckSquare className="h-6 w-6 mb-2" />
              مهمة جديدة
            </Button>
            <Button variant="outline" className="h-20 flex-col">
              <DollarSign className="h-6 w-6 mb-2" />
              معاملة مالية
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
