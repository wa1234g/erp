import React, { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: number
  email: string
  full_name: string
  role: string
  avatar?: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string, rememberMe?: boolean, twoFactorCode?: string) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchUser(token)
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async (token: string) => {
    try {
      const apiUrl = 'http://172.16.8.2:8000'
      console.log('Fetching user with token:', token.substring(0, 20) + '...')
      
      const response = await fetch(`${apiUrl}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json'
        }
      })
      
      console.log('Fetch user response status:', response.status)
      
      if (response.ok) {
        const userData = await response.json()
        console.log('User data fetched successfully:', userData)
        setUser(userData)
      } else {
        console.log('Failed to fetch user, clearing tokens')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    } catch (error) {
      console.error('Error fetching user:', error)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string, rememberMe = false, twoFactorCode?: string) => {
    console.log('Login attempt:', { email, rememberMe })
    
    try {
      const apiUrl = 'http://172.16.8.2:8000'
      console.log('Using API URL:', apiUrl)
      
      const response = await fetch(`${apiUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          email,
          password,
          remember_me: rememberMe,
          two_factor_code: twoFactorCode
        })
      })

      console.log('Login response status:', response.status)
      console.log('Login response ok:', response.ok)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('Login error response:', errorText)
        let errorMessage = 'فشل في تسجيل الدخول'
        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorMessage
        } catch (e) {
          console.error('Failed to parse error response:', e)
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      console.log('Login success:', data)
      
      if (!data.access_token || !data.refresh_token || !data.user) {
        console.error('Invalid response data:', data)
        throw new Error('استجابة غير صحيحة من الخادم')
      }
      
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      setUser(data.user)
      console.log('User set successfully:', data.user)
      
    } catch (error) {
      console.error('Login function error:', error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
