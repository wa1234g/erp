import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { clientsApi } from '@/lib/api'
import { Plus, Search, Filter, Download, Trash2, Eye } from 'lucide-react'

export default function Clients() {
  const [clients, setClients] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    loadClients()
  }, [page, search])

  const loadClients = async () => {
    try {
      setLoading(true)
      const params = { page, limit: 10, search }
      const data = await clientsApi.getAll(params)
      setClients(data.clients)
      setTotal(data.total)
    } catch (error) {
      console.error('Error loading clients:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, any> = {
      active: 'default',
      inactive: 'secondary',
      prospect: 'outline',
      suspended: 'destructive'
    }
    
    const labels: Record<string, string> = {
      active: 'نشط',
      inactive: 'غير نشط',
      prospect: 'محتمل',
      suspended: 'معلق'
    }

    return (
      <Badge variant={variants[status] || 'secondary'}>
        {labels[status] || status}
      </Badge>
    )
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">العملاء</h1>
        </div>
        <div className="grid gap-4">
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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">العملاء</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة عملاء الشركة</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          عميل جديد
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>قائمة العملاء</CardTitle>
              <CardDescription>إجمالي {total} عميل</CardDescription>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4 ml-2" />
                فلترة
              </Button>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 ml-2" />
                تصدير
              </Button>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="البحث في العملاء..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pr-10"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {clients.map((client) => (
              <div key={client.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800">
                <div className="flex items-center space-x-4 space-x-reverse">
                  <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-semibold">
                      {client.name.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {client.name}
                    </h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {client.email} • {client.phone}
                    </p>
                    <div className="flex items-center gap-2 mt-1">
                      {getStatusBadge(client.status)}
                      <Badge variant="outline">{client.type === 'company' ? 'شركة' : 'فرد'}</Badge>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-left">
                    <p className="text-sm font-medium">{client.total_projects} مشروع</p>
                    <p className="text-sm text-gray-500">{client.total_revenue?.toLocaleString()} ج.م</p>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
          
          {clients.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">لا توجد عملاء</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
