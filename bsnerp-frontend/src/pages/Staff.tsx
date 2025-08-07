import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Input } from '@/components/ui/input'
import { Plus, Search, Mail, Phone, MapPin, Calendar } from 'lucide-react'

export default function Staff() {
  const [staff, setStaff] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    loadStaff()
  }, [])

  const loadStaff = async () => {
    try {
      setLoading(true)
      const mockStaff = [
        {
          id: 1,
          full_name: 'أحمد محمد علي',
          email: 'ahmed@bsnerp.com',
          phone: '+201234567890',
          role: 'admin',
          department: 'إدارة',
          position: 'مدير عام',
          status: 'active',
          avatar: null,
          skills: ['إدارة', 'قيادة', 'تخطيط'],
          created_at: new Date().toISOString()
        },
        {
          id: 2,
          full_name: 'فاطمة أحمد',
          email: 'fatima@bsnerp.com',
          phone: '+201234567891',
          role: 'manager',
          department: 'التطوير',
          position: 'مدير التطوير',
          status: 'active',
          avatar: null,
          skills: ['React', 'Node.js', 'إدارة فرق'],
          created_at: new Date().toISOString()
        },
        {
          id: 3,
          full_name: 'محمد حسن',
          email: 'mohamed@bsnerp.com',
          phone: '+201234567892',
          role: 'employee',
          department: 'التصميم',
          position: 'مصمم UI/UX',
          status: 'active',
          avatar: null,
          skills: ['Figma', 'Adobe XD', 'تصميم واجهات'],
          created_at: new Date().toISOString()
        }
      ]
      setStaff(mockStaff)
    } catch (error) {
      console.error('Error loading staff:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRoleBadge = (role: string) => {
    const variants: Record<string, any> = {
      admin: 'destructive',
      manager: 'default',
      employee: 'secondary',
      client: 'outline'
    }
    
    const labels: Record<string, string> = {
      admin: 'مدير',
      manager: 'مدير قسم',
      employee: 'موظف',
      client: 'عميل'
    }

    return (
      <Badge variant={variants[role] || 'secondary'}>
        {labels[role] || role}
      </Badge>
    )
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, any> = {
      active: 'default',
      inactive: 'secondary',
      suspended: 'destructive'
    }
    
    const labels: Record<string, string> = {
      active: 'نشط',
      inactive: 'غير نشط',
      suspended: 'معلق'
    }

    return (
      <Badge variant={variants[status] || 'secondary'}>
        {labels[status] || status}
      </Badge>
    )
  }

  const filteredStaff = staff.filter(member =>
    member.full_name.toLowerCase().includes(search.toLowerCase()) ||
    member.email.toLowerCase().includes(search.toLowerCase()) ||
    member.department.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">الموظفين</h1>
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
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">الموظفين</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة فريق العمل والموظفين</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          موظف جديد
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>قائمة الموظفين</CardTitle>
              <CardDescription>إجمالي {staff.length} موظف</CardDescription>
            </div>
          </div>
          <div className="relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="البحث في الموظفين..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pr-10"
            />
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredStaff.map((member) => (
              <Card key={member.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4 space-x-reverse mb-4">
                    <Avatar className="h-12 w-12">
                      <AvatarImage src={member.avatar} />
                      <AvatarFallback className="bg-blue-600 text-white">
                        {member.full_name.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 dark:text-white">
                        {member.full_name}
                      </h3>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {member.position}
                      </p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {member.email}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Phone className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {member.phone}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {member.department}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        انضم في {new Date(member.created_at).toLocaleDateString('ar-EG')}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between mt-4">
                    <div className="flex gap-2">
                      {getRoleBadge(member.role)}
                      {getStatusBadge(member.status)}
                    </div>
                    <Button variant="ghost" size="sm">
                      عرض الملف
                    </Button>
                  </div>

                  {member.skills && member.skills.length > 0 && (
                    <div className="mt-4">
                      <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        المهارات:
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {member.skills.slice(0, 3).map((skill: string, index: number) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                        {member.skills.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{member.skills.length - 3}
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
          
          {filteredStaff.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">
                {search ? 'لا توجد نتائج للبحث' : 'لا يوجد موظفين'}
              </p>
              {!search && (
                <Button className="mt-4">
                  <Plus className="h-4 w-4 ml-2" />
                  إضافة أول موظف
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
