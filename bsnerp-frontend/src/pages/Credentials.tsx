import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { credentialsApi } from '@/lib/api'
import { Plus, Search, Eye, EyeOff, Key, Shield, AlertTriangle } from 'lucide-react'

export default function Credentials() {
  const [credentials, setCredentials] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [visiblePasswords, setVisiblePasswords] = useState<Set<number>>(new Set())

  useEffect(() => {
    loadCredentials()
  }, [search])

  const loadCredentials = async () => {
    try {
      setLoading(true)
      const params = { page: 1, limit: 20, search }
      const data = await credentialsApi.getAll(params)
      setCredentials(data.credentials)
    } catch (error) {
      console.error('Error loading credentials:', error)
    } finally {
      setLoading(false)
    }
  }

  const togglePasswordVisibility = async (credentialId: number) => {
    const newVisible = new Set(visiblePasswords)
    
    if (visiblePasswords.has(credentialId)) {
      newVisible.delete(credentialId)
      setVisiblePasswords(newVisible)
    } else {
      try {
        const credential = await credentialsApi.getById(credentialId, true)
        setCredentials(prev => prev.map(c => 
          c.id === credentialId ? { ...c, password: credential.password } : c
        ))
        newVisible.add(credentialId)
        setVisiblePasswords(newVisible)
      } catch (error) {
        console.error('Error fetching password:', error)
      }
    }
  }

  const getTypeBadge = (type: string) => {
    const variants: Record<string, any> = {
      domain: 'default',
      hosting: 'secondary',
      email: 'outline',
      wordpress: 'default',
      database: 'destructive',
      ftp: 'secondary',
      ssh: 'outline',
      api: 'default'
    }
    
    const labels: Record<string, string> = {
      domain: 'دومين',
      hosting: 'استضافة',
      email: 'بريد',
      wordpress: 'ووردبريس',
      database: 'قاعدة بيانات',
      ftp: 'FTP',
      ssh: 'SSH',
      api: 'API'
    }

    return (
      <Badge variant={variants[type] || 'secondary'}>
        {labels[type] || type}
      </Badge>
    )
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, any> = {
      active: 'default',
      expired: 'destructive',
      expiring_soon: 'outline',
      inactive: 'secondary'
    }
    
    const labels: Record<string, string> = {
      active: 'نشط',
      expired: 'منتهي',
      expiring_soon: 'ينتهي قريباً',
      inactive: 'غير نشط'
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
          <h1 className="text-3xl font-bold">بيانات الدخول</h1>
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
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">بيانات الدخول</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة آمنة لبيانات الدخول</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          بيانات جديدة
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>بيانات الدخول المحفوظة</CardTitle>
              <CardDescription>جميع بيانات الدخول الآمنة</CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-yellow-500" />
              <span className="text-sm text-yellow-600">تأكد من الأمان قبل عرض كلمات المرور</span>
            </div>
          </div>
          <div className="relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="البحث في بيانات الدخول..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pr-10"
            />
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {credentials.map((credential) => (
              <Card key={credential.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 space-x-reverse">
                      <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <Key className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">
                          {credential.name}
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {credential.username} • {credential.url || 'لا يوجد رابط'}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          {getTypeBadge(credential.type)}
                          {getStatusBadge(credential.status)}
                          {credential.two_factor_enabled && (
                            <Badge variant="outline" className="text-xs">
                              <Shield className="h-3 w-3 ml-1" />
                              2FA
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="text-left">
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-gray-600">كلمة المرور:</span>
                          <code className="bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded text-sm">
                            {visiblePasswords.has(credential.id) ? credential.password : '••••••••'}
                          </code>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => togglePasswordVisibility(credential.id)}
                          >
                            {visiblePasswords.has(credential.id) ? (
                              <EyeOff className="h-4 w-4" />
                            ) : (
                              <Eye className="h-4 w-4" />
                            )}
                          </Button>
                        </div>
                        {credential.expiry_date && (
                          <p className="text-sm text-gray-500 mt-1">
                            ينتهي: {new Date(credential.expiry_date).toLocaleDateString('ar-EG')}
                          </p>
                        )}
                      </div>
                      
                      <div className="flex flex-col gap-1">
                        <Button variant="outline" size="sm">
                          اختبار الاتصال
                        </Button>
                        <Button variant="ghost" size="sm">
                          تعديل
                        </Button>
                      </div>
                    </div>
                  </div>
                  
                  {credential.notes && (
                    <div className="mt-3 p-3 bg-gray-50 dark:bg-gray-800 rounded">
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {credential.notes}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
          
          {credentials.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">لا توجد بيانات دخول محفوظة</p>
              <Button className="mt-4">
                <Plus className="h-4 w-4 ml-2" />
                إضافة أول بيانات دخول
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
