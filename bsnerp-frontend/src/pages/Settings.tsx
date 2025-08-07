import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { settingsApi } from '@/lib/api'
import { 
  Building, 
  Shield, 
  Plug, 
  Database, 
  FileText, 
  Monitor,
  Save,
  Download,
  Upload
} from 'lucide-react'

export default function Settings() {
  const [companySettings, setCompanySettings] = useState<any>(null)
  const [securitySettings, setSecuritySettings] = useState<any>(null)
  const [integrations, setIntegrations] = useState<any>(null)
  const [systemInfo, setSystemInfo] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      const [company, security, integrationsData, system] = await Promise.all([
        settingsApi.getCompany(),
        settingsApi.getSecurity(),
        settingsApi.getIntegrations(),
        settingsApi.getSystemInfo()
      ])
      
      setCompanySettings(company)
      setSecuritySettings(security)
      setIntegrations(integrationsData)
      setSystemInfo(system)
    } catch (error) {
      console.error('Error loading settings:', error)
    } finally {
      setLoading(false)
    }
  }

  const saveCompanySettings = async () => {
    try {
      await settingsApi.updateCompany(companySettings)
    } catch (error) {
      console.error('Error saving company settings:', error)
    }
  }

  const createBackup = async () => {
    try {
      const result = await settingsApi.createBackup()
      console.log('Backup created:', result)
    } catch (error) {
      console.error('Error creating backup:', error)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">الإعدادات</h1>
        </div>
        <div className="grid gap-4">
          {[...Array(3)].map((_, i) => (
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
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">الإعدادات</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة إعدادات النظام والشركة</p>
        </div>
      </div>

      <Tabs defaultValue="company" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="company" className="flex items-center gap-2">
            <Building className="h-4 w-4" />
            الشركة
          </TabsTrigger>
          <TabsTrigger value="security" className="flex items-center gap-2">
            <Shield className="h-4 w-4" />
            الأمان
          </TabsTrigger>
          <TabsTrigger value="integrations" className="flex items-center gap-2">
            <Plug className="h-4 w-4" />
            التكاملات
          </TabsTrigger>
          <TabsTrigger value="backup" className="flex items-center gap-2">
            <Database className="h-4 w-4" />
            النسخ الاحتياطي
          </TabsTrigger>
          <TabsTrigger value="system" className="flex items-center gap-2">
            <Monitor className="h-4 w-4" />
            النظام
          </TabsTrigger>
        </TabsList>

        <TabsContent value="company" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>إعدادات الشركة</CardTitle>
              <CardDescription>معلومات الشركة الأساسية</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="company_name">اسم الشركة</Label>
                  <Input
                    id="company_name"
                    value={companySettings?.company_name || ''}
                    onChange={(e) => setCompanySettings(prev => ({ ...prev, company_name: e.target.value }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">البريد الإلكتروني</Label>
                  <Input
                    id="email"
                    type="email"
                    value={companySettings?.email || ''}
                    onChange={(e) => setCompanySettings(prev => ({ ...prev, email: e.target.value }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="phone">رقم الهاتف</Label>
                  <Input
                    id="phone"
                    value={companySettings?.phone || ''}
                    onChange={(e) => setCompanySettings(prev => ({ ...prev, phone: e.target.value }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="website">الموقع الإلكتروني</Label>
                  <Input
                    id="website"
                    value={companySettings?.website || ''}
                    onChange={(e) => setCompanySettings(prev => ({ ...prev, website: e.target.value }))}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">العنوان</Label>
                <Input
                  id="address"
                  value={companySettings?.address || ''}
                  onChange={(e) => setCompanySettings(prev => ({ ...prev, address: e.target.value }))}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="tax_number">الرقم الضريبي</Label>
                  <Input
                    id="tax_number"
                    value={companySettings?.tax_number || ''}
                    onChange={(e) => setCompanySettings(prev => ({ ...prev, tax_number: e.target.value }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="currency">العملة</Label>
                  <Input
                    id="currency"
                    value={companySettings?.currency || ''}
                    onChange={(e) => setCompanySettings(prev => ({ ...prev, currency: e.target.value }))}
                  />
                </div>
              </div>
              <Button onClick={saveCompanySettings}>
                <Save className="h-4 w-4 ml-2" />
                حفظ التغييرات
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>إعدادات الأمان</CardTitle>
              <CardDescription>إعدادات الحماية والأمان</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <h4 className="font-medium">سياسة كلمات المرور</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>الحد الأدنى لطول كلمة المرور</Label>
                    <Input
                      type="number"
                      value={securitySettings?.password_policy?.min_length || 8}
                      readOnly
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>انتهاء صلاحية كلمة المرور (أيام)</Label>
                    <Input
                      type="number"
                      value={securitySettings?.password_policy?.expiry_days || 90}
                      readOnly
                    />
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <Label>يتطلب أحرف كبيرة</Label>
                    <Switch checked={securitySettings?.password_policy?.require_uppercase} disabled />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label>يتطلب أحرف صغيرة</Label>
                    <Switch checked={securitySettings?.password_policy?.require_lowercase} disabled />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label>يتطلب أرقام</Label>
                    <Switch checked={securitySettings?.password_policy?.require_numbers} disabled />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label>يتطلب رموز خاصة</Label>
                    <Switch checked={securitySettings?.password_policy?.require_symbols} disabled />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">التحقق الثنائي</h4>
                <div className="flex items-center justify-between">
                  <Label>مفعل للنظام</Label>
                  <Switch checked={securitySettings?.two_factor?.enabled} disabled />
                </div>
                <div className="flex items-center justify-between">
                  <Label>إجباري للمديرين</Label>
                  <Switch checked={securitySettings?.two_factor?.mandatory_for_admins} disabled />
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">سجلات المراجعة</h4>
                <div className="flex items-center justify-between">
                  <Label>تفعيل سجلات المراجعة</Label>
                  <Switch checked={securitySettings?.audit_logs?.enabled} disabled />
                </div>
                <div className="space-y-2">
                  <Label>مدة الاحتفاظ بالسجلات (أيام)</Label>
                  <Input
                    type="number"
                    value={securitySettings?.audit_logs?.retention_days || 365}
                    readOnly
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>التكاملات الخارجية</CardTitle>
              <CardDescription>إعدادات التكامل مع الخدمات الخارجية</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h4 className="font-medium">البريد الإلكتروني</h4>
                    <p className="text-sm text-gray-600">إعدادات SMTP لإرسال الإيميلات</p>
                  </div>
                  <Badge variant={integrations?.email?.enabled ? 'default' : 'secondary'}>
                    {integrations?.email?.enabled ? 'مفعل' : 'غير مفعل'}
                  </Badge>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h4 className="font-medium">الرسائل النصية</h4>
                    <p className="text-sm text-gray-600">إرسال SMS عبر Twilio</p>
                  </div>
                  <Badge variant={integrations?.sms?.enabled ? 'default' : 'secondary'}>
                    {integrations?.sms?.enabled ? 'مفعل' : 'غير مفعل'}
                  </Badge>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h4 className="font-medium">النسخ الاحتياطي السحابي</h4>
                    <p className="text-sm text-gray-600">AWS S3 للنسخ الاحتياطي</p>
                  </div>
                  <Badge variant={integrations?.backup?.enabled ? 'default' : 'secondary'}>
                    {integrations?.backup?.enabled ? 'مفعل' : 'غير مفعل'}
                  </Badge>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">Webhooks</h4>
                {integrations?.webhooks?.map((webhook: any, index: number) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h5 className="font-medium">{webhook.name}</h5>
                      <p className="text-sm text-gray-600">{webhook.url}</p>
                    </div>
                    <Badge variant={webhook.enabled ? 'default' : 'secondary'}>
                      {webhook.enabled ? 'مفعل' : 'غير مفعل'}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="backup" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>النسخ الاحتياطي</CardTitle>
              <CardDescription>إدارة النسخ الاحتياطية للنظام</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                <div>
                  <h4 className="font-medium">النسخ الاحتياطي التلقائي</h4>
                  <p className="text-sm text-gray-600">يتم إنشاء نسخة احتياطية يومياً في الساعة 2:00 ص</p>
                </div>
                <Badge variant="default">مفعل</Badge>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">آخر نسخة احتياطية</h4>
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">نسخة احتياطية ناجحة</p>
                      <p className="text-sm text-gray-600">
                        تاريخ الإنشاء: {new Date().toLocaleDateString('ar-EG')}
                      </p>
                      <p className="text-sm text-gray-600">الحجم: 125.6 MB</p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4 ml-2" />
                      تحميل
                    </Button>
                  </div>
                </div>
              </div>

              <div className="flex gap-4">
                <Button onClick={createBackup}>
                  <Database className="h-4 w-4 ml-2" />
                  إنشاء نسخة احتياطية الآن
                </Button>
                <Button variant="outline">
                  <Upload className="h-4 w-4 ml-2" />
                  استعادة من نسخة احتياطية
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="system" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>معلومات النظام</CardTitle>
              <CardDescription>تفاصيل النظام والأداء</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>إصدار النظام</Label>
                  <Input value={systemInfo?.version || '1.0.0'} readOnly />
                </div>
                <div className="space-y-2">
                  <Label>البيئة</Label>
                  <Input value={systemInfo?.environment || 'production'} readOnly />
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">قاعدة البيانات</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>النوع</Label>
                    <Input value={systemInfo?.database?.type || 'in_memory'} readOnly />
                  </div>
                  <div className="space-y-2">
                    <Label>الحالة</Label>
                    <Input value={systemInfo?.database?.status || 'connected'} readOnly />
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-blue-600">
                      {systemInfo?.database?.records?.users || 0}
                    </p>
                    <p className="text-sm text-gray-600">المستخدمين</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-green-600">
                      {systemInfo?.database?.records?.clients || 0}
                    </p>
                    <p className="text-sm text-gray-600">العملاء</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-purple-600">
                      {systemInfo?.database?.records?.projects || 0}
                    </p>
                    <p className="text-sm text-gray-600">المشاريع</p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">أداء الخادم</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-yellow-600">45%</p>
                    <p className="text-sm text-gray-600">استخدام الذاكرة</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-red-600">23%</p>
                    <p className="text-sm text-gray-600">استخدام المعالج</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <p className="text-2xl font-bold text-orange-600">67%</p>
                    <p className="text-sm text-gray-600">استخدام القرص</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
