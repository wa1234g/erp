import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { financeApi } from '@/lib/api'
import { Plus, TrendingUp, TrendingDown, DollarSign, CreditCard } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function Finance() {
  const [transactions, setTransactions] = useState<any[]>([])
  const [stats, setStats] = useState<any>(null)
  const [cashFlow, setCashFlow] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFinanceData()
  }, [])

  const loadFinanceData = async () => {
    try {
      const [transactionsData, statsData, cashFlowData] = await Promise.all([
        financeApi.getTransactions({ page: 1, limit: 20 }),
        financeApi.getStats(),
        financeApi.getCashFlow(6)
      ])
      
      setTransactions(transactionsData.transactions)
      setStats(statsData)
      setCashFlow(cashFlowData.monthly_data)
    } catch (error) {
      console.error('Error loading finance data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTransactionBadge = (type: string) => {
    const variants: Record<string, any> = {
      income: 'default',
      expense: 'destructive',
      transfer: 'secondary'
    }
    
    const labels: Record<string, string> = {
      income: 'إيراد',
      expense: 'مصروف',
      transfer: 'تحويل'
    }

    return (
      <Badge variant={variants[type] || 'secondary'}>
        {labels[type] || type}
      </Badge>
    )
  }

  const getStatusBadge = (status: string) => {
    const variants: Record<string, any> = {
      pending: 'outline',
      approved: 'default',
      rejected: 'destructive',
      paid: 'default'
    }
    
    const labels: Record<string, string> = {
      pending: 'معلق',
      approved: 'معتمد',
      rejected: 'مرفوض',
      paid: 'مدفوع'
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
          <h1 className="text-3xl font-bold">الحسابات</h1>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {[...Array(3)].map((_, i) => (
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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">الحسابات</h1>
          <p className="text-gray-600 dark:text-gray-400">إدارة الأمور المالية للشركة</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 ml-2" />
          معاملة جديدة
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">إجمالي الإيرادات</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.total_income?.toLocaleString() || 0} ج.م
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingDown className="h-8 w-8 text-red-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">إجمالي المصروفات</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.total_expenses?.toLocaleString() || 0} ج.م
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DollarSign className="h-8 w-8 text-blue-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">صافي الربح</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.net_profit?.toLocaleString() || 0} ج.م
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CreditCard className="h-8 w-8 text-yellow-600" />
              </div>
              <div className="mr-4 flex-1">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">معاملات معلقة</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {stats?.pending_transactions || 0}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="transactions" className="space-y-4">
        <TabsList>
          <TabsTrigger value="transactions">المعاملات</TabsTrigger>
          <TabsTrigger value="reports">التقارير</TabsTrigger>
          <TabsTrigger value="categories">الفئات</TabsTrigger>
        </TabsList>

        <TabsContent value="transactions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>المعاملات المالية</CardTitle>
              <CardDescription>آخر المعاملات المالية</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {transactions.map((transaction) => (
                  <div key={transaction.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800">
                    <div className="flex items-center space-x-4 space-x-reverse">
                      <div className={`h-10 w-10 rounded-full flex items-center justify-center ${
                        transaction.type === 'income' ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        {transaction.type === 'income' ? (
                          <TrendingUp className="h-5 w-5 text-green-600" />
                        ) : (
                          <TrendingDown className="h-5 w-5 text-red-600" />
                        )}
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">
                          {transaction.description}
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {transaction.category_name} • {transaction.client_name}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          {getTransactionBadge(transaction.type)}
                          {getStatusBadge(transaction.status)}
                        </div>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className={`text-lg font-bold ${
                        transaction.type === 'income' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.type === 'income' ? '+' : '-'}{transaction.amount.toLocaleString()} {transaction.currency}
                      </p>
                      <p className="text-sm text-gray-500">
                        {new Date(transaction.transaction_date).toLocaleDateString('ar-EG')}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              
              {transactions.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-500 dark:text-gray-400">لا توجد معاملات</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reports" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>تدفق النقد</CardTitle>
              <CardDescription>آخر 6 أشهر</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={cashFlow}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="income" stroke="#10B981" name="الإيرادات" />
                  <Line type="monotone" dataKey="expenses" stroke="#EF4444" name="المصروفات" />
                  <Line type="monotone" dataKey="net" stroke="#3B82F6" name="صافي الربح" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="categories" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>فئات المعاملات</CardTitle>
              <CardDescription>إدارة فئات الإيرادات والمصروفات</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <p className="text-gray-500 dark:text-gray-400">سيتم إضافة إدارة الفئات قريباً</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
